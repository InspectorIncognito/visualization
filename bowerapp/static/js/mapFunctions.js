// mapping

/**
 * loads the GTFS options JSON file from carrier/datasantiago static files
 */
function loadGTFSOptions(callback, callback_failed) {

  var filename = '/static/carrier/datasantiago/options.json';
  $.getJSON(filename, function (data) {
      console.log('options data loaded successfully');
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

  var filename = '/static/carrier/datasantiago/busstops.json';
  $.getJSON(filename, function (data) {
      console.log('bus stop data loaded successfully');
      callback(data);
  }).fail(function () {
      console.log("couldn't load bus stop data file.");
      callback_failed();
  });
}