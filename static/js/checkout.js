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
    
});

