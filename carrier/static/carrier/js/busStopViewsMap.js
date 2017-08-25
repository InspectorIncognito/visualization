
$(document).ready(function () {
    var SPINNER_TARGET = document.getElementsByClassName("x_panel")[0];

    var TOGGLE_INPUT = $("#toggle-button");
    var DATE_RANGE_INPUT = $("#dateRange");

    DATE_RANGE_INPUT.daterangepicker(optionDateRangePicker);
    DATE_RANGE_INPUT.on("apply.daterangepicker", function(){
        loadData();
    });
    TOGGLE_INPUT.change(function () {
        loadData();
    });

    var map;
    var gtfs_bus_stops;

    function createMap() {
        var santiagoLocation = L.latLng(-33.459229, -70.645348);
        map = L.map("map_id").setView(santiagoLocation, 12);

        function loadDefaultMapboxTiles(options) {
            var mapboxURL = "https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/256/{z}/{x}/{y}?access_token={accessToken}";
            var attribution = "Map data &copy; <a href='http://openstreetmap.org'>OpenStreetMap</a> contributors, Imagery © <a href='http://mapbox.com'>Mapbox</a>";
            L.tileLayer(mapboxURL, {
                attribution: attribution,
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
    createMap();

    var cur_markers = [];
    function drawUserView(lat, lon) {
        var view_lat_lng = L.latLng(lat, lon);
        var view_marker = L.marker(view_lat_lng, {icon: user_icon}).addTo(map);
        cur_markers.push(view_marker);
    }

    function loadData() {
        var data_url = "/carriers/getUsersPositions/";
        var data = {
            date_init: DATE_RANGE_INPUT.data("daterangepicker").startDate.format(),
            date_end: DATE_RANGE_INPUT.data("daterangepicker").endDate.format()
        };

        //console.log("Retrieving data from: " + data_url);
        $(SPINNER_TARGET).spin(spinnerOpt);
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
            }).always(function(){
                $(SPINNER_TARGET).spin(false);
            });
    }
});
