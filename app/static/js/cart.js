 //import { strict } from "assert";

console.log("THIS IS Cart.js")
$('.btn-items-decrease').on('click', function () {
    url_cart = "/user/cart"

    var input = $(this).siblings('.input-items');
    if (parseInt(input.val(), 10) >= 1) {
        input.val(parseInt(input.val(), 10) - 1); 

    }
});

$('.btn-items-increase').on('click', function () {
    url_cart = "/user/cart"

    var input = $(this).siblings('.input-items');
    input.val(parseInt(input.val(), 10) + 1);

});

function updateQuantity(index) {

    // Create identifier to grab integer value from DOM
    identifier = "#" + index

    // Query that element from the DOM
    updated_quantity = document.getElementById(identifier)

    payload = {
        "item_index": index, 
        "updated_quantity": updated_quantity.value
    }
    console.log(payload)
    url_cart = "/user/cart"

    $.ajax({
        type: 'PUT', 
        url: url_cart, 
        contentType: 'application/json',
        data:JSON.stringify(payload)
    })

    document.location.reload()

}



$('.btn-guest-items-decrease').on('click', function () {
    url_cart = "/cart"

    var input = $(this).siblings('.input-items');
    if (parseInt(input.val(), 10) >= 1) {
        input.val(parseInt(input.val(), 10) - 1); 

    }
});

$('.btn-guest-items-increase').on('click', function () {
    url_cart = "/cart"

    var input = $(this).siblings('.input-items');
    input.val(parseInt(input.val(), 10) + 1);

});


function updateGuestQuantity(index) {
    url = "/update_guest_item"
    // Create identifier to grab integer value from DOM
    identifier = "#" + index
    console.log("HEEEEEERRRRRRRREEEEEEE")
    console.log(identifier)
    console.log("HEEEEEERRRRRRRREEEEEEE")
 
    // Query that element from the DOM
    updated_quantity = document.getElementById(identifier)
    console.log(updated_quantity.value)
    payload = {
        index: index,
        updated_quantity: updated_quantity.value
    }
    console.log(payload)

    $.ajax({
        type: 'PUT', 
        url: url, 
        contentType: 'application/json',
        data:JSON.stringify(payload)
    }).done(function(){
        document.location.reload()
    })
}