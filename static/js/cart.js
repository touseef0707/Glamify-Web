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