$(document).ready(function() {
    var SPINNER_TARGET = document.getElementsByClassName("x_panel")[0];

    var TOGGLE_INPUT = $("#toggle-button");
    var DATE_RANGE_INPUT = $("#dateRange");
    var CHECKBOX_DISTANCE_0 = $("#checkbox-distance-0");
    var CHECKBOX_DISTANCE_1 = $("#checkbox-distance-1");
    var CHECKBOX_DISTANCE_2 = $("#checkbox-distance-2");
    var CHECKBOX_DISTANCE_3 = $("#checkbox-distance-3");

    // default check
    TOGGLE_INPUT.prop("checked", true);
    CHECKBOX_DISTANCE_0.prop("checked", false);
    CHECKBOX_DISTANCE_1.prop("checked", true);
    CHECKBOX_DISTANCE_2.prop("checked", true);
    CHECKBOX_DISTANCE_3.prop("checked", true);

    DATE_RANGE_INPUT.daterangepicker(optionDateRangePicker);
    DATE_RANGE_INPUT.on("apply.daterangepicker", function(){
        loadData();
    });
    TOGGLE_INPUT.change(function () {
        console.log("change");
        redrawData();
    });

    CHECKBOX_DISTANCE_0.change(function () {
        redrawData();
    });
    CHECKBOX_DISTANCE_1.change(function () {
        redrawData();
    });
    CHECKBOX_DISTANCE_2.change(function () {
        redrawData();
    });
    CHECKBOX_DISTANCE_3.change(function () {
        redrawData();
    });

    function createMap() {
        var santiagoLocation = L.latLng(-33.459229, -70.645348);
        var map = L.map("map_id").setView(santiagoLocation, 12);

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
            loadData();
            loadGTFSOptions(loadDefaultMapboxTiles, null);
        }, null);

        return map;
    }

    function createTripInfoControl () {
        var info_div_single = L.control();
        info_div_single.onAdd = function (map) {
            this._div = L.DomUtil.create("div", "info_div"); // create a div with a class "info"
            return this._div;
        };
        // method that we will use to update the control based on feature properties passed
        info_div_single.update = function (props) {
            if (!props.hasOwnProperty("service")) {
                this._div.innerHTML = "<h4>Seleccione un viaje</h4>"
                return;
            }

            var dist_str;
            if (props.dist < 1000) { dist_str = Number(props.dist).toFixed(0) + " mts"; }
            else { dist_str = Number(props.dist/1000).toFixed(1) + " kms"; }

            var time_str;
            if (props.time < 60) { time_str = Number(props.time).toFixed(0) + " min"; }
            else { time_str = Number(props.time/60).toFixed(1) + " hrs"; }

            this._div.innerHTML = "<h4>Viaje</h4>" +
                "<b>Servicio: </b>" + props.service +
                "<br/>" +
                "<b>Distancia: </b>" + dist_str +
                "<br/>" +
                "<b>Duración: </b>" + time_str;
        };
        return info_div_single;
    }

    function createResumeInfoControl () {
        var info_div = L.control();
        info_div.onAdd = function (map) {
            this._div = L.DomUtil.create("div", "info_div"); // create a div with a class "info"
            return this._div;
        };

        // method that we will use to update the control based on feature properties passed
        info_div.update = function (props) {
            if (props.n === 0) {
                this._div.innerHTML = "<h4>Sin Información</h4>";
                return;
            }
            var n_str;
            if (props.n === 1) { n_str = "1 viaje"; }
            else { n_str = props.n + " viajes"; }

            var min_dist_str, max_dist_str;

            var DISTANCE_THRESHOLD = 1000; // meters
            var TIME_THRESHOLD = 60; // minutes
            if (props.min_dist < DISTANCE_THRESHOLD) { min_dist_str = Number(props.min_dist).toFixed(0) + " mts"; }
            else { min_dist_str = Number(props.min_dist/1000).toFixed(1) + " kms"; }
            if (props.max_dist < DISTANCE_THRESHOLD) { max_dist_str = Number(props.max_dist).toFixed(0) + " mts"; }
            else { max_dist_str = Number(props.max_dist/1000).toFixed(1) + " kms"; }

            var min_time_str, max_time_str;
            if (props.min_time < TIME_THRESHOLD) { min_time_str = Number(props.min_time).toFixed(0) + " min"; }
            else { min_time_str = Number(props.min_time/60).toFixed(1) + " hrs"; }
            if (props.max_time < TIME_THRESHOLD) { max_time_str = Number(props.max_time).toFixed(0) + " min"; }
            else { max_time_str = Number(props.max_time/60).toFixed(1) + " hrs"; }

            this._div.innerHTML = "<h4>Resumen</h4>" +
                n_str +
                "<br/>" +
                "<b>Distancias entre </b>" + min_dist_str + " y " + max_dist_str +
                "<br/>" +
                "<b>Tiempos entre </b>" + min_time_str + " y " + max_time_str;
        };
        return info_div;
    }

    var map = createMap();
    var info_div = createResumeInfoControl();
    var info_div_single = createTripInfoControl();

    info_div.addTo(map);
    info_div_single.addTo(map);

    var trips;
    var cur_markers = [];

    function loadData() {
        var data_url = "/carriers/getUsersTravelMap/";
        var data_options = {
            date_init: DATE_RANGE_INPUT.data("daterangepicker").startDate.format(),
            date_end: DATE_RANGE_INPUT.data("daterangepicker").endDate.format()
        };

        $(SPINNER_TARGET).spin(spinnerOpt);
        $.getJSON(data_url, data_options)
            .done(function (data) {
                console.log("... data retrieved");
                trips = data;
                cur_data_timestamp = moment();
                $(SPINNER_TARGET).spin(false);
                redrawData();
            }).error(function(){
                $(SPINNER_TARGET).spin(false);
            });
    }

    function redrawData() {
        $(SPINNER_TARGET).spin(spinnerOpt);
        cur_markers.forEach(function (item) {
            item.remove();
        });

        // stats
        var n_travels = 0;
        var min_dist = 99999999;
        var max_dist = 0;
        var min_time = 99999999;
        var max_time = 0;

        // control
        var drawOrigins = TOGGLE_INPUT.is(":checked");
        var checked_0 = CHECKBOX_DISTANCE_0.is(":checked");
        var checked_1 = CHECKBOX_DISTANCE_1.is(":checked");
        var checked_2 = CHECKBOX_DISTANCE_2.is(":checked");
        var checked_3 = CHECKBOX_DISTANCE_3.is(":checked");

        for (var user_id in trips) {
            var user_data = trips[user_id];
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
            if (100  <= dist && dist < 1000 && !checked_1) { continue;  }
            if (1000 <= dist && dist < 5000 && !checked_2) { continue;  }
            if (5000 <= dist && !checked_3) { continue;  }

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
            view_marker.on("mouseover", function () {
                var user_data = trips[this.user_id];
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

                var polylineOpts = { color: "red", weight: 2 };
                this["related_line"] = L.polyline([origin_lat_lng, dest_lat_lng], polylineOpts).addTo(map).bringToFront();

                info_div_single.update({
                    service: user_data.service,
                    dist: origin_lat_lng.distanceTo(dest_lat_lng),
                    time: dest_stamp.diff(origin_stamp)/(1000*60)
                });
            });
            view_marker.on("mouseout", function () {
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
        $(SPINNER_TARGET).spin(false);
    }
});