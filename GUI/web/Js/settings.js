//document.addEventListener("contextmenu", (event) => event.preventDefault());
resizeTo(screen.width, screen.height);

let searchData = {
  keywords: [],
  title: "",
  country: "",
  city: "",
};

let keywords = [];
let title = document.getElementById("title");
let coutry = document.getElementById("timeZoneSelector1");
let city = document.getElementById("timeZoneSelector2");
levels = document.getElementById("levels");

let search = document.getElementById("search");
search.addEventListener("click", start);

async function start() {
  let selectedCountry = coutry.options[coutry.selectedIndex].value;
  let selectedCity = city.options[city.selectedIndex].value;

  searchData.keywords = keywords;
  searchData.title = title.value;
  searchData.country = selectedCountry;
  searchData.city = selectedCity;
  console.log(searchData);
  localStorage.setItem("data", JSON.stringify(searchData));
  //   console.log("test");
  // let test = await eel.get_python()();

  //await eel.get_search_data(searchData)();
  //console.log(test);
  window.location.assign("./table.html");
}

function saveSotarge() {
  let data = localStorage.getItem("data");

  if (data == null) {
    return;
  }
  data = JSON.parse(data);
  console.log(keywords);
  data.keywords = keywords;
  console.log(data.keywords);
  localStorage.setItem("data", JSON.stringify(data));
}

function init_List() {
  // Create a "close" button and append it to each list item

  var myNodelist = document.getElementsByTagName("li");
  var i;
  for (i = 0; i < myNodelist.length; i++) {
    var span = document.createElement("SPAN");
    var txt = document.createTextNode("\u00D7");
    span.className = "close";
    span.appendChild(txt);
    myNodelist[i].appendChild(span);
  }
  // Click on a close button to hide the current list item
  var close = document.getElementsByClassName("close");
  var i;
  for (i = 0; i < close.length; i++) {
    close[i].onclick = function () {
      var div = this.parentElement;
      div.style.display = "none";
      console.log(div);
    };
  }
}

function createKeyword(key) {
  // Create LI
  var li = document.createElement("li");
  var inputValue = document.getElementById("Skills").value || key;

  var t = document.createTextNode(inputValue);
  li.appendChild(t);
  if (inputValue === "") {
    return;
  } else {
    document.getElementById("myUL").appendChild(li);
  }

  document.getElementById("Skills").value = "";
  var span = document.createElement("SPAN");
  var txt = document.createTextNode("\u00D7");
  span.className = "close";
  span.appendChild(txt);
  span.onclick = function () {
    var div = this;
    let key = div.parentElement.firstChild.textContent.trim();
    div.parentElement.style.display = "none";
    keywords = keywords.filter(function (item) {
      return item !== key;
    });
    saveSotarge();
  };
  li.appendChild(span);
}

function levelSelection() {
  let exp = levels.options[levels.selectedIndex].value;
  Fill_List(exp);
}

function Fill_List(keyword) {
  // Blink
  let list = document.getElementById("myUL");
  list.classList.add("blink_me");
  let text = document.getElementById("Skills").value || keyword;
  createKeyword(text);
  setTimeout(() => {
    list.classList.remove("blink_me");
  }, 550);

  keywords.push(text);
  console.log(keywords);
  saveSotarge();
}

let data = localStorage.getItem("data");

if (data != null) {
  data = JSON.parse(data);

  keywords = data.keywords;
  for (const key of keywords) {
    console.log(key);
    createKeyword(key);
  }
}
