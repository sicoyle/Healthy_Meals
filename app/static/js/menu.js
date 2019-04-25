console.log("IM HERE!!!")

function toggleChunkyModal() {
    $('#chunky_soup_modal').modal('toggle')
    console.log("Inside connect.js")
}

$('#chunky_soup_button').click(function() {
    console.log("Clicked button!")

    url_cart = "/user/cart"
    url_number_items = "/items/get_next_id"

    quantity = document.getElementById('quantity_chunky').value

    var next_item_id = $.get(url_number_items, function( data ) {
        alert( "success" );
    });

    payload = {
        name: "Thai Coconut Chicken Soup", 
        quantity: quantity,
        id: next_item_id,
        cost: 8, 
        picture_path: "img/menuPage/chunckysoup.jpg",
    }

    $.post(url_cart, payload, function(data, status) {
        console.log("${data} and status ${status}")
    }); 

    console.log(quantity)
})

function toggleTomatoModal() {
    $('#tomato_soup_modal').modal('toggle')
    console.log("Inside connect.js")
}

$('#tomato_soup_button').click(function() {
    console.log("Clicked button!")

    url_cart = "/user/cart"
    url_number_items = "/items/get_next_id"

    quantity = document.getElementById('quantity_tomato').value

    var next_item_id = $.get(url_number_items, function( data ) {
        alert( "success" );
    });

    payload = {
        name: "Tomato Basil Soup", 
        quantity: quantity,
        id: next_item_id,
        cost: 8, 
        picture_path: "/img/menuPage/SoupTomato.jpg"
    }

    $.post(url_cart, payload, function(data, status) {
        console.log("${data} and status ${status}")
    }); 

    console.log(quantity)
})

function toggleBlackBeanModal() {
    $('#bean_soup_modal').modal('toggle')
    console.log("Inside connect.js")
}

$('#bean_soup_button').click(function() {
    console.log("Clicked button!")

    url_cart = "/user/cart"
    url_number_items = "/items/get_next_id"

    quantity = document.getElementById('quantity_bean').value

    var next_item_id = $.get(url_number_items, function( data ) {
        alert( "success" );
    });

    payload = {
        name: "Spiced Black Bean Soup", 
        quantity: quantity,
        id: next_item_id,
        cost: 8, 
        picture_path: "/img/menuPage/soupBean.jpg"
    }

    $.post(url_cart, payload, function(data, status) {
        console.log("${data} and status ${status}")
    }); 

    console.log(quantity)
})

function toggleFetaSaladModal() {
    $('#feta_salad_modal').modal('toggle')
    console.log("Inside connect.js")
}

$('#feta_salad_button').click(function() {
    console.log("Clicked button!")

    url_cart = "/user/cart"
    url_number_items = "/items/get_next_id"

    quantity = document.getElementById('quantity_feta').value

    var next_item_id = $.get(url_number_items, function( data ) {
        alert( "success" );
    });

    payload = {
        name: "Chopped Veggie Salad", 
        quantity: quantity,
        id: next_item_id,
        cost: 10, 
        picture_path: "/img/menuPage/SaladFeta.jpg"
    }

    $.post(url_cart, payload, function(data, status) {
        console.log("${data} and status ${status}")
    }); 

    console.log(quantity)
})

function toggleFruitSaladModal() {
    $('#fruit_salad_modal').modal('toggle')
    console.log("Inside connect.js")
}

$('#fruit_salad_button').click(function() {
    console.log("Clicked button!")

    url_cart = "/user/cart"
    url_number_items = "/items/get_next_id"

    quantity = document.getElementById('quantity_fruit').value

    var next_item_id = $.get(url_number_items, function( data ) {
        alert( "success" );
    });

    payload = {
        name: "Field Greens Salad", 
        quantity: quantity,
        id: next_item_id,
        cost: 10, 
        picture_path: "/img/menuPage/saladFruit.jpg"
    }

    $.post(url_cart, payload, function(data, status) {
        console.log("${data} and status ${status}")
    }); 

    console.log(quantity)
})

function toggleLettuceCupsModal() {
    $('#lettuce_cups_modal').modal('toggle')
    console.log("Inside connect.js")
}

$('#lettuce_cups_button').click(function() {
    console.log("Clicked button!")

    url_cart = "/user/cart"
    url_number_items = "/items/get_next_id"

    quantity = document.getElementById('quantity_lettuce_cups').value

    var next_item_id = $.get(url_number_items, function( data ) {
        alert( "success" );
    });

    payload = {
        name: "Butter Lettuce Cups", 
        quantity: quantity,
        id: next_item_id,
        cost: 12, 
        picture_path: "/img/menuPage/lettuceWraps.jpg"
    }

    $.post(url_cart, payload, function(data, status) {
        console.log("${data} and status ${status}")
    }); 

    console.log(quantity)
})

function toggleGnudiModal() {
    $('#gnudi_modal').modal('toggle')
    console.log("Inside connect.js")
}

$('#gnudi_button').click(function() {
    console.log("Clicked button!")

    url_cart = "/user/cart"
    url_number_items = "/items/get_next_id"

    quantity = document.getElementById('quantity_gnudi').value

    var next_item_id = $.get(url_number_items, function( data ) {
        alert( "success" );
    });

    payload = {
        name: "Free Range Chicken Gnudi", 
        quantity: quantity,
        id: next_item_id,
        cost: 12, 
        picture_path: "/img/menuPage/GnudiSquashBox.jpg"
    }

    $.post(url_cart, payload, function(data, status) {
        console.log("${data} and status ${status}")
    }); 

    console.log(quantity)
})

function toggleSalmonCakeModal() {
    $('#salmon_cake_modal').modal('toggle')
    console.log("Inside connect.js")
}

$('#salmon_cake_button').click(function() {
    console.log("Clicked button!")

    url_cart = "/user/cart"
    url_number_items = "/items/get_next_id"

    quantity = document.getElementById('quantity_salmon_cake').value

    var next_item_id = $.get(url_number_items, function( data ) {
        alert( "success" );
    });

    payload = {
        name: "Baked Atlantic Salmon Cakes", 
        quantity: quantity,
        id: next_item_id,
        cost: 12, 
        picture_path: "/img/menuPage/salmonCakes.jpg"
    }

    $.post(url_cart, payload, function(data, status) {
        console.log("${data} and status ${status}")
    }); 

    console.log(quantity)
})

function toggleChickPeaModal() {
    $('#chick_pea_modal').modal('toggle')
    console.log("Inside connect.js")
}

$('#chick_pea_button').click(function() {
    console.log("Clicked button!")

    url_cart = "/user/cart"
    url_number_items = "/items/get_next_id"

    quantity = document.getElementById('quantity_chick_pea').value

    var next_item_id = $.get(url_number_items, function( data ) {
        alert( "success" );
    });

    payload = {
        name: "Moroccan Chick Pea Quinoa Box", 
        quantity: quantity,
        id: next_item_id,
        cost: 12, 
        picture_path: "/img/menuPage/QuinoaBowlBox.jpg"
    }

    $.post(url_cart, payload, function(data, status) {
        console.log("${data} and status ${status}")
    }); 

    console.log(quantity)
})

function toggleCauliflowerModal() {
    $('#cauliflower_box_modal').modal('toggle')
    console.log("Inside connect.js")
}

$('#cauliflower_box_button').click(function() {
    console.log("Clicked button!")

    url_cart = "/user/cart"
    url_number_items = "/items/get_next_id"

    quantity = document.getElementById('quantity_cauliflower_box').value

    var next_item_id = $.get(url_number_items, function( data ) {
        alert( "success" );
    });

    payload = {
        name: "Sweet and Spicy Cauliflower Box", 
        quantity: quantity,
        id: next_item_id,
        cost: 12, 
        picture_path: "/img/menuPage/cauliflowerBox.jpg"
    }

    $.post(url_cart, payload, function(data, status) {
        console.log("${data} and status ${status}")
    }); 

    console.log(quantity)
})

function toggleSouthwestModal() {
    $('#southwest_modal').modal('toggle')
    console.log("Inside connect.js")
}

$('#southwest_button').click(function() {
    console.log("Clicked button!")

    url_cart = "/user/cart"
    url_number_items = "/items/get_next_id"

    quantity = document.getElementById('quantity_southwest').value

    var next_item_id = $.get(url_number_items, function( data ) {
        alert( "success" );
    });

    payload = {
        name: "Southwest Box", 
        quantity: quantity,
        id: next_item_id,
        cost: 12, 
        picture_path: "/img/menuPage/sweetPotBox.jpg"
    }

    $.post(url_cart, payload, function(data, status) {
        console.log("${data} and status ${status}")
    }); 

    console.log(quantity)
})

function toggleProteinBarModal() {
    $('#protein_bar_modal').modal('toggle')
    console.log("Inside connect.js")
}

$('#protein_bar_button').click(function() {
    console.log("Clicked button!")

    url_cart = "/user/cart"
    url_number_items = "/items/get_next_id"

    quantity = document.getElementById('quantity_protein_bar').value

    var next_item_id = $.get(url_number_items, function( data ) {
        alert( "success" );
    });

    payload = {
        name: "Chocolate Almond Protein Bar", 
        quantity: quantity,
        id: next_item_id,
        cost: 8, 
        picture_path: "/img/menuPage/granola.jpg"
    }

    $.post(url_cart, payload, function(data, status) {
        console.log("${data} and status ${status}")
    }); 

    console.log(quantity)
})

function toggleSconeModal() {
    $('#scone_modal').modal('toggle')
    console.log("Inside connect.js")
}

$('#scone_button').click(function() {
    console.log("Clicked button!")

    url_cart = "/user/cart"
    url_number_items = "/items/get_next_id"

    quantity = document.getElementById('quantity_scone').value

    var next_item_id = $.get(url_number_items, function( data ) {
        alert( "success" );
    });

    payload = {
        name: "Lemon Blueberry Scone", 
        quantity: quantity,
        id: next_item_id,
        cost: 8, 
        picture_path: "/img/menuPage/blueberryScone.jpg"
    }

    $.post(url_cart, payload, function(data, status) {
        console.log("${data} and status ${status}")
    }); 

    console.log(quantity)
})

function toggleBrownieModal() {
    $('#brownie_modal').modal('toggle')
    console.log("Inside connect.js")
}

$('#brownie_button').click(function() {
    console.log("Clicked button!")

    url_cart = "/user/cart"
    url_number_items = "/items/get_next_id"

    quantity = document.getElementById('quantity_brownie').value

    var next_item_id = $.get(url_number_items, function( data ) {
        alert( "success" );
    });

    payload = {
        name: "Chocolate Hazelnut Brownie", 
        quantity: quantity,
        id: next_item_id,
        cost: 8, 
        picture_path: "/img/menuPage/brownies.jpg"
    }

    $.post(url_cart, payload, function(data, status) {
        console.log("${data} and status ${status}")
    }); 

    console.log(quantity)
})

function toggleBeatJuiceModal() {
    $('#beat_juice_modal').modal('toggle')
    console.log("Inside connect.js")
}

$('#beat_juice_button').click(function() {
    console.log("Clicked button!")

    url_cart = "/user/cart"
    url_number_items = "/items/get_next_id"

    quantity = document.getElementById('quantity_beat_juice').value

    var next_item_id = $.get(url_number_items, function( data ) {
        alert( "success" );
    });

    payload = {
        name: "Cold Beat Down Juice", 
        quantity: quantity,
        id: next_item_id,
        cost: 6, 
        picture_path: "/img/menuPage/BeatDownSmoothie.jpg"
    }

    $.post(url_cart, payload, function(data, status) {
        console.log("${data} and status ${status}")
    }); 

    console.log(quantity)
})

function toggleChocolateBombeModal() {
    $('#chocolate_bombe_modal').modal('toggle')
    console.log("Inside connect.js")
}

$('#chocolate_bombe_button').click(function() {
    console.log("Clicked button!")

    url_cart = "/user/cart"
    url_number_items = "/items/get_next_id"

    quantity = document.getElementById('quantity_chocolate_bombe').value

    var next_item_id = $.get(url_number_items, function( data ) {
        alert( "success" );
    });

    payload = {
        name: "Chocolate Almond Bombe", 
        quantity: quantity,
        id: next_item_id,
        cost: 6, 
        picture_path: "/img/menuPage/chocolateBombe.jpg"
    }

    $.post(url_cart, payload, function(data, status) {
        console.log("${data} and status ${status}")
    }); 

    console.log(quantity)
})

function toggleKaleSmoothieModal() {
    $('#kale_smoothie_modal').modal('toggle')
    console.log("Inside connect.js")
}

$('#kale_smoothie_button').click(function() {
    console.log("Clicked button!")

    url_cart = "/user/cart"
    url_number_items = "/items/get_next_id"

    quantity = document.getElementById('quantity_kale_smoothie').value

    var next_item_id = $.get(url_number_items, function( data ) {
        alert( "success" );
    });

    payload = {
        name: "Chocolate Kale Smoothie", 
        quantity: quantity,
        id: next_item_id,
        cost: 6, 
        picture_path: "/img/menuPage/ChocolateKaleSmoothie.jpg"
    }

    $.post(url_cart, payload, function(data, status) {
        console.log("${data} and status ${status}")
    }); 

    console.log(quantity)
})

function toggleTropicalSmoothieModal() {
    $('#tropical_smoothie_modal').modal('toggle')
    console.log("Inside connect.js")
}

$('#tropical_smoothie_button').click(function() {
    console.log("Clicked button!")

    url_cart = "/user/cart"
    url_number_items = "/items/get_next_id"

    quantity = document.getElementById('quantity_tropical_smoothie').value

    var next_item_id = $.get(url_number_items, function( data ) {
        alert( "success" );
    });

    payload = {
        name: "Tropical Blast Smoothie", 
        quantity: quantity,
        id: next_item_id,
        cost: 6, 
        picture_path: "/img/menuPage/tropicalSmoothie.jpg"
    }

    $.post(url_cart, payload, function(data, status) {
        console.log("${data} and status ${status}")
    }); 

    console.log(quantity)
})

function toggleElderberryModal() {
    $('#elderberry_modal').modal('toggle')
    console.log("Inside connect.js")
}

$('#elderberry_button').click(function() {
    console.log("Clicked button!")

    url_cart = "/user/cart"
    url_number_items = "/items/get_next_id"

    quantity = document.getElementById('quantity_elderberry').value

    var next_item_id = $.get(url_number_items, function( data ) {
        alert( "success" );
    });

    payload = {
        name: "Elderberry", 
        quantity: quantity,
        id: next_item_id,
        cost: 6, 
        picture_path: "/img/menuPage/elderBerryElixir.jpg"
    }

    $.post(url_cart, payload, function(data, status) {
        console.log("${data} and status ${status}")
    }); 

    console.log(quantity)
})

function togglePineappleElixirModal() {
    $('#pineapple_elixir_modal').modal('toggle')
    console.log("Inside connect.js")
}

$('#pineapple_elixir_button').click(function() {
    console.log("Clicked button!")

    url_cart = "/user/cart"
    url_number_items = "/items/get_next_id"

    quantity = document.getElementById('quantity_pineapple_elixir').value

    var next_item_id = $.get(url_number_items, function( data ) {
        alert( "success" );
    });

    payload = {
        name: "Pineapple", 
        quantity: quantity,
        id: next_item_id,
        cost: 6, 
        picture_path: "/img/menuPage/pineappleElixir.jpg"
    }

    $.post(url_cart, payload, function(data, status) {
        console.log("${data} and status ${status}")
    }); 

    console.log(quantity)
})

function toggleMixedBerryModal() {
    $('#mixed_berry_modal').modal('toggle')
    console.log("Inside connect.js")
}

$('#mixed_berry_button').click(function() {
    console.log("Clicked button!")

    url_cart = "/user/cart"
    url_number_items = "/items/get_next_id"

    quantity = document.getElementById('quantity_mixed_berry').value

    var next_item_id = $.get(url_number_items, function( data ) {
        alert( "success" );
    });

    payload = {
        name: "Mixed Berry", 
        quantity: quantity,
        id: next_item_id,
        cost: 6, 
        picture_path: "/img/menuPage/mixedBerryElixir.jpg"
    }

    $.post(url_cart, payload, function(data, status) {
        console.log("${data} and status ${status}")
    }); 

    console.log(quantity)
})
