function User(jobTitil, Date, Skills, Level, source) {
  this.website = "Test";
  this.jobTitil = jobTitil;
  this.date = Date;
  this.Skills = Skills;
  this.Level = Level;
  this.source = source;
}

let myArr = [
  new User(
    "Leonardo",
    "30 jan",
    "Santorini",
    "mid",
    "https://blog.codepen.io/documentation/preview-template/"
  ),
  new User("Edoardo", "30 jan", "Monaco", "hige", "https://blog"),
  new User(
    "Nicole",
    "30 jan ",
    "Milano",
    "good",
    "https://blog.codepen.io/documentation/preview-template/"
  ),
  new User(
    "Jasmine",
    "30 jan",
    "Los Angeles",
    "bad",
    "https://blog.codepen.io/"
  ),
  new User(
    "Emily",
    "30 jan",
    "San Francisco",
    "very good",
    "https://blog.codepen.io/documentation/"
  ),
];

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
  let tableColums = ["Source", "Title", "Date", "Matching", "Level", "Poster"];
  let row = document.createElement("tr");

  tableColums.map((col) => {
    row.innerHTML += `<th>${col}</th>`;
  });
  document.querySelector("#myTable thead").append(row);

  data.forEach((element) => {
    let rowData = document.createElement("tr");
    for (const key in element) {
      if (element[key].includes("https"))
        rowData.appendChild(createButtons(element[key]));
      else {
        let td = document.createElement("td");
        td.innerHTML = element[key];
        rowData.appendChild(td);
        td = null;
      }
    }

    document.querySelector("#myTable tbody").append(rowData);
  });
}

async function work() {
  let results = null;

  console.log("waiting");
  results = await eel.startScrapping()();
  console.log(results);
  hideLoader();
  initTable(myArr);
}

work();
