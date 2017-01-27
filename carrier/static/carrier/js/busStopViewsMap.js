
$(function () {
    $('#date_init').datetimepicker({
        defaultDate: moment().subtract(1, 'months'),
        format: 'LL'
    });
    $('#date_end').datetimepicker({
        defaultDate: moment(),
        format: 'LL'
    });
    $("#filters").on("dp.change", function () {
        loadData();
    });
    $("#toggle-button").change(function () {
        loadData();
    })
});


$(document).ready(function () {
    createMap();
});

var map;
var gtfs_bus_stops;
function createMap() {
    var santiagoLocation = L.latLng(-33.459229, -70.645348);
    map = L.map("map_id").setView(santiagoLocation, 12);

    function loadDefaultMapboxTiles(options) {
        L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/256/{z}/{x}/{y}?access_token={accessToken}', {
            attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, Imagery © <a href="http://mapbox.com">Mapbox</a>',
            maxZoom: 18,
            accessToken: options.token
        }).addTo(map);
    }
    loadGTFSBusStops(function (data) {
        gtfs_bus_stops = data;
        loadData();
        loadGTFSOptions(loadDefaultMapboxTiles, null);
    }, null);
}


var user_icon = L.icon({
    iconUrl: '/static/carrier/images/usuario.png',
    shadowUrl: null,

    iconSize:     [30, 38], // size of the icon
    shadowSize:   [ 0,  0], // size of the shadow
    iconAnchor:   [15, 38], // point of the icon which will correspond to marker's location
    shadowAnchor: [ 0,  0],  // the same for the shadow
    popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
});

var cur_markers = [];
function drawUserView(lat, lon) {
    var view_lat_lng = L.latLng(lat, lon);
    var view_marker = L.marker(view_lat_lng, {icon: user_icon}).addTo(map);
    cur_markers.push(view_marker);
}

// # http://localhost/carriers/getUsersPositions/?date_init=2016-10-24T00:00:00&date_end=2017-01-25T00:00:00&_=1485262643655
// # {
// #   "9142b237-074c-4282-aaea-c586447087ac": [
// #       {"lat": -33.4382809, "timeStamp": "2016-10-26T22:17:45.363Z", "lon": -70.5732056},
// #       {"lat": -33.4391086, "timeStamp": "2016-10-26T22:18:22.036Z", "lon": -70.5726174},
// #       ...
function loadData() {
    var data_url = 'http://' + location.host + '/carriers/getUsersPositions/';
    var data = {
        date_init: $('#date_init').data("DateTimePicker").date().format("YYYY-MM-DD") + "T00:00:00",
        date_end: $('#date_end').data("DateTimePicker").date().add(1, 'days').format("YYYY-MM-DD") + "T00:00:00"
    };

    console.log("Retrieving data from: " + data_url);
    $.getJSON(data_url, data)
        .done(function (data) {
            // console.log("... data retrieved");

            cur_markers.forEach(function (item, idx) {
                item.remove();
            });

            var n_users = 0;
            var loadFromFirst = document.getElementById("toggle-button").checked;
            for (var user_id in data) {
                var user_data = data[user_id];
                var datum = user_data.first;
                if (!loadFromFirst && user_data.hasOwnProperty("last")) {
                    datum = user_data.last;
                }
                drawUserView(datum.lat, datum.lon);
                n_users++;
            }
            console.log("Loaded " + n_users + " bus stop views");

            console.log("... done. Stopping spinner");
            spinner.stop();
        });
}
