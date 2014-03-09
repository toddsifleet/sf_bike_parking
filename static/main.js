$(function() {
  var clearMap  = function() {
    current_info_window && current_info_window.close();
    directions.display.setMap(null);
  };

  var flashError = function(message) {
    // TODO: Show user a message
    console.log(message);
  };

  var addMarker = function(spot, icon) {
    if (markers[spot.id]) return;
    var position = spot.coords || new google.maps.LatLng(
      spot.latitude,
      spot.longitude
    );
    return markers[spot.id] = new google.maps.Marker({
      map: map,
      position: position,
      icon: icon
    });
  };

  var drawDirections = function(spot) {
    var request = {
      travelMode: 'BICYCLING',
      origin: current_position.coords,
      destination: new google.maps.LatLng(
        spot.latitude,
        spot.longitude
      )
    };
    directions.service.route(request, function(response, status) {
      if (status == google.maps.DirectionsStatus.OK) {
        directions.display.setMap(map);
        directions.display.setDirections(response);
      }
      else {
        flashError(status);
      }
    });
  }

  var drawInfoWindow = function(marker, spot) {
    console.log(current_position.coords);
    current_info_window = new google.maps.InfoWindow({
      content: Mustache.render(popup_template, {
        spot: spot,
        current: current_position.coords
      })
    });
    google.maps.event.addListener(current_info_window, 'closeclick', clearMap);
    drawDirections(spot);
    current_info_window.open(map, marker);
  }

  var drawParkingSpot = function(spot) {
    var marker = addMarker(spot);
    if (!marker) return;

    google.maps.event.addListener(marker, 'click', function() {
      clearMap();
      $.get('/spots/' +  spot.id, function(spot, status) {
        if (status != 'success') {
          return flashError('Could not load space information');
        }
        drawInfoWindow(marker, spot);
      });
    });
  }

  var updateParkingSpots = function(data, status) {
    if (status != 'success') {
      return flashError('Could not oad parking spots from server');
    }
    for (var i in data.result) {
      drawParkingSpot(data.result[i]);
    }
  }

  var updateCurrentPosition = function(position) {
    if (markers['current_position']) {
      markers['current_position'].setMap(null);
      delete markers['current_position'];
    }
    current_position = {
      id: 'current_position',
      coords: new google.maps.LatLng(
        position.d,
        position.e
      )
    };
    addMarker(current_position,
      'http://maps.google.com/mapfiles/kml/pal4/icon47.png'
    );

  };

  var updateMap = function(position) {
    $('#loading-animation').hide();
    map.setCenter(position);
    updateCurrentPosition(position);
  }

  var onUserInput = function() {
    closeInfoWindow();
    var data = { 'address': $('#address').val() };
    geocoder.geocode(data, function(results, status) {
      if (status === google.maps.GeocoderStatus.OK) {
        updateMap(results[0].geometry.location);
      }
      else {
        flashError(status)
      }
    });
  }

  var onPositionCoords = function(position) {
    position = new google.maps.LatLng(
      position.coords.latitude,
      position.coords.longitude
    );

    updateMap(position);
    geocoder.geocode({'latLng': position}, function(results, status) {
      if (status === google.maps.GeocoderStatus.OK) {
        $('#address').val(results[1].formatted_address);
      }
      else {
        flashError(status);
      }
    });
  }

  var initDefaults = function() {
    if (!navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(onPositionCoords);
    }
    else {
      onPositionCoords({
        coords: {
          latitude: 37.7908906,
          longitude: -122.3930944
        }
      })
    }
  }

  var initMap = function() {
    var mapOptions = {
      zoomControl: false,
      streetViewControl: false,
      panControl: false,
      mapTypeControl: false,
      zoom: 18
    };

    map = new google.maps.Map(
      document.getElementById('map-canvas'),
      mapOptions
    );

    google.maps.event.addListener(map, 'bounds_changed', function() {
      var bounds = map.getBounds().toUrlValue()
      $.get('/spots/bounds', { bounds: bounds }, updateParkingSpots);
    });

    $(document).on('click', "a.direction", drawDirections);
  }

  var initUserInput = function() {
    var address_input = $('#address');
    address_input.keyup(function(e) {
      var code = e.keyCode || e.which;
      if (code == 13) onUserInput();
    })

    address_input.on('focus', function (argument) {
      address_input.unbind('focus');
      address_input.val('');
    });
  }

  var initDirections = function() {
    return {
      service: new google.maps.DirectionsService(),
      display: new google.maps.DirectionsRenderer()
    };
  }

  var current_position,
    current_info_window,
    geocoder = new google.maps.Geocoder(),
    map,
    markers = {},
    popup_template = $('#popup-template').html();
    directions = initDirections();

  initMap(),
  initDefaults();
  initUserInput();
});


