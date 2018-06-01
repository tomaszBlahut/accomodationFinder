function init() {
  var map = new google.maps.Map(document.getElementById('map-canvas'), {
    center: {
      lat: 50.049683,
      lng: 19.944544
    },
    zoom: 10
  });

  var marker = new google.maps.Marker({
    map: map,
    position: new google.maps.LatLng(50.049683, 19.944544),
    title: 'Search center',
    draggable: true
  });
  google.maps.event.addListener(marker, 'dragend', function () {
    const position = marker.getPosition();  
    $("#latitude").val(position.lat());
    $("#longitude").val(position.lng());
  });

  var circle = new google.maps.Circle({
    map: map,
    radius: 10000,
    fillColor: '#AA0000',
    editable: true
  });
  circle.bindTo('center', marker, 'position');
  google.maps.event.addListener(circle, 'radius_changed', function() {
    $("#radiusInput").val(circle.getRadius());    
  });

  var inputElement = $("#pac-input");
  var searchBox = new google.maps.places.SearchBox(document.getElementById('pac-input'));
  map.controls[google.maps.ControlPosition.TOP_CENTER].push(document.getElementById('pac-input'));
  google.maps.event.addListener(searchBox, 'places_changed', function () {
    searchBox.set('map', null);

    var places = searchBox.getPlaces();
    var bounds = new google.maps.LatLngBounds();
    var i, place;

    for (i = 0; place = places[i]; i++) {
      (function (place) {        
        bounds.extend(place.geometry.location);
      }(place));
    }

    marker.setPosition(bounds.getCenter());

    map.fitBounds(bounds);
    searchBox.set('map', map);
    map.setZoom(Math.min(map.getZoom(), 12));
  });
}
google.maps.event.addDomListener(window, 'load', init);