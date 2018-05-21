function show_shops() {

    const addressField = "Warszawa";
    const shopsInCity = document.getElementById('shopsInCity');
    shopsInCity.innerHTML = "";

    $.ajax({
        url: "http://127.0.0.1:5000/shop/",
        cache: false,
        success: function (responseData) {
            for(let i = 0; i < responseData.length; ++i) {
                const currentShop = responseData[i];
                shopsInCity.innerHTML += "<p>";
                shopsInCity.innerHTML += currentShop[0] + ". ";
                shopsInCity.innerHTML += "<i>" + currentShop[1] + "</i>, ";
                shopsInCity.innerHTML += currentShop[2] + ", ";
                shopsInCity.innerHTML += currentShop[3] + ", ";
                shopsInCity.innerHTML += currentShop[4];
                shopsInCity.innerHTML += "</p>";
            }
        }
    });
}