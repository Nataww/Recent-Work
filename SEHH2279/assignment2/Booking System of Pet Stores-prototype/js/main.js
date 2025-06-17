function init() {
    if(localStorage.getItem('login') == 'yes') {
        document.getElementById("hasLogin").style.display = "";
        document.getElementById("noLogin").style.display = "none";
    }
}