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

function initTable(data) {
  let tableColums = [
    "Source",
    "Title",
    "Date",
    "Matching",
    "city",
    "country",
    "Level",
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
      if (i == 6) key = `Matched ${key} %`;

      let td = document.createElement("td");

      td.innerHTML = key;
      rowData.appendChild(td);
      td = null;
    }
    document.querySelector("#myTable tbody").append(rowData);
  });
}

async function work() {
  let results = null;

  console.log("waiting");
  results = await eel.start_scrapping()();
  console.log(results);
  hideLoader();
  initTable(results);
}

work();
