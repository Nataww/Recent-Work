function selectIt(id) {
    var findOldButton = document.getElementsByName("selectedType")[0];
    findOldButton.removeAttribute("name");
    findOldButton.classList.remove("selected");
    document.getElementById(id).name = "selectedType";
    document.getElementById(id).classList.add("selected");
  }
  

function sendConfirm() {
	var date = document.getElementById("chooseDate").value;
	if(date == "") {
		alert("Date cannot be empty");
		return;
	}
	var types = document.getElementById("types").value;
	var facilities = document.getElementById("facilities").value;
	var places = document.getElementById("places").value;
	var timeperiod = document.getElementById("timeperiod").value;
	document.getElementById("confirmDate").innerHTML = "Date: "+date;
	document.getElementById("confirmType").innerHTML = "Type: "+types;
	document.getElementById("confirmFacilities").innerHTML = "Facilities: "+facilities;
	document.getElementById("confirmVenue").innerHTML = "Venue: "+places;
	document.getElementById("confirmTime").innerHTML = "Time: "+timeperiod;
    document.getElementById("step1").style.display = "none";
    document.getElementById("step2").style.display = "";
	selectIt("Confirmation");
}

function confirm() {
    document.getElementById("step2").style.display = "none";
    document.getElementById("step3").style.display = "";
	selectIt("Payment");
}

function pay() {
	var date = document.getElementById("chooseDate").value;
	var types = document.getElementById("types").value;
	var facilities = document.getElementById("facilities").value;
	var places = document.getElementById("places").value;
	var timeperiod = document.getElementById("timeperiod").value;


	var cardn = document.getElementById("cardn").value;
	var cardd = document.getElementById("cardd").value;
	var cardcvc = document.getElementById("cardcvc").value;
	var cardo = document.getElementById("cardo").value;
	if(cardn == "" || cardd == "" || cardcvc == "" || cardo == "") {
		alert("Payment Data cannot be empty");
		return;
	}

	document.getElementById("pay_confirmDate").innerHTML = "Date: "+date;
	document.getElementById("pay_confirmType").innerHTML = "Type: "+types;
	document.getElementById("pay_confirmFacilities").innerHTML = "Facilities: "+facilities;
	document.getElementById("pay_confirmVenue").innerHTML = "Venue: "+places;
	document.getElementById("pay_confirmTime").innerHTML = "Time: "+timeperiod;
    document.getElementById("step3").style.display = "none";
    document.getElementById("step4").style.display = "";
	selectIt("Recipe");

}

function backStep1() {
    document.getElementById("step1").style.display = "";
    document.getElementById("step2").style.display = "none";
	selectIt("selectServices");
}

function backStep2() {
    document.getElementById("step2").style.display = "";
    document.getElementById("step3").style.display = "none";
	selectIt("Confirmation");
}