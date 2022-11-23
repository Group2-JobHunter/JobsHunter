document.addEventListener("contextmenu", (event) => event.preventDefault());
function createButtons(url) {
  let td = document.createElement("td");
  let button = document.createElement("button");
  button.innerHTML = "Apply";
  button.classList.add("apply");
  button.onclick = function () {
    window.open(url, "_blank");
  };
  td.appendChild(button);
  return td;
}

function hideLoader() {
  let loaderContainer = document.querySelector(".loaderContainer");
  loaderContainer.style.display = "none";
}

async function csv() {
  results = await eel.resultsToCsv()();
  document.querySelector(".csv").disabled = true;
  document.querySelector(".csv").style.opacity = 0.1;
}

function initTable(data) {
  let tableColums = [
    "Source",
    "Title",
    "Company",
    "Date",
    "City",
    "Country",
    "Matching",
    "Poster",
  ];
  let row = document.createElement("tr");

  tableColums.map((col) => {
    row.innerHTML += `<th>${col}</th>`;
  });
  document.querySelector("#myTable thead").append(row);
  data.forEach((element) => {
    let rowData = document.createElement("tr");
    //  ("LinkedIn",title,company,date,self.city,self.country,percent,link)
    for (let i = 0; i < element.length; i++) {
      let key = element[i];
      if (i == 7) {
        rowData.appendChild(createButtons(key));
        continue;
      }
      if (i == 6) key = ` ${key} %`;

      let td = document.createElement("td");

      td.innerHTML = key;
      rowData.appendChild(td);
      td = null;
    }
    document.querySelector("#myTable tbody").append(rowData);
  });
}

function sortMatching(a, b, asc) {
  let x = a.split(" ")[0];
  let y = b.split(" ")[0];

  return (parseInt(x) - parseInt(y)) * asc;
}

function sortByDate(a, b, asc) {
  if (a < b) {
    return 1 * asc;
  }
  if (a > b) {
    return -1 * asc;
  }
  return 0;
}

function sortTableByColumn(table, column, asc = true) {
  const dirModifier = asc ? 1 : -1;
  const tBody = table.tBodies[0];
  const rows = Array.from(tBody.querySelectorAll("tr"));

  const sortedRows = rows.sort((a, b) => {
    const aColText = a
      .querySelector(`td:nth-child(${column + 1})`)
      .textContent.trim();
    const bColText = b
      .querySelector(`td:nth-child(${column + 1})`)
      .textContent.trim();
    if (column == 6) {
      a = aColText.split(" ")[0];
      b = bColText.split(" ")[0];
      return sortMatching(a, b, dirModifier);
    } else if (column == 3) return sortByDate(aColText, bColText, dirModifier);
    else return aColText > bColText ? 1 * dirModifier : -1 * dirModifier;
  });

  // Remove all existing TRs from the table
  while (tBody.firstChild) {
    tBody.removeChild(tBody.firstChild);
  }

  // Re-add the newly sorted rows
  tBody.append(...sortedRows);

  // Remember how the column is currently sorted
  table
    .querySelectorAll("th")
    .forEach((th) => th.classList.remove("th-sort-asc", "th-sort-desc"));
  table
    .querySelector(`th:nth-child(${column + 1})`)
    .classList.toggle("th-sort-asc", asc);
  table
    .querySelector(`th:nth-child(${column + 1})`)
    .classList.toggle("th-sort-desc", !asc);
}

async function work() {
  let results = null;
  results = await eel.fetch()(); // import from data base

  hideLoader();
  initTable(results);

  document.querySelectorAll(".table-sortable th").forEach((headerCell) => {
    console.log(headerCell);
    headerCell.addEventListener("click", function () {
      const tableElement = headerCell.parentElement.parentElement.parentElement;
      console.log("Yes");
      const headerIndex = Array.prototype.indexOf.call(
        headerCell.parentElement.children,
        headerCell
      );
      const currentIsAscending = headerCell.classList.contains("th-sort-asc");

      sortTableByColumn(tableElement, headerIndex, !currentIsAscending);
    });
  });
}

work();
