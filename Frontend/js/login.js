function validate() {
    // Get username and password values
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    // Simple validation check (replace this with actual validation logic)
    if (username === "admin" && password === "sreejith") {
        // Redirect to interface.html if login is successful
        window.location.href = "interface.html";
    } else {
        alert("Invalid username or password. Please try again.");
    }
}
