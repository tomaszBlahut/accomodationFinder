$(document).on("click",
    "#sendButton",
    function send_data() {
        const wages = {};
        $(".wageContainer").each(function() {
            if (!$(this).hasClass('hidden')) {
                const element = $(this).find("input");
                wages[element.attr('name')] = element.val();            
            }
        });
        const prepared_data = JSON.stringify({
            radius: $("#radiusInput").val(),
            start: {
                latitude: $("#latitude").val(),
                longitude: $("#longitude").val()
            },
            wages: wages,
            mesh_density: $("#meshDensity").val(),
            area_bounds: JSON.parse($("#areaBounds").val())
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
    }
);