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
    $("#filters").on("dp.change", function (e) {
        myFunction();
    });
    $('#types').on("select2:select", function () {
        if ($(".select2_multiple").val()[0] == "Todos los tipos") {
            $("#types").select2("val", "");
        }
    });
    init();
});

$(document).ready(function () {
    $(".select2_multiple").select2({
        placeholder: "Todos los tipos",
        allowClear: true
    });
});

var table;
var fileName = "Todos los reportes";
var url = 'http://' + location.host + '/carriers/getFullTable/';

function init() {
    var date_init = $('#date_init').data("DateTimePicker").date().format("YYYY-MM-DD");
    var date_end = $('#date_end').data("DateTimePicker").date().format("YYYY-MM-DD");
    var types = $(".select2_multiple").val();
    var params = '?date_init=' + date_init + '&date_end=' + date_end;
    if (types != null) params += '&types=' + JSON.stringify(types);
    $.fn.dataTable.moment('DD-MM-YYYY HH:mm:ss');
    table = $('#example').dataTable({
        pageLength: 50,
        order: [[1, "desc"]],
        dom: 'Bfrtip',
        buttons: [
            {extend: 'copy', text: 'Copiar'}, {
                extend: 'csv',
                filename: fileName
            }, {extend: 'excel', filename: fileName},

        ],
        responsive: true,
        ajax: url + params,
        columns: [
            {title: "Tipo de Reporte ", data: 'category'},
            {title: "Fecha", data: 'timeCreation'},
            {title: "Reporte ", data: 'type'},
            {title: "Verdaderos", data: 'eventConfirm'},
            {title: "Falsos", data: 'eventDecline'},
            {title: "Tipo de día", data: 'plate'},
            {title: "Período media hora", data: 'periodHour'},
            {title: "Servicio", data: 'service'},
            {title: "Patente", data: 'plate'},
            {title: "Comuna", data: 'commune'},
            {title: "Paradero 1", data: 'busStop1'},
            {title: "Paradero 2", data: 'busStop2'},
            {title: "Zona 777-lugar", data: 'zone777'},
            {title: "Período Transantiago", data: 'periodTransantiago'},
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
    });
}

function myFunction() {

    var date_init = $('#date_init').data("DateTimePicker").date().format("YYYY-MM-DD");
    var date_end = $('#date_end').data("DateTimePicker").date().format("YYYY-MM-DD");
    var types = $(".select2_multiple").val();
    var params = '?date_init=' + date_init + '&date_end=' + date_end;
    if (types != null) params += '&types=' + JSON.stringify(types);
    table.api().ajax.url(url + params).load();
}