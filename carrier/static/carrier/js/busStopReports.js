

var spinner = new Spinner(spinner_options)
    .spin(document.getElementById('right_col_page_content'));

$(function () {
    $('#date_init').datetimepicker({
        defaultDate: moment().subtract(3, 'months'),
        format: 'LL'
    });
    $('#date_end').datetimepicker({
        defaultDate: moment(),
        format: 'LL'
    });
    $("#filters :input").change(function () {
        myFunction();
    });
    $("#filters").on("dp.change", function () {
        myFunction();
    });
    init();
});

var table;
var url = 'http://' + location.host + '/carriers/getBusStopReports/';
var exportFileName = "ReportesLibresDeParaderos";
var exportButtonCommon = {
    exportOptions: {
        format: {
            body: function (data, row, column, node) {
                // row: row number
                // column: column number
                // node: cell DOM node: <td>, <td class="text-center">, ...
                // data:
                return data;
            }
        },
        orthogonal: 'export'
    }
};

function init() {
    var date_init = $('#date_init').data("DateTimePicker").date().format("YYYY-MM-DD");
    var date_end = $('#date_end').data("DateTimePicker").date().add(1, 'days').format("YYYY-MM-DD");
    var params = '?date_init=' + date_init + '&date_end=' + date_end;
    $.fn.dataTable.moment('DD-MM-YYYY HH:mm:ss');

    table = $('#bus-stop-reports-table').DataTable({
        scrollX: true,
        pageLength: 15,
        order: [[0, "desc"]],
        dom: 'Bfrtip',
        buttons: [

            $.extend(true, {}, exportButtonCommon, {
                extend: 'copy',
                text: 'Copiar'
            }),
            $.extend(true, {}, exportButtonCommon, {
                extend: 'csv',
                filename: exportFileName
            }),
            $.extend(true, {}, exportButtonCommon, {
                extend: 'excel',
                filename: exportFileName
            })
        ],
        ajax: url + params,
        columns: [
            {
                title: "Fecha",
                data: 'timeStamp'
            },
            {
                title: "Mensaje",
                data: 'message',
                render: $.fn.dataTable.render.ellipsis(40, true, false)
            },
            {
                title: "Paradero",
                data: 'busStopCode'
            },
            {
                title: "Ubicación",
                data: 'busStopName',
                render: $.fn.dataTable.render.ellipsis(30, true, false)
            },
            {
                title: "Mapa",
                class: "text-center",
                render: function (data, type, row) {
                    try {
                        if (type == 'export') {
                            // export as JSON {user: [-33.2423, -70.23234], bus_stop: [-33.2423, -70.23234]}
                            return '{user: [' + row.userLatitude + ', ' + row.userLongitude + '], bus_stop: [' +
                                        row.latitude + ', ' + row.longitude + ']}';
                        }
                        return '<a ' +
                                    'class="btn btn-default" ' +
                                    'onclick="openMapModal(' +
                                        row.userLatitude + ',' + row.userLongitude + ',' +
                                        row.latitude + ',' + row.longitude +
                                    ')"' +
                                'style="margin-bottom: 0; margin-right: 0">' +
                                '<i class="fa fa-map-marker"></i>' +
                                '</a>';
                    } catch (err) {
                        return " - "
                    }
                }
            },
            {
                title: "Comuna",
                data: 'commune'
            },
            {
                title: 'Imagen',
                class: "text-center",
                render: function (data, type, row) {
                    if (type == 'export') {
                        if (row.imageName != "no image") {
                            return row.imageName;
                        }
                        return "";
                    }
                    if (row.imageName != "no image") {
                        // export only imageName
                        return '<button ' +
                                    'type="button" ' +
                                    'class="btn btn-default" ' +
                                    'onclick="openModal(\'' + row.imageName + '\')"' +
                                'style="margin-bottom: 0; margin-right: 0">' +
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
                copyTitle: 'Copiar al portapapeles',
                copySuccess: {
                    _: 'Copiadas %d filas',
                    1: 'Copiada 1 fila'
                }
            }
        }
    }).on("init.dt", function () { spinner.stop(); });
}

var modal_map = null;
function openMapModal(user_lat, user_lon, bus_stop_lat, bus_stop_lon) {

    var user_lat_lng = L.latLng(user_lat, user_lon);
    var bus_stop_lat_lng = L.latLng(bus_stop_lat, bus_stop_lon);

    $('#modal-map-distance-info').text(Number(user_lat_lng.distanceTo(bus_stop_lat_lng)).toFixed(1));
    // $('#modal-map-content-bottom').html('');

    // modal table data
    $('#modal-bus-stop-lat').text(bus_stop_lat);
    $('#modal-bus-stop-lon').text(bus_stop_lon);
    $('#modal-user-lat').text(user_lat);
    $('#modal-user-lon').text(user_lon);


    // make sure the map recomputes the modal size, otherwise some tiles
    // will not be shown
    $('#modal-map-view').on('shown.bs.modal', function (e) {
        modal_map.invalidateSize();
    })
    $("#modal-map-view").modal();

    // create map on request
    if (modal_map == null) {

        var boundingBox = L.latLngBounds(user_lat_lng, bus_stop_lat_lng);

        modal_map = L.map('modal-map-leaflet').setView(boundingBox.getCenter(), 18);

        function loadDefaultMapboxTiles(options) {
            L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/256/{z}/{x}/{y}?access_token={accessToken}', {
                attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, Imagery © <a href="http://mapbox.com">Mapbox</a>',
                maxZoom: 18,
                accessToken: options.token
            }).addTo(modal_map);
        }
        loadGTFSOptions(loadDefaultMapboxTiles, null);

        // bus stop marker
        var bus_stop_icon = L.icon({
            iconUrl: '/static/carrier/images/paradero.png',
            shadowUrl: null,

            iconSize:     [32, 48], // size of the icon
            shadowSize:   [ 0,  0], // size of the shadow
            iconAnchor:   [16, 48], // point of the icon which will correspond to marker's location
            shadowAnchor: [ 0,  0],  // the same for the shadow
            popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
        });
        var bus_stop_marker = L.marker([bus_stop_lat, bus_stop_lon], {icon: bus_stop_icon}).addTo(modal_map);

        // user marker
        var user_icon = L.icon({
            iconUrl: '/static/carrier/images/usuario.png',
            shadowUrl: null,

            iconSize:     [30, 38], // size of the icon
            shadowSize:   [ 0,  0], // size of the shadow
            iconAnchor:   [15, 38], // point of the icon which will correspond to marker's location
            shadowAnchor: [ 0,  0],  // the same for the shadow
            popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
        });
        var user_marker = L.marker([user_lat, user_lon], {icon: user_icon}).addTo(modal_map);

        // var user_marker = L.circle([user_lat, user_lon], {
        //     color: 'red',
        //     fillColor: '#f03',
        //     fillOpacity: 0.5,
        //     radius: 15
        // }).addTo(modal_map);


        // console.log(gtfs_options);
        // if (gtfs_options != null) {
        //
        // } else {
        //     // destroy map
        //     // modal_map.
        //     $('#modal-map-content-bottom').html('<p> No se puede cargar el mapa.</p>');
        // }
        //
    }

    //$('#modal-body').html('<img src="' + imageName + '" alt="No se puede cargar la imagen" style="display:block; width: auto; max-width: 100%; height: auto;"/>');


    //
}

function openModal(imageName) {
    $('#modal-image-content').html('<img src="' + imageName + '" alt="No se puede cargar la imagen" style="display:block; width: auto; max-width: 100%; height: auto;"/>');
    $("#modal-image-view").modal();
}

function myFunction() {
    var date_init = $('#date_init').data("DateTimePicker").date().format("YYYY-MM-DD");
    var date_end = $('#date_end').data("DateTimePicker").date().add(1, 'days').format("YYYY-MM-DD");
    var params = '?date_init=' + date_init + '&date_end=' + date_end;
    table.ajax.url(url + params).load();
}