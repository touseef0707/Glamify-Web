// Add event listener to the table container
document.querySelector('.table-container').addEventListener('wheel', function(event) {
    var deltaY = event.deltaY;
    var table = document.querySelector('.table');
    var isTableScrolledToTop = table.scrollTop === 0;
    var isTableScrolledToBottom = table.scrollHeight - table.clientHeight === table.scrollTop;

    if ((deltaY < 0 && isTableScrolledToTop) || (deltaY > 0 && isTableScrolledToBottom)) {
        event.stopPropagation(); // Stop propagation to prevent body scrolling
    }
});

var currentUrl = window.location.pathname;

// Get all navigation links
var navLinks = document.querySelectorAll('#navbar li');

// Loop through each navigation link
navLinks.forEach(function(link) {
    // Compare the href attribute with the current URL
    if (link.getAttribute('href') === currentUrl) {
        // Add the 'active' class if the href matches the current URL
        link.classList.add('active');
        }
});