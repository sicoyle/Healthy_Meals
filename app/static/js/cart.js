$('.btn-items-decrease').on('click', function () {
    var input = $(this).siblings('.input-items');
    if (parseInt(input.val(), 10) >= 1) {
        input.val(parseInt(input.val(), 10) - 1);
    }
});

$('.btn-items-increase').on('click', function () {
    var input = $(this).siblings('.input-items');
    input.val(parseInt(input.val(), 10) + 1);
});

function deleteGuestItem(index) {
    
    url = "/delete_guest_item"
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

function placeUserOrder(user_items) {
    url = "/place_user_order"

    console.log()

    first_name = $("#user_first_name").val()
    last_name = $("#user_last_name").val()
    address = $("#user_address").val()

    payload = {
        first_name: first_name, 
        last_name: last_name,
        address: address    
    }

    $.post(url, payload, function() {
        console.log("DID IT?")
    })
}