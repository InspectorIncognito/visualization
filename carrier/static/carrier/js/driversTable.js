
var table;
var date = moment();
var dateString = date.format("YYYY-MM-DD");
var exportFileName = "EventosDeConductores_" + dateString;

$(document).ready(function () {
    $.fn.dataTable.moment( 'DD-MM-YYYY HH:mm:ss' );
    table = $('#example').dataTable({
        scrollX: true,
        pageLength: 15,
        order: [[1, "desc"]],
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'copy',
                text: 'Copiar'
            },
            {
                extend: 'csv',
                filename: exportFileName
            },
            {
                extend: 'excel',
                filename: exportFileName
            }
        ],
        ajax: 'http://' + location.host + '/carriers/getDriversTable/',
        columns: [
            {title: "Reporte", data: 'type'},
            {title: "Fecha", data: 'timeCreation'},
            {title: "Patente", data: 'plate'},
            {title: "Servicio", data: 'service'},
            {title: "Dirección", data: 'direction'},
            {title: "Comuna", data: 'commune'},
            {title: "Paradero más cercano 1", data: 'busStop1'},
            {title: "Paradero más cercano 2", data: 'busStop2'}
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
});

setInterval(function () {
    table.api().ajax.reload();
}, 300000);