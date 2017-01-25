/**
 * Created by mpavez on 17-01-17.
 */

var spinner_options = {
  lines: 7 // The number of lines to draw
, length: 25 // The length of each line
, width: 15 // The line thickness
, radius: 30 // The radius of the inner circle
, scale: 0.8 // Scales overall size of the spinner
, corners: 1 // Corner roundness (0..1)
, color: 'rgb(42, 63, 84)' // #rgb or #rrggbb or array of colors
, opacity: 0.05 // Opacity of the lines
, rotate: 0 // The rotation offset
, direction: 1 // 1: clockwise, -1: counterclockwise
, speed: 1 // Rounds per second
, trail: 75 // Afterglow percentage
, fps: 20 // Frames per second when using setTimeout() as a fallback for CSS
, zIndex: 2e9 // The z-index (defaults to 2000000000)
, className: 'spinner' // The CSS class to assign to the spinner
, top: '50%' // Top position relative to parent
, left: '50%' // Left position relative to parent
, shadow: false // Whether to render a shadow
, hwaccel: false // Whether to use hardware acceleration
, position: 'absolute' // Element positioning
};

var spinner = new Spinner(spinner_options)
    .spin(document.getElementById('right_col_page_content'));


// Data exports
var exportButtonCommon = {
    exportOptions: {
        // format: {
        //     body: function (data, row, column, node) {
        //         // row: row number
        //         // column: column number
        //         // node: cell DOM node: <td>, <td class="text-center">, ...
        //         // data:
        //         return data;
        //     }
        // },
        orthogonal: 'export'
    }
};


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