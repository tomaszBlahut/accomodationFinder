function preparePage() {
  $("#meshDensity").val(settings.initialMeshDensity);

  $.ajax({
    url: settings.API_URL + 'shopTypes',
    type: 'GET',
    async: false,
    success: function (response) {
      createWageInputs(response.shops)
    }
  });
}

function createWageInputs(shops) {
  const wagesContainer = $("#wagesContainer");
  wagesContainer.empty();
  shops.forEach(element => {
    const container = $("<div></div>").attr({
      id: element.name,
      class: 'wageContainer'
    });
    $('<span></span>').text(element.name).appendTo(container);
    $('<input type="range"/>').attr({
      name: element.name,
      value: 5,
      class: 'wage mdl-slider mdl-js-slider ',
      min: 0,
      max: 10
    }).appendTo(container);

    wagesContainer.append(container);
  });
}

function showCurrentWageInputs(shops) {
  $(".wageContainer").addClass('hidden');
  shops.forEach(element => {
    $('#' + element.name).removeClass('hidden');
  });
}

function getShopTypes(areaBounds) {
  $.ajax({
    url: settings.API_URL + 'shopTypes',
    type: 'POST',
    data: JSON.stringify(areaBounds),
    contentType: 'application/json',
    async: false,
    success: function (response) {
      showCurrentWageInputs(response.shops)
    }
  });
}

function init() {
  var map = new google.maps.Map(document.getElementById('map-canvas'), {
    center: settings.initialLatLng,
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
    $("#areaBounds").val(JSON.stringify(circle.getBounds().toJSON()));
    getShopTypes(circle.getBounds().toJSON());
  });

  var circle = new google.maps.Circle({
    map: map,
    radius: 0,
    fillColor: '#AA0000',
    editable: true
  });
  circle.bindTo('center', marker, 'position');
  google.maps.event.addListener(circle, 'radius_changed', function () {
    $("#radiusInput").val(circle.getRadius());
    $("#areaBounds").val(JSON.stringify(circle.getBounds().toJSON()));
    getShopTypes(circle.getBounds().toJSON());
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

  marker.setPosition(settings.initialLatLng);
  $("#latitude").val(settings.initialLatLng.lat);
  $("#longitude").val(settings.initialLatLng.lng);
  circle.setRadius(settings.initialRadius);
}
google.maps.event.addDomListener(window, 'load', init);

$(document).ready(preparePage);