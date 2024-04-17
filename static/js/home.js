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