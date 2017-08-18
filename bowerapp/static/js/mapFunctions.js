"use strict";
// mapping

/**
 * loads the GTFS options JSON file from carrier/datasantiago static files
 */
function loadGTFSOptions(callback, callback_failed) {

  var filename = "/static/carrier/datasantiago/options.json";
  $.getJSON(filename, function (data) {
      console.log("options data loaded successfully");
      callback(data);
  }).fail(function () {
      console.log("couldn't load options file.");
      callback_failed();
  });
}

/**
 * loads the GTFS options BusStops file from carrier/datasantiago static files
 */
function loadGTFSBusStops(callback, callback_failed) {

  var filename = "/static/carrier/datasantiago/busstops.json";
  $.getJSON(filename, function (data) {
      console.log("bus stop data loaded successfully");
      callback(data);
  }).fail(function () {
      console.log("couldn't load bus stop data file.");
      callback_failed();
  });
}

// bus stop marker
var bus_stop_icon = L.icon({
    iconUrl: "/static/carrier/images/paradero.png",
    shadowUrl: null,

    iconSize:     [32, 48], // size of the icon
    shadowSize:   [ 0,  0], // size of the shadow
    iconAnchor:   [16, 48], // point of the icon which will correspond to marker"s location
    shadowAnchor: [ 0,  0],  // the same for the shadow
    popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
});

// user marker
var user_icon = L.icon({
    iconUrl: "/static/carrier/images/usuario.png",
    shadowUrl: null,

    iconSize:     [30, 38], // size of the icon
    shadowSize:   [ 0,  0], // size of the shadow
    iconAnchor:   [15, 38], // point of the icon which will correspond to marker"s location
    shadowAnchor: [ 0,  0],  // the same for the shadow
    popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
});