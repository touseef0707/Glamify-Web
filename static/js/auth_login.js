
document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('toggleRegister').addEventListener('click', function (event) {
        event.preventDefault();
        window.location.href = '/auth_register';  // Change '/auth_register' to your actual registration route
    });
});