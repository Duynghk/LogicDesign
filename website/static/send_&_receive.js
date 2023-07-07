let data;

// Function to send form data as JSON via XMLHttpRequest
function sendFormData(jsonData) {
  const xhr = new XMLHttpRequest();
  xhr.open("POST", "/");
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.send(jsonData);
  return xhr;
}

// Function to create step tables
function CreateStepTables() {
  const index = ["A", "0", "1"];
  var steps = data.steps;
  const containerSteps = document.getElementById("step-tables");
  const tdiv = document.createElement("div");
  
  // Create tables for each step
  for (let i in steps) {
    const stepNumber = document.createElement("h6");
    stepNumber.setAttribute("class", "step-number");
    stepNumber.textContent = "Step " + (parseInt(i) + 1).toString() + ":";
    var table = document.createElement("table");
    table.setAttribute(
      "class",
      "step" + (parseInt(i) + 1).toString() + "table"
    );
    
    // Parse step data
    const step = JSON.parse(steps[i]["step" + (parseInt(i) + 1).toString()]);
    
    // Populate the table with data
    step.forEach((obj, j) => {
      const row = table.insertRow();
      const cell0 = row.insertCell();
      cell0.innerHTML = index[j];
      for (const k in obj) {
        if (obj.hasOwnProperty(k)) {
          const cell = row.insertCell();
          if (j == 0) {
            cell.innerHTML = "G" + k.toString() + "{" + obj[k].toString() + "}";
          } else {
            cell.innerHTML = obj[k];
          }
        }
      }
    });
    
    tdiv.appendChild(stepNumber);
    tdiv.appendChild(table);
  }
  
  // Remove previous step tables
  while (containerSteps.firstChild) {
    containerSteps.removeChild(containerSteps.firstChild);
  }
  
  // Add the new step tables to the page
  containerSteps.appendChild(tdiv);
  const stepTables = document.getElementById("step-tables");
  stepTables.style.display = "block";
}

// Function to create the result table
function CreateResultTable() {
  var table = document.createElement("table");
  var thead = table.createTHead();
  thead.setAttribute("class", "title-row");
  
  // Create the table headers
  const headers = ["Present State", "Next State", "A = 0", "A = 1"];
  var headerRow = thead.insertRow();
  headerRow.insertAdjacentHTML(
    "beforeend",
    '<th rowspan="2">' + headers[0] + "</th>"
  );
  headerRow.insertAdjacentHTML(
    "beforeend",
    '<th colspan="2">' + headers[1] + "</th>"
  );

  headerRow = table.insertRow();
  headerRow.insertAdjacentHTML("beforeend", "<th>" + headers[2] + "</th>");
  headerRow.insertAdjacentHTML("beforeend", "<th>" + headers[3] + "</th>");
  
  // Parse the result data
  var data_result = data.result;
  const data_array = JSON.parse(data_result);
  
  // Populate the table with data
  data_array.forEach((obj) => {
    const row = table.insertRow();
    
    const presentStateCell = row.insertCell();
    presentStateCell.innerHTML = obj.present_state;

    const nextState0Cell = row.insertCell();
    nextState0Cell.innerHTML = obj.next_state_0;

    const nextState1Cell = row.insertCell();
    nextState1Cell.innerHTML = obj.next_state_1;
  });
  
  // Create Total After element
  var TotalAfterElement = document.createElement("h6");
  TotalAfterElement.className = "total-state-after"
  TotalAfterElement.innerHTML = "Total state: " + data_array.length;
  console.log("Total state: " + data_array.length);
  
  // Get the container element
  const container = document.getElementById("minimize-tables");

  // Remove the previous table
  while (container.firstChild) {
    container.removeChild(container.firstChild);
  }
  
  // Add the new table to the page
  container.appendChild(table);
  container.appendChild(TotalAfterElement);
}

// Function to show error message
function showError(message) {
  const errorElement = document.createElement("div");
  errorElement.setAttribute("class", "alert alert-danger");
  errorElement.role = "alert";
  errorElement.innerText = message;
  const errorContainer = document.getElementById("error-container");
  while (errorContainer.firstChild) {
    errorContainer.removeChild(errorContainer.firstChild);
  }
  errorContainer.appendChild(errorElement);
  
  // Remove the error message after 0.5 seconds
  setTimeout(() => {
    errorElement.remove();
  }, 500);
}

// Function to submit the form
function submitForm() {
  const form = document.querySelector("form");
  
  // Add event listener to the form's submit event
  form.addEventListener("submit", onSubmit);
  
  function onSubmit(event) {
    event.preventDefault();
    form.removeEventListener("submit", onSubmit);
    
    const tableData = [];
    var tableRows = document.querySelectorAll(".input-table tr");
    
    // Remove empty rows at the end
    const table = document.querySelector(".my-table");
    const rows = table.rows;
    var lastIndex = rows.length - 1;
    
    while (lastIndex >= 0) {
      var lastRow = rows[lastIndex];
      var input1 = lastRow.querySelector(
        "input[name=row" + (lastIndex-1) + "col1]"
      );
      var input2 = lastRow.querySelector(
        "input[name=row" + (lastIndex-1) + "col2]"
      );
      var input3 = lastRow.querySelector(
        "input[name=row" + (lastIndex-1) + "col3]"
      );
      
      if (
        input1.value.trim() === "" &&
        input2.value.trim() === "" &&
        input3.value.trim() === ""
      ) {
        lastRow.remove();
        lastIndex--;
      } else {
        break;
      }
    }
    
    tableRows = document.querySelectorAll(".input-table tr");
    
    // Update Total Before element
    var TotalBeforeElement = document.getElementsByClassName("total-state-before")[0];
    TotalBeforeElement.textContent = "Total state: " + (tableRows.length);
    
    // Retrieve data from each row
    tableRows.forEach((row) => {
      const presentState = row.querySelector(
        'input[name^="row"][name$="col1"]'
      ).value;
      const nextState0 = row.querySelector(
        'input[name^="row"][name$="col2"]'
      ).value;
      const nextState1 = row.querySelector(
        'input[name^="row"][name$="col3"]'
      ).value;
      const rowData = {
        present_state: presentState,
        next_state_0: nextState0,
        next_state_1: nextState1,
      };
      tableData.push(rowData);
    });
    
    const jsonData = JSON.stringify(tableData);
    const xhr = sendFormData(jsonData);
    const spinner = document.querySelector(".spinner.center");
    
    // Handle the XMLHttpRequest response
    xhr.onreadystatechange = function () {
      if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
        const json = JSON.parse(this.responseText);
        console.log(json);
        if (json.status === "success") {
          data = json.data;
          CreateResultTable();
          const detailBtn = document.querySelector(".details-btn");
          detailBtn.style.display = "block";
        } else {
          showError(json.message);
        }
        spinner.style.display = "none";
      }
    };
    
    const stepTables = document.getElementById("step-tables");
    stepTables.style.display = "none";
    spinner.style.display = "block";
  }
}
