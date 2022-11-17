function User(jobTitil, Date, Skills, Level,source) {
    this.jobTitil = jobTitil;
    this.Date = Date;
    this. Skills =  Skills;
    this.Level = Level;
    this.source=source;
  }
  
  let myArr = [
    new User('Leonardo', '30 jan', 'Santorini', 'mid',"https://blog.codepen.io/documentation/preview-template/"),
    new User('Edoardo', '30 jan', 'Monaco', 'hige',"https://blog"),
    new User('Nicole', '30 jan ', 'Milano', 'good',"https://blog.codepen.io/documentation/preview-template/"),
    new User('Jasmine', '30 jan', 'Los Angeles', 'bad',"https://blog.codepen.io/documentation/preview-template/"),
    new User('Emily', '30 jan', 'San Francisco', 'very good',"https://blog.codepen.io/documentation/preview-template/")
  ]
  //console.log(myArr);
  
  document.querySelector("#myTable tbody").innerHTML = myArr.map(user => `<tr><td>${user.jobTitil}</td><td>${user.Date}</td><td>${user. Skills}</td><td>${user.Level}</td> <td>${user.source}</td></tr>`).join('')