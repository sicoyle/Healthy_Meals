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

function addToCartQuantity(index) {

    // Create identifier to grab integer value from DOM
    identifier = "#" + index

    // Query that element from the DOM
    updated_quantity = document.getElementById(identifier)

    payload = {
        "item_index": index, 
        "updated_quantity": updated_quantity.value
    }

    url_cart = "/user/cart"

    $.post(url_cart, payload, function() {
        console.log("Sent over wire?")
        document.location.reload()

    })


}

// payload = {
//     //     "item_index": index, 
//     //     "updated_quantity": updated_quantity
//     // }

//     // url_cart = "/user/cart"

//     // console.log(updated_quantity)

//     // // $.put(url_cart, payload, function() {
//     // //     console.log("index")
//     // // });
//     // // $.ajax({
//     // //     type: 'PUT', 
//     // //     url: url_cart, 
//     // //     contentType: 'application/json',
//     // //     data:JSON.stringify(payload)
//     // // })