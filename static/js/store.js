// JavaScript code to handle clicking the cart anchor tag
document.querySelectorAll('.cart').forEach(item => {
    item.addEventListener('click', event => {
        event.preventDefault(); // Prevent the default anchor tag behavior
        
        // Get product details from the DOM
        const productElement = item.closest('.product');// Get product details from the DOM
        const itemId = document.getElementById('itemid').value;
        const itemName = productElement.querySelector('.description h5').textContent;
        const itemPrice = productElement.querySelector('.description h4').textContent.replace('AED ', ''); // Remove 'AED ' prefix
        console.log(itemId, itemName, itemPrice);
        // Send data to Flask server via AJAX
        fetch('/add_to_cart', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                itemId: itemId,
                itemName: itemName,
                itemPrice: itemPrice
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to add item to cart');
            }
            return response.json();
        })
        .then(data => {
            console.log(data); // Log success message or handle accordingly
        })
        .catch(error => {
            console.error(error); // Log error message or handle accordingly
        });
    });
});
