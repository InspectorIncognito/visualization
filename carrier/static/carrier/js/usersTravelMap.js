
document.getElementById("toggle-button").checked = true;
document.getElementById("checkbox-distance-0").checked = false; // outliers?
document.getElementById("checkbox-distance-1").checked = true;
document.getElementById("checkbox-distance-2").checked = true;
document.getElementById("checkbox-distance-3").checked = true;

$(function () {
    $('#date_init')
        .datetimepicker({
            defaultDate: moment().subtract(1, 'months').subtract(15, 'days'),
            format: 'LL'
        })
        .on("dp.change", function () {
            resetCurData();
            loadData();
        });
    $('#date_end')
        .datetimepicker({
            defaultDate: moment(),
            format: 'LL'
        })
        .on("dp.change", function () {
            resetCurData();
            loadData();
        });
    $("#toggle-button").change(function () {
        redrawData();
    });

    $("#checkbox-distance-0").change(function () {
        redrawData();
    });
    $("#checkbox-distance-1").change(function () {
        redrawData();
    });
    $("#checkbox-distance-2").change(function () {
        redrawData();
    });
    $("#checkbox-distance-3").change(function () {
        redrawData();
    });
});


$(document).ready(function () {
    createMap();
});

var map;
var gtfs_bus_stops;
var info_div;
var info_div_single;
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

    info_div = L.control();
    info_div.onAdd = function (map) {
        this._div = L.DomUtil.create('div', 'info_div'); // create a div with a class "info"
        return this._div;
    };

    // method that we will use to update the control based on feature properties passed
    info_div.update = function (props) {

        if (props.n == 0) {
            this._div.innerHTML = '<h4>Sin Información</h4>'
            return;
        }

        var n_str;
        if (props.n == 1) { n_str = "1 viaje"; }
        else { n_str = props.n + " viajes"; }

        var min_dist_str, max_dist_str;
        if (props.min_dist < 1000) { min_dist_str = Number(props.min_dist).toFixed(0) + " mts"; }
        else { min_dist_str = Number(props.min_dist/1000).toFixed(1) + " kms"; }
        if (props.max_dist < 1000) { max_dist_str = Number(props.max_dist).toFixed(0) + " mts"; }
        else { max_dist_str = Number(props.max_dist/1000).toFixed(1) + " kms"; }

        var min_time_str, max_time_str;
        if (props.min_time < 60) { min_time_str = Number(props.min_time).toFixed(0) + " min"; }
        else { min_time_str = Number(props.min_time/60).toFixed(1) + " hrs"; }
        if (props.max_time < 60) { max_time_str = Number(props.max_time).toFixed(0) + " min"; }
        else { max_time_str = Number(props.max_time/60).toFixed(1) + " hrs"; }

        this._div.innerHTML = '<h4>Resumen</h4>' +
            n_str +
            '<br/>' +
            '<b>Distancias entre </b>' + min_dist_str + ' y ' + max_dist_str +
            '<br/>' +
            '<b>Tiempos entre </b>' + min_time_str + ' y ' + max_time_str;
    };
    info_div.addTo(map);

    info_div_single = L.control();
    info_div_single.onAdd = function (map) {
        this._div = L.DomUtil.create('div', 'info_div'); // create a div with a class "info"
        return this._div;
    };
    // method that we will use to update the control based on feature properties passed
    info_div_single.update = function (props) {
        if (!props.hasOwnProperty("service")) {
            this._div.innerHTML = '<h4>Seleccione un viaje</h4>'
            return;
        }

        var dist_str;
        if (props.dist < 1000) { dist_str = Number(props.dist).toFixed(0) + " mts"; }
        else { dist_str = Number(props.dist/1000).toFixed(1) + " kms"; }

        var time_str;
        if (props.time < 60) { time_str = Number(props.time).toFixed(0) + " min"; }
        else { time_str = Number(props.time/60).toFixed(1) + " hrs"; }

        this._div.innerHTML = '<h4>Viaje</h4>' +
            '<b>Servicio: </b>' + props.service +
            '<br/>' +
            '<b>Distancia: </b>' + dist_str +
            '<br/>' +
            '<b>Duración: </b>' + time_str;
    };
    info_div_single.addTo(map);
}


var cur_data;
var cur_data_timestamp = moment().subtract(1, 'days');

function resetCurData() {
    cur_data_timestamp = moment().subtract(1, 'days');
}

function loadData() {
    runSpinner();

    var now = moment();
    var elapsed_seconds = now.diff(cur_data_timestamp)/(1000);
    if (elapsed_seconds > 30*60) {
        var data_url = 'http://' + location.host + '/carriers/getUsersTravelMap/';
        var data_options = {
            date_init: $('#date_init').data("DateTimePicker").date().format("YYYY-MM-DD") + "T00:00:00",
            date_end: $('#date_end').data("DateTimePicker").date().add(1, 'days').format("YYYY-MM-DD") + "T00:00:00"
        };
        console.log("(re)loading data from: " + data_url);
        $.getJSON(data_url, data_options)
            .done(function (data) {
                console.log("... data retrieved");
                cur_data = data;
                cur_data_timestamp = moment();
                redrawData();
                stopSpinner();
            });
    } else {
        console.log("... using already loaded data from " + elapsed_seconds + " seconds ago.");
        redrawData();
        stopSpinner();
    }
}

// # http://localhost/carriers/getUsersTravelMap/?date_init=2016-10-24T00:00:00&date_end=2017-01-25T00:00:00&_=1485262643655
// # {
// #   "3e4b1eda90e01f977577c4dbcad03091c76c33942b1217a7e7bbf6d2483e568a19f121a86562b5ac5e9da7ae8399da776e889c0f0b6a6961cc8ce61757e90f99": {
// #       "origin": {"latitude": -33.4459671, "timeStamp": "2016-12-14T12:22:13Z", "longitude": -70.6605514},
// #       "destination": {"latitude": -33.4461054, "timeStamp": "2016-12-14T13:21:14Z", "longitude": -70.6615643},
// #       "service": "418"
// #   },
// #   ...



var origin_icon = L.icon({
    iconUrl: '/static/carrier/images/drawable-mdpi/circulo_inicio.png',
    shadowUrl: null,

    iconSize:     [22, 22], // size of the icon
    shadowSize:   [ 0,  0], // size of the shadow
    iconAnchor:   [11, 11], // point of the icon which will correspond to marker's location
    shadowAnchor: [ 0,  0], // the same for the shadow
    popupAnchor:  [11,  0]  // point from which the popup should open relative to the iconAnchor
});

var dest_icon = L.icon({
    iconUrl: '/static/carrier/images/drawable-mdpi/circulo_fin.png',
    shadowUrl: null,

    iconSize:     [22, 22], // size of the icon
    shadowSize:   [ 0,  0], // size of the shadow
    iconAnchor:   [11, 11], // point of the icon which will correspond to marker's location
    shadowAnchor: [ 0,  0], // the same for the shadow
    popupAnchor:  [11,  0]  // point from which the popup should open relative to the iconAnchor
});

var cur_markers = [];
function redrawData() {

    cur_markers.forEach(function (item, idx) {
        item.remove();
    });


    // stats
    var n_travels = 0;
    var min_dist = 99999999;
    var max_dist = 0;
    var min_time = 99999999;
    var max_time = 0;

    // control
    var drawOrigins = document.getElementById("toggle-button").checked;
    var checked_0 = document.getElementById("checkbox-distance-0").checked;
    var checked_1 = document.getElementById("checkbox-distance-1").checked;
    var checked_2 = document.getElementById("checkbox-distance-2").checked;
    var checked_3 = document.getElementById("checkbox-distance-3").checked;

    for (var user_id in cur_data) {
        var user_data = cur_data[user_id];
        if (!user_data.hasOwnProperty("origin") || !user_data.hasOwnProperty("destination")) {
            continue;
        }

        // data
        var origin_datum = user_data.origin;
        var dest_datum = user_data.destination;
        var origin_lat_lng = L.latLng(origin_datum.latitude, origin_datum.longitude);
        var dest_lat_lng = L.latLng(dest_datum.latitude, dest_datum.longitude);
        var origin_stamp = moment(origin_datum.timeStamp);
        var dest_stamp = moment(dest_datum.timeStamp);

        // only draw required markers
        var dist = origin_lat_lng.distanceTo(dest_lat_lng);
        if (dist < 100 && !checked_0) { continue;  }
        if (100  < dist && dist < 1000 && !checked_1) { continue;  }
        if (1000 < dist && dist < 5000 && !checked_2) { continue;  }
        if (5000 < dist && !checked_3) { continue;  }

        // stats
        if (dist < min_dist) { min_dist = dist; }
        if (dist > max_dist) { max_dist = dist; }
        var time_diff = dest_stamp.diff(origin_stamp)/(1000*60);
        if (time_diff < min_time) { min_time = time_diff; }
        if (time_diff > max_time) { max_time = time_diff; }

        // draw marker
        var view_marker = null;
        if (drawOrigins) {
            view_marker = L.marker(origin_lat_lng, {icon: origin_icon, riseOnHover: true}).addTo(map);
        } else {
            view_marker = L.marker(dest_lat_lng, {icon: dest_icon, riseOnHover: true}).addTo(map);
        }

        // mouse over functionality
        view_marker["user_id"] = user_id;
        view_marker.on('mouseover', function () {
            var user_data = cur_data[this.user_id];
            var origin_datum = user_data.origin;
            var dest_datum = user_data.destination;
            var origin_lat_lng = L.latLng(origin_datum.latitude, origin_datum.longitude);
            var dest_lat_lng = L.latLng(dest_datum.latitude, dest_datum.longitude);
            var origin_stamp = moment(origin_datum.timeStamp);
            var dest_stamp = moment(dest_datum.timeStamp);

            if (drawOrigins) {
                this["related_marker"] = L.marker(dest_lat_lng, {icon: dest_icon, zIndexOffset:1000}).addTo(map);
            } else {
                this["related_marker"] = L.marker(origin_lat_lng, {icon: origin_icon, zIndexOffset:1000}).addTo(map);
            }

            this["related_line"] = L.polyline([origin_lat_lng, dest_lat_lng], {
                    color: 'red',
                    weight: 2
                }).addTo(map).bringToFront();

            info_div_single.update({
                service: user_data.service,
                dist: origin_lat_lng.distanceTo(dest_lat_lng),
                time: dest_stamp.diff(origin_stamp)/(1000*60)
            });


        });
        view_marker.on('mouseout', function () {
            this.related_line.remove();
            this.related_marker.remove();
            info_div_single.update({});
        });
        cur_markers.push(view_marker);
        n_travels++;
    }
    console.log("Loaded " + n_travels + " user travels");

    info_div.update({
        n: n_travels,
        min_dist: min_dist,
        max_dist: max_dist,
        min_time: min_time,
        max_time: max_time
    });
    info_div_single.update({});
}
