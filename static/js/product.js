document.addEventListener('DOMContentLoaded', function() {
    const addToCartButton = document.getElementById('btn-cart');
    
    addToCartButton.addEventListener('click', function(event) {
        // Prevent default form submission behavior
        event.preventDefault();

        // Extract product ID from the data attribute
        const productId = document.querySelector('.quantity').dataset.itemId;
        // Extract selected quantity
        const selectedQuantity = document.querySelector('.quantity').value;
        console.log(productId);
        fetch('/add_to_cart', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                itemId: productId,
                quantity: selectedQuantity // Pass the selected quantity
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to add item to cart');
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            // Optionally, you can perform any additional actions here after adding item to cart
        })
        .catch(error => {
            console.error(error);
        });
    });
});


