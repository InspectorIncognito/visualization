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
    init();
});

var table;
var fileName = "Reportes Libres";
var url = 'http://' + location.host + '/carriers/getReports/';

function init() {
    var date_init = $('#date_init').data("DateTimePicker").date().format("YYYY-MM-DD");
    var date_end = $('#date_end').data("DateTimePicker").date().format("YYYY-MM-DD");
    var params = '?date_init=' + date_init + '&date_end=' + date_end;
    $.fn.dataTable.moment('DD-MM-YYYY HH:mm:ss');
    var i = 0;
    table = $('#example').dataTable({
        scrollX: true,
        pageLength: 50,
        order: [[0, "desc"]],
        dom: 'Bfrtip',
        buttons: [
            {extend: 'copy', text: 'Copiar'}, {
                extend: 'csv',
                filename: fileName
            }, {extend: 'excel', filename: fileName},

        ],
        ajax: url + params,
        columns: [
            {title: "Fecha", data: 'timeStamp'},
            {title: "Mensaje", data: 'message'},
            {
                title: 'Imagen',
                data: 'imageName',
                defaultContent: "<button type='button' class='btn-xs btn-primary' id='si'> imageName </button>" //TODO should say Ver imagen if string isn't 'no image'
            },
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

    $('#example tbody').on('click', 'button', function () {
            var data = table.row($(this).parents('tr')).data();
            $('#confirmationtext').html('hola');
            $("#myModal").modal();
        });
}


function myFunction() {

    var date_init = $('#date_init').data("DateTimePicker").date().format("YYYY-MM-DD");
    var date_end = $('#date_end').data("DateTimePicker").date().format("YYYY-MM-DD");
    table.api().ajax.url(url + params).load();
}