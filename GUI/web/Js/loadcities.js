var countrySelector = document.getElementById("timeZoneSelector1");
var citySelector = document.getElementById("timeZoneSelector2");

var selectedCountry;
var selectedCity;

var IsCountryloaded = false;
var ISCityLoaded = false;

selectedCountry = "JORDAN";

function loadCountries(countryName) {
  if (IsCountryloaded == false) {
    document.getElementById("timeZoneSelector1").innerText = null;
    for (let countryData in countries) {
      let opt = document.createElement("option");
      opt.value = countryData;
      opt.innerHTML = countryData;
      countrySelector.appendChild(opt);
    }

    IsCountryloaded = true;
  }

  ISCityLoaded = false;

  selectedCountry = countryName;
}

function loadCities(cityname) {
  selectedCity = cityname;
  ISCityLoaded = false;

  var path = selectedCountry + ".";
  paths = path.split(".");
  var City_obj_path = countries;
  var citiesNamesPath;

  for (var i = 0; i < paths.length; ++i) {
    if (City_obj_path[paths[i]] == undefined) {
      return undefined;
    } else {
      City_obj_path = City_obj_path[paths[i]];
    }
    citiesNamesPath = City_obj_path.citiesNames;
    break;
  }

  // load the cities from citiesdb.js using Dot Notation.
  cities = countries[cityname]["citiesNames"];
  if (ISCityLoaded == false) {
    console.log("YES");
    document.getElementById("timeZoneSelector2").innerText = null;
    for (let city of cities) {
      let opt = document.createElement("option");
      opt.value = city;
      console.log(city);
      city = city.replace("_", " ");
      opt.innerHTML = city.toUpperCase();
      citySelector.appendChild(opt);
    }

    ISCityLoaded = true;
  }

  selectedCity = cityname;
}

loadCountries(selectedCountry);
loadCities(selectedCountry);

var options = countrySelector.options;
for (var i = 0; i < options.length; i++) {
  if (options[i].value === selectedCountry) {
    options[i].selected = true;
    break;
  }
}

var options = citySelector.options;
for (var i = 0; i < options.length; i++) {
  if (options[i].value === "AMMAN") {
    options[i].selected = true;
    break;
  }
}

var levels = document.getElementById("levels");
lvls = [
  "Internship",
  "Novice",
  "Entry level",
  "junior",
  "Intermediate",
  "Mid-level",
  "Associate",
  "Mid-Senior level",
  "Expert",
  "Director",
];

for (let lvl of lvls) {
  let opt = document.createElement("option");
  opt.value = lvl;
  opt.innerHTML = lvl.toUpperCase();
  levels.appendChild(opt);
}
