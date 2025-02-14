function validateLogin(event) {
    event.preventDefault(); // Prevent form submission

    // Get values from the form
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    // Check if the username and password are correct
    if (username === 'amal2003' && password === '123456') {
        // If correct, redirect to the next page (replace 'nextpage.html' with your desired page)
        Window.location.href = 'seatselc.html';
    } else {
        alert('Incorrect username or password. Please try again.');
    }
}
