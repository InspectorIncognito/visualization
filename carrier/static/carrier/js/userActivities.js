
$(document).ready(function () {
    var target = document.getElementsByClassName("x_panel")[0];

    var table = null;
    var DATE_RANGE_INPUT = $("#dateRange");

    DATE_RANGE_INPUT.daterangepicker(optionDateRangePicker);

    DATE_RANGE_INPUT.on("apply.daterangepicker", function(){
        $(target).spin(spinnerOpt);
        table.ajax.url(getURL()).load(function(){
            $(target).spin(false);
        });
    });

    function getURL() {
        var URL = "/carriers/getUsersActivities/?";
        var data = {
            date_init: DATE_RANGE_INPUT.data("daterangepicker").startDate.format(),
            date_end: DATE_RANGE_INPUT.data("daterangepicker").endDate.format()
        };
        return URL + $.param(data);
    }

    var dateString = moment().format("YYYY-MM-DD");
    var exportFileName = "TablaDeActividadDeUsuarios" + dateString;

    $.fn.dataTable.moment('DD-MM-YYYY HH:mm:ss');
    var datatableOpts = {
        scrollX: true,
        pageLength: 15,
        order: [[1, "desc"]],
        dom: 'Bfrtip',
        buttons: [
            { extend: 'copy', text: 'Copiar' },
            { extend: 'csv', filename: exportFileName },
            { extend: 'excel', filename: exportFileName }
        ],
        ajax: getURL(),
        columns: [
            { title: "Dispositivo", data: "device_id" },
            { title: "Viajes", data: "tokenCount", class: "text-right" },
            { title: "GPS", data: "devicePositionInTimeCount", class: "text-right" },
            { title: "R",  data: "reportCount", class: "text-right" },
            { title: "ECB", data: "busEventCreationCount", class: "text-right" },
            { title: "ECP", data: "busStopEventCreationCount", class: "text-right" },
            { title: "B+", data: "confirmBusCount", class: "text-right" },
            { title: "B-", data: "declineBusCount", class: "text-right" },
            { title: "P+", data: "confirmBusStopCount", class: "text-right" },
            { title: "P-", data: "declineBusStopCount", class: "text-right" },
            { title: "VP", data: "busStopCheckCount", class: "text-right" }
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
    };
    $(target).spin(spinnerOpt);
    table = $("#datatable").DataTable(datatableOpts).on("init.dt", function () {
        $(target).spin(false);
    });
});