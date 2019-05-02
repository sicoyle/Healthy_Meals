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

function deleteGuestItem(index) {
    console.log("HERE")
    url = "/delete_guest_cart_item"
    payload = {
        index: index
    }

    $.post(url, payload, function() {
        window.location.reload()
    })
}

function deleteUserItem(index) {
    url = "/delete_user_item"
    payload = {
        index: index
    }

    $.post(url, payload, function() {
        window.location.reload()
    })
}

var user; 

function placeUserOrder(user_id, total) {
    url_number_orders = "/orders/get_next_id"
    url = "/place_user_order"
    user_route = "/user"

    $.post(url, function(data, status) {
        console.log("${data} and status ${status}")
    }); 

    
}