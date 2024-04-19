document.querySelectorAll('.cart').forEach(item => {
    item.addEventListener('click', event => {
        event.preventDefault(); // Prevent the default anchor tag behavior
        
        // Get product details from the DOM
        const productElement = item.closest('.product');
        const itemId = productElement.querySelector('input[type="hidden"]').value; // Fetch the product ID from the hidden input field
        // Send data to Flask server via AJAX
        fetch('/add_to_cart', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                itemId: itemId
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
