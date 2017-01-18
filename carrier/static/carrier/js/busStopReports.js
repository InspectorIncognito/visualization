

var spinner = new Spinner(spinner_options)
    .spin(document.getElementById('main-content-panel'));

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
var fileName = "Reportes Libres";
var url = 'http://' + location.host + '/carriers/getBusStopReports/';

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
            {extend: 'copy', text: 'Copiar'},
            {extend: 'csv', filename: fileName},
            {extend: 'excel', filename: fileName}
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
                render: $.fn.dataTable.render.ellipsis( 40, true, false)
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
                        return '<a ' +
                                    'class="btn btn-default" ' +
                                    'onclick="openMapModal(' +
                                        row.userLatitude + ',' + row.userLongitude + ',' +
                                        row.latitude + ',' + row.longitude +
                                    ')">' +
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
                    if (row.imageName != "no image") {
                        return '<button ' +
                                    'type="button" ' +
                                    'class="btn btn-default" ' +
                                    'onclick="openModal(\'' + row.imageName + '\')"' +
                                '>' +
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
    $('#modal-map-content-top').html('<p>' + user_lat + ", " + user_lon + ", "  + bus_stop_lat + ", " + bus_stop_lon+ '</p>');

    // make sure the map recomputes the modal size, otherwise some tiles
    // will not be shown
    $('#modal-map-view').on('shown.bs.modal', function (e) {
        modal_map.invalidateSize();
    })
    $("#modal-map-view").modal();

    // create map on request
    if (modal_map == null) {

         var userLatLng = L.latLng(user_lat, user_lon);
         var busStopLatLng = L.latLng(bus_stop_lat, bus_stop_lon);
         var boundingBox = L.latLngBounds(userLatLng, busStopLatLng);

         modal_map = L.map('modal-map-leaflet').setView(boundingBox.getCenter(), 18);

         function loadDefaultMapboxTiles(options) {
            L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/256/{z}/{x}/{y}?access_token={accessToken}', {
                attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, Imagery © <a href="http://mapbox.com">Mapbox</a>',
                maxZoom: 18,
                accessToken: options.token
            }).addTo(modal_map);
         }
         loadGTFSOptions(loadDefaultMapboxTiles, null);

         var bus_stop_marker = L.marker([bus_stop_lat, bus_stop_lon]).addTo(modal_map);

         var user_marker = L.circle([user_lat, user_lon], {
            color: 'red',
            fillColor: '#f03',
            fillOpacity: 0.5,
            radius: 15
        }).addTo(modal_map);


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