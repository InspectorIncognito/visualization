
$(function () {
    var DATE_RANGE_INPUT = $("#dateRange");
    var TABLE = $("#bus-stop-reports-table");

    optionDateRangePicker.startDate = moment().subtract(3, "months");
    DATE_RANGE_INPUT.daterangepicker(optionDateRangePicker);

    function getURL() {
        var URL = "/carriers/getBusStopReports/?";
        var data = {
            date_init: DATE_RANGE_INPUT.data("daterangepicker").startDate.format(),
            date_end: DATE_RANGE_INPUT.data("daterangepicker").endDate.format()
        };
        return URL + $.param(data);
    }

    var table;

    var target = document.getElementsByClassName("x_content")[0];
    var spinner = new Spinner(spinnerOpt).spin(target);

    var dateString = moment().format("YYYY-MM-DD");
    var exportFileName = "ReportesLibresDeParaderos_" + dateString;
    $.fn.dataTable.moment("DD-MM-YYYY HH:mm:ss");

    var dataTableOpts = {
        scrollX: true,
        pageLength: 15,
        order: [[0, "desc"]],
        dom: "Bfrtip",
        buttons: [
            {extend: "copy", text: "Copiar"},
            {extend: "csv",  filename: exportFileName},
            {extend: "excel", filename: exportFileName}
        ],
        ajax: getURL(),
        columns: [
            {title: "Fecha", data: "timeStamp"},
            {title: "Mensaje", data: "message",
                render: $.fn.dataTable.render.ellipsis(40, true, false)
            },
            {title: "Paradero", data: "busStopCode"},
            {title: "Ubicación", data: "busStopName",
                render: $.fn.dataTable.render.ellipsis(30, true, false)
            },
            {title: "Mapa", class: "text-center",
                render: function (data, type, row) {
                    try {
                        if (type === "export") {
                            // export as JSON {user: [-33.2423, -70.23234], bus_stop: [-33.2423, -70.23234]}
                            return "{user: [" + row.userLatitude + ", " + row.userLongitude + "], bus_stop: [" +
                                        row.latitude + ", " + row.longitude + "]}";
                        }
                        return "<a class='btn btn-default' " +
                                    'onclick="openMapModal(' +
                                        row.userLatitude + ',' + row.userLongitude + ',' +
                                        row.latitude + ',' + row.longitude +
                                    ')" ' +
                                'style="margin-bottom: 0; margin-right: 0">' +
                                '<i class="fa fa-map-marker"></i>' +
                                '</a>';
                    } catch (err) {
                        return " - "
                    }
                }
            },
            {title: "Comuna", data: "commune"},
            {title: "Imagen", class: "text-center",
                render: function (data, type, row) {
                    var image_filename = row.imageName;
                    if (type === "export") {
                        if (image_filename !== "no image") {
                            return image_filename;
                        }
                        return "";
                    }
                    if (image_filename !== "no image") {
                        // export only imageName
                        return '<button ' +
                                    'type="button" ' +
                                    'class="btn btn-default" ' +
                                    'onclick="openImageModal(\'' + image_filename + '\')"' +
                                ' style="margin-bottom: 0; margin-right: 0">' +
                                ' Ver Imagen ' +
                                '</button>';
                    }
                    // return "<span style='color:red'> No hay </span>";
                    return "No hay";
                }
            }
        ],
        language: {
            "url": "//cdn.datatables.net/plug-ins/1.10.12/i18n/Spanish.json",
            buttons: {
                copyTitle: "Copiar al portapapeles",
                copySuccess: {
                    _: "Copiadas %d filas",
                    1: "Copiada 1 fila"
                }
            }
        }
    };

    // activate spinner
    spinner.spin(target);
    table = TABLE.DataTable(dataTableOpts).on("init.dt", function () { spinner.stop(); });
    spinner.stop();

    DATE_RANGE_INPUT.on("apply.daterangepicker", function(){
        // activate spinner
        spinner.spin(target);
        table.ajax.url(getURL()).load();
        spinner.stop();
    });
});

var modal_map = null;
var bus_stop_marker = null;
var user_marker = null;

function openMapModal(user_lat, user_lon, bus_stop_lat, bus_stop_lon) {

    var user_lat_lng = L.latLng(user_lat, user_lon);
    var bus_stop_lat_lng = L.latLng(bus_stop_lat, bus_stop_lon);
    var map_bounding_box = L.latLngBounds(user_lat_lng, bus_stop_lat_lng);

    // testing
    // user_lat_lng = L.latLng(user_lat + 0.01, user_lon + 0.01);
    // map_bounding_box = L.latLngBounds(user_lat_lng, bus_stop_lat_lng);

    // RENDER MODAL INFORMATION
    // --------------------------------------------------------------------------

    // distance bus_stop - user
    var user_bus_stop_distance = user_lat_lng.distanceTo(bus_stop_lat_lng);
    $("#modal-map-distance-info")
        .text(Number(user_bus_stop_distance).toFixed(1))
        .parent()
        .removeClass("text-info")
        .removeClass("text-warning")
        .addClass(function() {
            if (user_bus_stop_distance < 100) {
                return "text-info";
            }
            return "text-warning";
        });

    // bus_stop and user coordinates
    $("#modal-bus-stop-lat").text(bus_stop_lat);
    $("#modal-bus-stop-lon").text(bus_stop_lon);
    $("#modal-user-lat").text(user_lat);
    $("#modal-user-lon").text(user_lon);


    // RENDER MODAL MAP
    // --------------------------------------------------------------------------

    // make sure the map recomputes the modal size, otherwise some tiles
    // will not be shown
    var modal_map_view = $("#modal-map-view");
    modal_map_view.on("shown.bs.modal", function () {
        modal_map.invalidateSize();
        modal_map.fitBounds(map_bounding_box);
    });
    modal_map_view.modal();

    // create map on request
    if (modal_map === null) {

        modal_map = L.map("modal-map-leaflet").setView(map_bounding_box.getCenter(), 17);

        function loadDefaultMapboxTiles(options) {
            L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/256/{z}/{x}/{y}?access_token={accessToken}", {
                attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, Imagery © <a href="http://mapbox.com">Mapbox</a>',
                maxZoom: 18,
                accessToken: options.token
            }).addTo(modal_map);
        }
        loadGTFSOptions(loadDefaultMapboxTiles, null);

        // bus stop marker
        bus_stop_marker = L.marker(bus_stop_lat_lng, {icon: bus_stop_icon}).addTo(modal_map);

        // user marker
        user_marker = L.marker(user_lat_lng, {icon: user_icon}).addTo(modal_map);


    } else {
        // update values
        bus_stop_marker.setLatLng(bus_stop_lat_lng);
        user_marker.setLatLng(user_lat_lng);

        //modal_map.fitBounds(map_bounding_box);
    }
}

function openImageModal(imageName) {
    $("#modal-image-content").html('<img src="' + imageName + '" alt="No se puede cargar la imagen" style="display:block; margin: auto; width: auto; max-width: 100%; height: auto; max-height: 400px"/>');
    $("#modal-image-view").modal();
}