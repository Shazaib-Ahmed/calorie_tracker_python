console.log("date script is running");
var today = new Date();

var dateInput = document.getElementById("date");


var yyyy = today.getFullYear();
var mm = String(today.getMonth() + 1).padStart(2, "0");
var dd = String(today.getDate()).padStart(2, "0");
var maxDate = yyyy + "-" + mm + "-" + dd;


dateInput.setAttribute("max", maxDate);