import pandas as pd
import os
def pre_processing_state_table(data_df):
    """
    This function takes a pandas DataFrame as input and splits the next_state_0 and next_state_1 columns 
    into two columns each.
    """
    data_df = data_df.applymap(lambda x: x.strip())
    data_df[['next_state_0', 'output_0']] = data_df['next_state_0'].str.split('-|/|\s', expand=True)
    data_df[['next_state_1', 'output_1']] = data_df['next_state_1'].str.split('-|/|\s', expand=True)
    return data_df

def grouping_states(data_df):
    """
    This function groups the present_state, next_state_0, and next_state_1 columns 
    by their output values.
    """
    grouped = data_df.groupby(['output_0', 'output_1']).agg({
        'present_state': lambda x: list(x),
        'next_state_0': lambda x: list(x),
        'next_state_1': lambda x: list(x)
    }).reset_index()
    grouped['group'] = grouped['present_state']
    grouped.drop(['present_state','output_0', 'output_1'], axis=1, inplace=True)
    grouped_table = grouped.transpose()
    grouped_table = grouped_table.iloc[[-1] + list(range(len(grouped_table)-1))]
    return grouped_table

def create_state_map(grouped_table):
    """
    This function creates a state map that maps each state to its group.
    """
    state_map = pd.DataFrame(columns=['state','group'])
    for col_name, col_data in grouped_table.iloc[0].items():  
        for data  in col_data:  
            new_row = [data,col_name]
            state_map.loc[len(state_map)] = new_row
    return state_map


def group_next_states(grouped_table, state_map):
    """
    This function groups the next states based on the state map.
    """
    def find_group_by_state(state_map, state_group):
        """
        This function finds the group for a given state (or a list of states).
        """
        list_group = list(range(len(state_group)))
        for index, state_value in enumerate(state_group):
            list_group[index] = state_map.loc[state_map['state'] == state_value, 'group'].iloc[0]
        return list_group
    i = 0
    while i < grouped_table.shape[1]: 
        grouped_table.iat[1,i] = find_group_by_state(state_map, grouped_table.iat[1,i])
        grouped_table.iat[2,i] = find_group_by_state(state_map, grouped_table.iat[2,i])
        i += 1
    grouped_table = grouped_table.rename(index={'next_state_0': 'next_group_0', 'next_state_1': 'next_group_1'})
    return grouped_table

def check_finish(grouped_table):
    """
    This function checks if the state table minimization is finished.
    """
    grouped_table = grouped_table.iloc[[1,2]].copy()
    for row in grouped_table.itertuples():
        for index in range(1,grouped_table.shape[1]+1):
            cell = row[index]
            if len(cell) > 1:
                for j in range(1,len(cell)):
                    if cell[j] != cell[j-1]:
                        return False
    return True

def split_groups(grouped_table, states_table):
    """
    This function splits the groups in the state table.
    """
    def split_columns(pre_list, split_position):
        new_list = [pre_list[i] for i in split_position]
        offset = 0
        for i in split_position:
            pre_list.pop(i-offset)
            offset += 1
        return new_list
    i = 0
    grouped_table = pd.concat([grouped_table, states_table], axis=0)
    while i < grouped_table.shape[1]:
        list1 = grouped_table.iloc[1,i]
        list2 = grouped_table.iloc[2,i]
        if len(list1) > 1:
            split_position = []
            have_split = False
            for j in range(1,len(list1)):
                if list1[0] != list1[j] or list2[0] != list2[j]:
                    split_position.append(j)
                    have_split = True
            if have_split:
                new_col = grouped_table.iloc[:,i].apply(split_columns, args=(split_position,))
                # grouped_table.insert(i+1, grouped_table.shape[1], new_col)
                grouped_table = pd.concat([grouped_table, pd.DataFrame(new_col)], axis=1, ignore_index=True)
        i += 1
    grouped_table = grouped_table.drop(['next_group_0', 'next_group_1'])
    return grouped_table


def minimize_state_table(file_name,directory):
    file_path = os.path.join(directory, file_name)
    data = pd.read_csv(file_path)
    # Pre-process the state table by splitting the next state columns and removing any leading/trailing white space
    state_table = pre_processing_state_table(pd.DataFrame(data))

    
    # Group the states based on their next states and output symbols
    grouped_table = grouping_states(state_table.copy())
    
    # Extract the next states from the grouped table
    next_states = grouped_table.iloc[1:].copy()
    
    # Create a mapping between each state and its corresponding group
    state_map = create_state_map(grouped_table)
    
    # Group the next states based on their group mappings
    grouped_table = group_next_states(grouped_table, state_map)


    # Repeatedly split the groups until no further splitting is possible
    step_number = 2
    print("\nMinimizing")
    while check_finish(grouped_table) is not True:
        print(".")
        # Split the groups based on their next states and output symbols
        splited_table = split_groups(grouped_table,next_states)
        grouped_table = splited_table
        
        # Extract the next states from the updated grouped table
        next_states = grouped_table.iloc[1:].copy()
        
        # Update the mapping between each state and its corresponding group
        state_map = create_state_map(grouped_table)
        
        # Group the next states based on their group mappings
        grouped_table = group_next_states(grouped_table, state_map)


        step_number += 1
    
    # Create a dictionary to map each state in a group to the group's representative state
    new_name_dict = dict()
    for _, cell in grouped_table.iloc[0].items():
        for i in range(1,len(cell)):
            new_name_dict[cell[i]] = cell[0] 
    
    # Remove duplicate states from the original state table
    result_state_table = state_table.set_index("present_state")
    row_number_before = result_state_table.shape[0]
    for _, cell in grouped_table.iloc[0].items():
        result_state_table = result_state_table.drop(cell[1:], axis=0)

    return row_number_before - result_state_table.shape[0]