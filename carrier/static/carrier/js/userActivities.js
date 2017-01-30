
$(function () {
    $('#date_init').datetimepicker({
        defaultDate: moment().subtract(1, 'months'),
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
var url = 'http://' + location.host + '/carriers/getUsersActivities/';

var date = moment();
var dateString = date.format("YYYY-MM-DD");
var exportFileName = "TablaDeActividadDeUsuarios" + dateString;

function init() {
    var date_init = $('#date_init').data("DateTimePicker").date().format("YYYY-MM-DD") + "T00:00:00";
    var date_end = $('#date_end').data("DateTimePicker").date().add(1, 'days').format("YYYY-MM-DD") + "T00:00:00";
    var params = '?date_init=' + date_init + '&date_end=' + date_end;
    $.fn.dataTable.moment('DD-MM-YYYY HH:mm:ss');

    table = $('#bus-stop-reports-table').DataTable({
        scrollX: true,
        pageLength: 15,
        order: [[1, "desc"]],
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
                title: "Dispositivo",
                data: "device_id"
            },
            {
                title: "Viajes",
                data: "tokenCount",
                class: "text-right"
            },
            {
                title: "GPS",
                data: "devicePositionInTimeCount",
                class: "text-right"
            },
            {
                title: "R",
                data: "reportCount",
                class: "text-right"
            },
            {
                title: "ECB",
                data: "busEventCreationCount",
                class: "text-right"
            },
            {
                title: "ECP",
                data: "busStopEventCreationCount",
                class: "text-right"
            },
            {
                title: "B+",
                data: "confirmBusCount",
                class: "text-right"
            },
            {
                title: "B-",
                data: "declineBusCount",
                class: "text-right"
            },
            {
                title: "P+",
                data: "confirmBusStopCount",
                class: "text-right"
            },
            {
                title: "P-",
                data: "declineBusStopCount",
                class: "text-right"
            },
            {
                title: "VP",
                data: "busStopCheckCount",
                class: "text-right"
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

function myFunction() {
    var date_init = $('#date_init').data("DateTimePicker").date().format("YYYY-MM-DD") + "T00:00:00";
    var date_end = $('#date_end').data("DateTimePicker").date().add(1, 'days').format("YYYY-MM-DD") + "T00:00:00";
    var params = '?date_init=' + date_init + '&date_end=' + date_end;
    table.ajax.url(url + params).load();
}