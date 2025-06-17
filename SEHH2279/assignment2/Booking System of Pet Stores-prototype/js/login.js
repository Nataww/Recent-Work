function login() {
    var username = document.getElementById("username");
    var password = document.getElementById("password");
    if(username.value == "1234" && password.value == "1234") {
        localStorage.setItem("login", "yes");
        alert("Login Successfully.");
        window.location.href = 'home.html';
    } else {
        alert('Username and password is incorrect.');
    }
}