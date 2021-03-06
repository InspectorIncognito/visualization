
$(document).ready(function () {
    var DATE_RANGE_INPUT = $("#dateRange");
    var REPORT_TYPES = $("#reportTypes");
    var UPDATE_BUTTON = $("#btnUpdateData");

    var target = document.getElementsByClassName("x_panel")[0];

    function getURL() {
        var data = {
            date_init: DATE_RANGE_INPUT.data("daterangepicker").startDate.format(),
            date_end: DATE_RANGE_INPUT.data("daterangepicker").endDate.format()
        };
        var types = REPORT_TYPES.val();
        if (types !== null) {
            data["types[]"] = types;
        }
        var params = $.param(data);
        var url = "/carriers/getFullTableBus/?";
        return url + params;
    }

    function initializeTable() {
        var fileName = "Todos los reportes";
        $.fn.dataTable.moment("DD-MM-YYYY HH:mm:ss");
        var dataTableOpts = {
            scrollX: true,
            pageLength: 15,
            order: [[1, "desc"]],
            dom: "Bfrtip",
            buttons: [
                {extend: "copy", text: "Copiar"},
                {extend: "csv",  filename: fileName},
                {extend: "excel", filename: fileName}
            ],
            ajax: getURL(),
            columns: [
                {title: "Tipo de Reporte ", data: "category"},
                {title: "Fecha", data: "timeCreation"},
                {title: "Reporte ", data: "type"},
                {title: "Verdaderos", data: "eventConfirm"},
                {title: "Falsos", data: "eventDecline"},
                {title: "Tipo de día", data: "typeOfDay"},
                {title: "Período media hora", data: "periodHour"},
                {title: "Servicio", data: "service"},
                {title: "Dirección", data: "direction"},
                {title: "Patente", data: "plate"},
                {title: "Comuna", data: "commune"},
                {title: "Paradero más cercano 1", data: "busStop1"},
                {title: "Paradero más cercano 2", data: "busStop2"},
                {title: "Zona 777", data: "zone777"},
                {title: "Período Transantiago", data: "periodTransantiago"}
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
            fnInitComplete: function () {
              $(target).spin(false);
            }
        };
        $(target).spin(spinnerOpt);
        return $("#datatable").dataTable(dataTableOpts);
    }

    // Initialize inputs
    DATE_RANGE_INPUT.daterangepicker(optionDateRangePicker);
    REPORT_TYPES.select2({
        placeholder: "Todos los tipos",
        allowClear: true
    });

    var table;

    UPDATE_BUTTON.click(function(){
        // activate spinner
        $(target).spin(spinnerOpt);
        table.api().ajax.url(getURL()).load(function(){
            $(target).spin(false)
        });
    });

    table = initializeTable();
});
