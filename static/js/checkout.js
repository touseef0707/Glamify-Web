document.getElementById("use-saved-address").addEventListener("change", function() {
    var savedAddressSection = document.getElementById("saved-address-section");
    var newAddressSection = document.getElementById("new-address-section");
    if (this.checked) {
        savedAddressSection.style.display = "block";
        newAddressSection.style.display = "none";
    } else {
        savedAddressSection.style.display = "none";
        newAddressSection.style.display = "block";
    }
});

document.getElementById("pay").addEventListener("click", function() {
    // Gather all the form data
    var fullname = document.getElementById('fullname').value;
    var phone = document.getElementById('phone').value;
    var address = document.getElementById('address').value;
    var city = document.getElementById('city').value;
    var zipcode = document.getElementById('zipcode').value;

    // Construct the JSON object with all the details
    var formData = {
        fullname: fullname,
        phone: phone,
        address: address,
        city: city,
        zipcode: zipcode
    };

    // Send the data to the /complete_order route in Flask
    fetch("/complete_order", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(formData)
    }).then(function(response) {
        return response.json();
    }
    ).then(function(data) {
        if (data.status == "success") {
            // Redirect the user to the order confirmation page
            window.location.href = "/order_confirmation";
        }
    }
    ).catch(function(error) {
        console.log('Request failed', error);
    });

});

