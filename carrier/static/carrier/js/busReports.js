$(function () {
    DATE_RANGE_INPUT = $("#dateRange");
    DATE_RANGE_INPUT.daterangepicker(optionDateRangePicker);

    function getURL() {
        var URL = "/carriers/getBusReports/?";
        var data = {
            date_init: DATE_RANGE_INPUT.data("daterangepicker").startDate.format(),
            date_end: DATE_RANGE_INPUT.data("daterangepicker").endDate.format()
        };
        return URL + $.param(data);
    }

    var target = document.getElementsByClassName("x_content")[0];
    var spinner = new Spinner(spinnerOpt).spin(target);

    var dateString = moment().format("YYYY-MM-DD");
    var exportFileName = "ReportesLibresDeBuses_" + dateString;
    $.fn.dataTable.moment("DD-MM-YYYY HH:mm:ss");

    var dataTableOpts = {
        scrollX: true,
        pageLength: 15,
        order: [[0, "desc"]],
        dom: "Bfrtip",
        buttons: [
            {extend: "copy", text: "Copiar"},
            {extend: "csv", filename: exportFileName},
            {extend: "excel", filename: exportFileName}
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
        },
        ajax: getURL(),
        columns: [
            {title: "Fecha", data: "timeStamp"},
            {title: "Mensaje", data: "message"},// render: $.fn.dataTable.render.ellipsis(60, true, false)},
            {title: "Patente", data: "registrationPlate", class: "text-center"},
            {title: "Servicio", data: "service", class: "text-center" },
            {title: "Dirección", data: "direction",
                render: function (data, type, row) {
                    if (data === "I") {
                        return "IDA";
                    } else if (data === "R") {
                        return "REGRESO";
                    }
                    return data;
                }
            },
            {title: "Mapa", class: "text-center",
                render: function (data, type, row) {
                    try {
                        if (type === "export") {
                            // export as JSON {bus: [-33.2423, -70.23234]}
                            return "{bus: [" +
                                        row.latitude + ", " + row.longitude + "]}";
                        }
                        return "<a class='btn btn-default' onclick='openMapModal(" + row.latitude + "," + row.longitude + ")' " +
                                "style='margin-bottom: 0; margin-right: 0'>" +
                                "<i class='fa fa-map-marker'></i></a>";
                    } catch (err) {
                        return " - "
                    }
                }
            },
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
                        return "<button type='button' class='btn btn-default' onclick='openImageModal(\"" + image_filename + "\")'" +
                                " style='margin-bottom: 0; margin-right: 0'> Ver Imagen </button>";
                    }
                    return "No hay";
                }
            }
        ]
    };

    // activate spinner
    spinner.spin(target);
    var table = $("#bus-reports-table").DataTable(dataTableOpts).on("init.dt", function () {
        spinner.stop();
    });

    DATE_RANGE_INPUT.on("apply.daterangepicker", function(){
        // activate spinner
        spinner.spin(target);
        table.ajax.url(getURL()).load();
        spinner.stop();
    });
});

var modal_map = null;
var bus_marker = null;

// bus marker
var bus_icon = L.icon({
    iconUrl: "/static/carrier/images/usuario.png",
    shadowUrl: null,

    iconSize:     [30, 38], // size of the icon
    shadowSize:   [ 0,  0], // size of the shadow
    iconAnchor:   [15, 38], // point of the icon which will correspond to marker"s location
    shadowAnchor: [ 0,  0],  // the same for the shadow
    popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
});

function openMapModal(bus_lat, bus_lon) {

    var bus_lat_lng = L.latLng(bus_lat, bus_lon);

    // RENDER MODAL INFORMATION
    // --------------------------------------------------------------------------

    // bus_stop and user coordinates
    $("#modal-bus-lat").text(bus_lat);
    $("#modal-bus-lon").text(bus_lon);

    // RENDER MODAL MAP
    // --------------------------------------------------------------------------

    // make sure the map recomputes the modal size, otherwise some tiles
    // will not be shown
    var modal_map_view = $("#modal-map-view");
    modal_map_view.on("shown.bs.modal", function () {
        modal_map.invalidateSize();
    });
    modal_map_view.modal();

    // create map on request
    if (modal_map === null) {

        modal_map = L.map("modal-map-leaflet").setView(bus_lat_lng, 17);

        function loadDefaultMapboxTiles(options) {
            L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/256/{z}/{x}/{y}?access_token={accessToken}", {
                attribution: "Map data &copy; <a href='http://openstreetmap.org'>OpenStreetMap</a> contributors, Imagery © <a href='http://mapbox.com'>Mapbox</a>",
                maxZoom: 18,
                accessToken: options.token
            }).addTo(modal_map);
        }
        loadGTFSOptions(loadDefaultMapboxTiles, null);

        // bus stop marker
        bus_marker = L.marker(bus_lat_lng, {icon: bus_icon}).addTo(modal_map);
    } else {
        // update values
        bus_marker.setLatLng(bus_lat_lng);
        modal_map.setView(bus_lat_lng, 17);
    }
}

function openImageModal(imageName) {
    $("#modal-image-content").html('<img src="' + imageName + '" alt="No se puede cargar la imagen" style="display:block; margin: auto; width: auto; max-width: 100%; height: auto; max-height: 400px"/>');
    $("#modal-image-view").modal();
}