function send_data()
{
    var prepared_data = {
            radius: document.myform.radius_input.value,
            start: {
                    latitude: 50.049683,
                    longitude: 19.944544
                    },
            wages: {
                shop: document.myform.shop_importance.value,
                church: document.myform.church_importance.value
            },
            mesh_density: document.myform.mesh_density.value


        };

    $.ajax({
        url: 'http://127.0.0.1:5000/',
        type: 'POST',

        data: prepared_data,
        contentType: 'application/json; charset=utf-8',
        dataType: 'JSON',
        async: false,
        success: function(data) {
            alert(data);
        }
    });


}