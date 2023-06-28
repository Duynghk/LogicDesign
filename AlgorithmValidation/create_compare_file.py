import shutil
import os
import pandas as pd
from minimize_state_table import minimize_state_table
from create_testcase import create_testcase

DIRECTORY = 'TestCase' # Name of directory to store test cases
MAX_STATE = 1000  # Maximum of state in the states table
FILE_NUMBER = 100 # Number of test cases

# Create an empty DataFrame to store the results
df = pd.DataFrame(columns=['File', 'State Number', 'Number of states to minimize', "Number of minimized states"])


# Check if the directory exists
if os.path.exists(DIRECTORY):
    # Get the list of files and directories in the directory
    items = os.listdir(DIRECTORY)
    
    # Remove files and directories in the directory
    for item in items:
        item_path = os.path.join(DIRECTORY, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        else:
            shutil.rmtree(item_path)
else:
    # Create the directory if it doesn't exist
    os.makedirs(DIRECTORY)

# Generate test cases and perform state minimization
for i in range(FILE_NUMBER):
    testcase = create_testcase(DIRECTORY, max_state=MAX_STATE)
    reduce_state_num = minimize_state_table(testcase["File"],DIRECTORY,True,"")
    df.loc[i] = [testcase["File"], testcase["State Number"], testcase['Number of states to minimize'], reduce_state_num]

# Save the results to a CSV file
df.to_csv("Compare.csv", index=False, encoding='utf-8-sig')
