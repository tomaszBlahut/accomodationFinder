$(document).on("click", 
"#sendButton",
function send_data()
{
    var prepared_data = JSON.stringify({
            radius: document.myform.radius_input.value,
            start: {
                    latitude: 50.049683,
                    longitude: 19.944544
                    },
            // wages: {
            //     shop: document.myform.shop_importance.value,
            //     church: document.myform.church_importance.value
            // },
            mesh_density: document.myform.mesh_density.value

        });

    $.ajax({
        url: settings.API_URL+'search',
        type: 'POST',
        data: prepared_data,
        contentType: 'application/json',
        async: false,
        success: function(response) {
            window.location.replace('result/' + response.id);
        }
    });
});