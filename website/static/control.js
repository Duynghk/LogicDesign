function addRow() {
  // Get the table element
  var table = document.getElementsByTagName("table")[0];

  // Insert a new row at the end of the table
  var newRow = table.insertRow(table.rows.length);

  // Add three cells to the new row
  for (var i = 0; i < 3; i++) {
    var newCell = newRow.insertCell(i);

    // Set the HTML content of each cell to an input element
    newCell.innerHTML =
      '<input type="text" name="row' +
      (newRow.rowIndex - 1) +
      "col" +
      (i + 1) +
      '" + autocomplete="off"/>';
  }

  // Call the initTableNavigation function to enable navigation within the table
  initTableNavigation();
}

function initTableNavigation() {
  // Get all input elements of type "text"
  var cells = document.querySelectorAll('input[type="text"]');

  // Get the table element with class "my-table"
  const table = document.querySelector(".my-table");

  cells.forEach((cell) => {
    // Add a keydown event listener to each input element
    cell.addEventListener("keydown", (event) => {
      // Get the index of the current cell
      const currentCellIndex = Array.from(cells).indexOf(event.target);
      let nextCellIndex;

      // Get the rows of the table
      const rows = table.rows;

      // Calculate the index of the last cell
      const lastCellIndex = (rows.length - 2) * 3 - 1;

      // Handle different key presses
      switch (event.key) {
        case "ArrowLeft":
          nextCellIndex = currentCellIndex - 1;
          break;
        case "ArrowRight":
          nextCellIndex = currentCellIndex + 1;
          break;
        case "ArrowUp":
          nextCellIndex = currentCellIndex - 3;
          break;
        case "ArrowDown":
          nextCellIndex = currentCellIndex + 3;
          break;
        case "Enter":
          event.preventDefault();
          nextCellIndex = currentCellIndex + 1;

          // Add a new row if the current cell is the last cell
          if (currentCellIndex === lastCellIndex) {
            addRow();
          }
          break;
        default:
          return;
      }

      // Update the cells collection after adding a new row
      cells = document.querySelectorAll('input[type="text"]');

      // Focus on the next cell if it exists
      if (nextCellIndex >= 0 && nextCellIndex < cells.length) {
        cells[nextCellIndex].focus();
      }
    });
  });
}

function handleFileUpload() {
  // Get the file input element
  var fileInput = document.getElementById("file");

  // Get the selected file
  var file = fileInput.files[0];

  // Create a new FileReader
  var reader = new FileReader();

  reader.onload = function (e) {
    // Get the contents of the file
    var contents = e.target.result;

    // Split the contents into rows
    var rows = contents.split("\n");

    // Clear the current table rows (except the header row)
    var tableBody = document.querySelector(".input-table");
    while (tableBody.rows.length > 0) {
      tableBody.deleteRow(0);
    }

    // Create new rows for each row in the file
    for (var i = 1; i < rows.length; i++) {
      var cols = rows[i].split(",");
      var newRow = tableBody.insertRow(i - 1);

      // Add cells to the new row
      for (var j = 0; j < cols.length; j++) {
        var newCell = newRow.insertCell(j);
        var input = document.createElement("input");

        // Set properties for the input element
        input.type = "text";
        input.name = "row" + i + "col" + (j + 1);
        input.autocomplete = "off";
        input.placeholder = "S" + i + " " + j;
        input.value = cols[j];

        // Append the input element to the cell
        newCell.appendChild(input);
      }
    }

    // Call the initTableNavigation function to enable navigation within the table
    initTableNavigation();

    // Update the "Total state" element with the number of rows
    var TotalBeforeElement =
      document.getElementsByClassName("total-state-before")[0];
    TotalBeforeElement.textContent = "Total state: " + (rows.length - 1);
  };

  // Read the file as text
  reader.readAsText(file);

  // Display the selected file name
  var fileNameElement = document.getElementById("file-name");
  fileNameElement.textContent = file.name;
}
