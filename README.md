Minimize State Table Website
============================

This is a website for minimizing state tables, built using the Flask framework and utilizing the Pandas library for data processing. The website allows users to upload a CSV file containing the state table to minimize. Additionally, users can directly input the state table from the interface.

The website has been deployed and is online at the following link:  [https://logic-design.onrender.com/](https://logic-design.onrender.com/)
## Features

### 1. Upload CSV File

Users can upload a CSV file containing the state table to perform calculations. To upload a file, follow these steps:

1. Access the website at [https://logic-design.onrender.com/](https://logic-design.onrender.com/).
2. Click on the "Upload .csv" button and select the CSV file you want to minimize from your device.
3. Wait for the data to be fully populated in the input table. Press the "Submit" button to start the minimization process.

### 2. Input State Table
In addition to uploading a CSV file, users can also directly input the state table from the interface. To input a state table, follow these steps:

1. Access the website at [https://logic-design.onrender.com/](https://logic-design.onrender.com/).
2. Click on the first cell in the input table. After entering the data, you can press "Enter" to move to the next cell or use the ←,→,↑,↓ keys to navigate to the desired cell.
3.Add a new row by moving the cursor to the last cell and pressing "Enter".
4. After inputting the state table, click the "Submit" button to start the state table minimization.

### 3. Minimize State Table
After uploading a CSV file or inputting the state table, users can minimize the state table to obtain the corresponding result. The state table minimization process will be performed automatically. The execution time will depend on the number of rows in the state table.

### 4. Display Minimized State Table
Once the state table minimization process is complete, the result will be displayed on the user interface. The minimized state table will be presented as a table for easy viewing.

### 5. Show steps
In addition to displaying the final result, the website also provides the functionality to display the step-by-step calculation for tracking the state table minimization process. Users can view each calculation step by clicking the "Detail" button to display the individual steps of the minimization process.

## Automated Test Case Generation Software
The software is written in Python using random functions to generate random test cases. The automated test cases are created and used to verify the correctness of the state table minimization software.
The software is stored in the [Algorithm Validation](https://github.com/Duynghk/LogicDesign/tree/master/AlgorithmValidation) folder.
### It includes the following files:
`create_rating_files.py`: used to generate files for comparing the results of the test case generation algorithm and the state table minimization algorithm.
`draw_compare_chart.py`: used to draw a comparison chart based on the `Compare.csv` file.
`draw_rating_speed.py`: used to draw a speed evaluation chart for the two algorithms.
Some test case files have been pre-generated in the [TestCase](https://github.com/Duynghk/LogicDesign/tree/master/AlgorithmValidation/TestCase) folder.
## Installation and Local Setup
Installation and Local Setup

1. Clone the repository from GitHub:
   ```bash
   git clone https://github.com/Duynghk/LogicDesign.git
2. Install the required libraries:
   ```bash
   pip install -r requirements.txt
3. Run website
   ```bash
   python main.py
