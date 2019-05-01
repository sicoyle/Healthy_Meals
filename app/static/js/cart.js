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

var user; 

function placeUserOrder(user_id, total) {
    url_number_orders = "/orders/get_next_id"
    url = "/place_user_order"
    user_route = "/user"

    var next_order_id = $.get(url_number_orders, function( data ) {
        console.log("DID IT? 1")
    });

    // user = $.get(user_route, function( data ) {
    //     console.log("DID IT? 2")
    // })

    $.ajax({
        dataType: "json", 
        url: user_route
    }).done(function(obj) {
        user = obj
        console.log("USER: ", user["users"][user_id - 1]["items"])
        
        payload = {
            id: next_order_id,
            order_items: user["users"][user_id - 1]["items"],
            cost: total,
            completed: false, 
            user_id: user["users"][user_id - 1]["id"], 
            admin_id: 0
        }
        console.log("USER: ", user["users"][user_id - 1]["items"])
        console.log("PAYLOAD: ", payload)

        $.post(url, payload, function() {
            console.log("DID IT? 3")
        })
    })

    
}