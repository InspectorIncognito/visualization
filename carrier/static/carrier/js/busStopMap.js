
$(function () {
    $('#date_init').datetimepicker({
        defaultDate: moment().subtract(1, 'months'),
        format: 'LL'
    });
    $('#date_end').datetimepicker({
        defaultDate: moment(),
        format: 'LL'
    });
    $("#filters").on("dp.change", function (e) {
        loadData();
    });
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


// bus stop icon
var bus_stop_icon = L.icon({
    iconUrl: '/static/carrier/images/paradero.png',
    shadowUrl: null,

    iconSize:     [32, 48], // size of the icon
    shadowSize:   [ 0,  0], // size of the shadow
    iconAnchor:   [16, 48], // point of the icon which will correspond to marker's location
    shadowAnchor: [ 0,  0],  // the same for the shadow
    popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
});

var cur_markers = {};
function drawBusStop(code, name, lat, lon, services, app_data) {
    var bus_stop_lat_lng = L.latLng(lat, lon);
    var bus_stop_marker = L.marker(bus_stop_lat_lng, {icon: bus_stop_icon}).addTo(map);

    // 'eventCount'
    // 'confirmCount'
    // 'declineCount'
    // 'busStopCheckCount'
    bus_stop_marker.bindPopup(
        "<b>" + code + " - " + name + "</b>" +
        "<br>" +
        "<p>Servicios: " + services + "</p> " +
        "<ul>" +
            "<li>Eventos: " + app_data.eventCount + "</li>" +
            "<li>Confirmados: " + app_data.confirmCount + "</li>" +
            "<li>Rechazados: " + app_data.declineCount + "</li>" +
            "<li>Vistas: " + app_data.busStopCheckCount + "</li>" +
        "</ul>"
    );
    // if (app_data.busStopCheckCount > 0) {
    //     console.log("VISTAS:" + app_data.busStopCheckCount);
    //     console.log("- name:" + name);
    //     console.log("- code:" + code);
    // }
    cur_markers[code] = bus_stop_marker;
}

function loadData() {
    var data_url = 'http://' + location.host + '/carriers/getBusStopInfo/';
    var data = {
        date_init: $('#date_init').data("DateTimePicker").date().format("YYYY-MM-DD") + "T00:00:00",
        date_end: $('#date_end').data("DateTimePicker").date().add(1, 'days').format("YYYY-MM-DD") + "T00:00:00"
    };

    console.log("Retrieving data from: " + data_url);
    $.getJSON(data_url, data)
        .done(function (data) {
            // console.log("... data retrieved");

            // console.log("... drawing");
            var i = 0;

            // remove old markers
            for (var marker_code in cur_markers) {
                // // only removes unused markers
                // if (!data.hasOwnProperty(marker_code))  {
                //     // console.log("Marker to be removed: " + marker_code);
                //     cur_markers[marker_code].remove();
                //     delete cur_markers[marker_code];
                // }

                // remove all
                cur_markers[marker_code].remove();
                delete cur_markers[marker_code];
            }

            for (var bus_stop_code in data) {
                if (!gtfs_bus_stops.hasOwnProperty(bus_stop_code)) {
                    console.warn("Unknown bus stop code: " + bus_stop_code);
                    continue;
                }

                var app_data = data[bus_stop_code];
                var bus_stop = gtfs_bus_stops[bus_stop_code];
                drawBusStop(
                    bus_stop_code,
                    bus_stop.name,
                    bus_stop.latitude,
                    bus_stop.longitude,
                    bus_stop.services,
                    app_data
                );
                i++;
            }
            console.log("Loaded " + i + " bus stop markers");

            // console.log("... done. Stopping spinner");
            spinner.stop();
        });
}
