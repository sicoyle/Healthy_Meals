const Http = new XMLHttpRequest()
const url = 'http://localhost:8080/food'

payload = {
    category: "MyDankasssalad", 
    cost: 99, 
    iconPath: "", 
    id: 25, 
    ingredients: [], 
    name: "Brents Salad", 
    withInformation: "Brents salad with love", 
    picturePath: "img/fake/image.jpg"
}

$('.btn').click(function() {
    console.log("Clicked button!")
    $.post(url, payload, function(data, status) {
        console.log('${data} and status ${status}')
    }); 
})