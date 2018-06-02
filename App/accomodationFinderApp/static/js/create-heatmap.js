function createHeatMap(response) {
    const requestParameters = JSON.parse(response.request_params);
    const results = JSON.parse(response.result);
    const latitudes = results.latitudes;
    const longitudes = results.longitudes;
    const weights = results.values;
    const latStep = results.latitude_step;
    const lngStep = results.longitude_step;    

    const map = new google.maps.Map(document.getElementById('map-canvas'), {
        center: new google.maps.LatLng(requestParameters.start.latitude, requestParameters.start.longitude),
        zoom: 12
    });    

    for (let i = 0; i < results.mesh_density; i++) {
        for (let j = 0; j < results.mesh_density; j++) {
            const currentWeight = weights[i][j];
            let opacityAdd = 0.5 - Math.pow(currentWeight, 1/3);
            opacityAdd = opacityAdd > 0 ? opacityAdd : 0;
            const color = numberToColorHsl(currentWeight, 0, 1.0);
            const rectangle = new google.maps.Rectangle({
                strokeWeight: 0,
                fillColor: color,
                fillOpacity: 0.5 + opacityAdd,
                map: map,
                bounds: {
                    north: latitudes[i],
                    south: latitudes[i] + latStep,
                    west: longitudes[j],
                    east: longitudes[j] + lngStep
                },
                clickable: false
            });
        }
    }

    const sw = new google.maps.LatLng("" + requestParameters.area_bounds.south, "" + requestParameters.area_bounds.west);
    const ne = new google.maps.LatLng(requestParameters.area_bounds.north, requestParameters.area_bounds.east);
    const bounds = new google.maps.LatLngBounds(sw, ne);

    map.fitBounds(bounds, 0);
}