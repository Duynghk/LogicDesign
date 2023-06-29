import random
import pandas as pd
import os
from minimize_state_table import minimize_state_table
import time

def create_testcase(directory,max_state):
    start_time = time.time()
    # Generate a random STATE_NUMBER
    STATE_NUMBER = random.randint(10, max_state)

    # Generate a random target sum
    target_sum = random.randint(10,STATE_NUMBER)

    # Divide the target sum into four groups with an average value
    groups = [None] * 4
    avg = int(target_sum/4)
    groups[0] = groups[1] = groups[2] = avg
    groups[3] = target_sum - (groups[0] + groups[1] + groups[2])
    
    # Randomize the groups
    for i in range(4):
        groups[0] = groups[0] - int(groups[0]*0.2)
        groups[1] = groups[1] + int(groups[0]*0.2)
        random.shuffle(groups)

    reduce_state_num = sum(groups) - 4
    groups.insert(0,0)
    groups[2] = groups[1] + groups[2]
    groups[3] = groups[2] + groups[3]
    groups[4] = groups[3] + groups[4]

    # Create an empty DataFrame to store the test case
    df = pd.DataFrame(columns=['present_state', 'next_state_0', 'next_state_1'])

    arr = list(range(STATE_NUMBER))
    random.shuffle(arr)
    split_index = groups[4]
    same_state_arr = arr[:split_index]
    different_state_arr = arr[split_index:]
    diff_len = len(different_state_arr)
    
    chosen_group_0 = 0
    chosen_group_1 = 0
    for i in range(STATE_NUMBER):
        if i in groups:
            chosen_group_0 = random.randint(0,3)
            chosen_group_1 = random.randint(0,3)
    
        present_state = "S" + str(arr[i])
        if i < groups[1]:
            next_state_0 = 'S' + str(same_state_arr[random.randint(groups[chosen_group_0],groups[chosen_group_0+1]-1)]) + '/' + "0"
            next_state_1 = 'S' + str(same_state_arr[random.randint(groups[chosen_group_1],groups[chosen_group_1+1]-1)]) + '/' + "0"
        elif i < groups[2]:
            next_state_0 = 'S' + str(same_state_arr[random.randint(groups[chosen_group_0],groups[chosen_group_0+1]-1)]) + '/' + "0"
            next_state_1 = 'S' + str(same_state_arr[random.randint(groups[chosen_group_1],groups[chosen_group_1+1]-1)]) + '/' + "1"
        elif i < groups[3]:
            next_state_0 = 'S' + str(same_state_arr[random.randint(groups[chosen_group_0],groups[chosen_group_0+1]-1)]) + '/' + "1"
            next_state_1 = 'S' + str(same_state_arr[random.randint(groups[chosen_group_1],groups[chosen_group_1+1]-1)]) + '/' + "0"
        elif i < groups[4]:
            next_state_0 = 'S' + str(same_state_arr[random.randint(groups[chosen_group_0],groups[chosen_group_0+1]-1)]) + '/' + "1"
            next_state_1 = 'S' + str(same_state_arr[random.randint(groups[chosen_group_1],groups[chosen_group_1+1]-1)]) + '/' + "1"
        else:
            next_state_0 = 'S' + str(different_state_arr[random.randint(0,diff_len-1)]) + '/' + str(random.randint(0,1))
            next_state_1 = 'S' + str(different_state_arr[random.randint(0,diff_len-1)]) + '/' + str(random.randint(0,1))      
        df.loc[i] = [present_state, next_state_0, next_state_1]
    if groups[4] < STATE_NUMBER:
        subset_df = df.iloc[groups[4]:STATE_NUMBER]
        duplicate_count = minimize_state_table("","",False,subset_df)['Number of states']
        reduce_state_num += duplicate_count
        print("Repeated random state: ",duplicate_count)
    shuffled_df = df.sample(frac=1)

    # Generate a unique file name
    file_name = str(STATE_NUMBER) + '_states.csv'
    file_path = os.path.join(directory, file_name)
    counter = 1
    while os.path.exists(file_path):
        file_name = f"{str(STATE_NUMBER)}_states({counter}).csv"
        file_path = os.path.join(directory, file_name)
        counter += 1
    
    # Save the shuffled DataFrame to a CSV file
    shuffled_df.to_csv(file_path, index=False)
    with open(file_path, 'rb+') as file:
        file.seek(-2, 2)
        file.truncate()
    
    print("\nCreated testcase")
    end_time = time.time()
    execution_time = end_time - start_time
    # Store information about the test case
    info_testcase = {}
    info_testcase['File'] = file_name
    info_testcase['State Number'] = str(STATE_NUMBER)
    info_testcase['Number of states'] = reduce_state_num
    info_testcase['Execution time'] = execution_time
    
    return info_testcase
create_testcase("TestCase",15)
