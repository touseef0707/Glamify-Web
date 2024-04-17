document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('toggleLogin').addEventListener('click', function (event) {
        event.preventDefault();
        window.location.href = '/auth_login';  // Change '/auth_login' to your actual login route
    });
});
