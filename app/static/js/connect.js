console.log("IM HERE!!!")

function toggleModal() {
    $('#chunky_soup_modal').modal('toggle')
    console.log("Inside connect.js")
}

$('#chunky_soup_button').click(function() {
    console.log("Clicked button!")

    url = "/add_cart_item"

    quantity = document.getElementById('quantity_chunky').value

    payload = {
        name: "Thai Coconut Chicken Soup", 
        quantity: quantity,
        id: 11,
        cost: 8, 
        picture_path: "/img/menuPage/chunckysoup.jpg"
    }

    $.post(url, payload, function(data, status) {
        console.log("${data} and status ${status}")
    }); 

    console.log(quantity)
})