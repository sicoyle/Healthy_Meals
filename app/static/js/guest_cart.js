function deleteItem(index) {
    console.log("Index", index)
    url = "/delete_guest_cart_item"
    payload = {
        index: index
    }

    $.post(url, payload, function() {
        document.location.reload()
    })
}