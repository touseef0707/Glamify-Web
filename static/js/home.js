document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('toggleRegister').addEventListener('click', function (event) {
        event.preventDefault();
        window.location.href = '/auth_register';  // Change '/auth_register' to your actual registration route
    });
});

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('toggleLogin').addEventListener('click', function (event) {
        event.preventDefault();
        window.location.href = '/auth_login';  // Change '/auth_login' to your actual login route
    });
});

function adjustMinMaxDates() {
    var dobMonth = document.getElementById('dobMonth').value;
    var dobYear = document.getElementById('dobYear').value;
    var dobDay = document.getElementById('dobDay');

    var maxDay = 31; // Default maximum day

    // Adjust the maximum day based on the selected month
    if (dobMonth === '4' || dobMonth === '6' || dobMonth === '9' || dobMonth === '11') {
        maxDay = 30;
    } else if (dobMonth === '2') {
        // Check for February and adjust for leap years
        if ((dobYear % 4 == 0 && dobYear % 100 != 0) || dobYear % 400 == 0) {
            maxDay = 29; // Leap year
        } else {
            maxDay = 28; // Non-leap year
        }
    }

    // Set the maximum and minimum attributes of the day input field
    dobDay.setAttribute('min', 1);
    dobDay.setAttribute('max', maxDay);
}

// Attach the adjustMinMaxDates function to the change event of month and year inputs
document.getElementById('dobMonth').addEventListener('change', adjustMinMaxDates);
document.getElementById('dobYear').addEventListener('change', adjustMinMaxDates);

// Call the function initially to set the correct min and max values
adjustMinMaxDates();



function removeCartItem(button) {
    var item = button.parentNode;
    var row = item.parentNode;
    row.parentNode.removeChild(row);
}


function decrementQuantity(button) {
    var quantityElement = button.nextElementSibling;
    var currentQuantity = parseInt(quantityElement.innerText);
    if (currentQuantity > 1) {
        quantityElement.innerText = currentQuantity - 1;
        updateTotalPrice(button.parentElement.parentElement);
    }
}

function incrementQuantity(button) {
    var quantityElement = button.previousElementSibling;
    var currentQuantity = parseInt(quantityElement.innerText);
    quantityElement.innerText = currentQuantity + 1;
    updateTotalPrice(button.parentElement.parentElement);
}

function updateTotalPrice(row) {
    var priceCell = row.querySelector('td:nth-child(4) p').innerText;
    var quantity = parseInt(row.querySelector('.quantity').innerText);
    var totalPriceCell = row.querySelector('td:nth-child(6) p');
    var price = parseFloat(priceCell.substring(1)); // Remove '$' and parse as float
    var totalPrice = price * quantity;
    totalPriceCell.innerText = '$' + totalPrice.toFixed(2); // Update total price with 2 decimal places
}

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