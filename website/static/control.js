function addRow() {
  var table = document.getElementsByTagName("table")[0];
  var newRow = table.insertRow(table.rows.length);
  for (var i = 0; i < 3; i++) {
    var newCell = newRow.insertCell(i);
    newCell.innerHTML =
      '<input type="text" name="row' +
      (newRow.rowIndex - 1) +
      "col" +
      (i + 1) +
      '" + autocomplete="off"/>';
  }
  initTableNavigation();
}

function initTableNavigation() {
  var cells = document.querySelectorAll('input[type="text"]');
  const table = document.querySelector(".my-table");

  cells.forEach((cell) => {
    cell.addEventListener("keydown", (event) => {
      const currentCellIndex = Array.from(cells).indexOf(event.target);
      let nextCellIndex;
      const rows = table.rows;
      const lastCellIndex = (rows.length - 2)*3-1;

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
          event.preventDefault(); // Ngăn chặn hành vi mặc định của phím Enter
          nextCellIndex = currentCellIndex + 1;
          if (currentCellIndex === lastCellIndex) {
            addRow();
          }
          break;
        default:
          return;
      }
      cells = document.querySelectorAll('input[type="text"]');
      if (nextCellIndex >= 0 && nextCellIndex < cells.length) {
        cells[nextCellIndex].focus();
      }
    });
  });
}

function handleFileUpload() {
  var fileInput = document.getElementById("file");
  var file = fileInput.files[0];
  var reader = new FileReader();
  reader.onload = function (e) {
    var contents = e.target.result;
    var rows = contents.split("\n");
    // Xóa các hàng hiện tại trong bảng (trừ dòng tiêu đề)
    var tableBody = document.querySelector(".input-table");
    while (tableBody.rows.length > 0) {
      tableBody.deleteRow(0);
    }
    // Tạo hàng mới cho mỗi dòng trong file
    for (var i = 1; i < rows.length; i++) {
      var cols = rows[i].split(",");
      var newRow = tableBody.insertRow(i - 1);
      for (var j = 0; j < cols.length; j++) {
        var newCell = newRow.insertCell(j);
        var input = document.createElement("input");
        input.type = "text";
        input.name = "row" + i + "col" + (j + 1);
        input.autocomplete = "off";
        input.placeholder = "S" + i + " " + j;
        input.value = cols[j];
        newCell.appendChild(input);
      }
    }
    initTableNavigation();
  };
  reader.readAsText(file);
  // Hiển thị tên file được chọn
  var fileNameElement = document.getElementById("file-name");
  fileNameElement.textContent = file.name;
}
