var name;
var headerids = {};
function createheaders() {
    var Dataurl = "http://" + location.host + "/carriers/getPhysicalHeaders/";
    $.getJSON(Dataurl)
        .done(function (data) {
            var n = 0;
            var total = 0;

            var header_selector = $("#headers ul");
            header_selector.html("");
            $.each(data, function (key, number) {
                n++;
                total += number;
                headerids[key] = "header" + n;
                header_selector.append(
                    '<li id="' + headerids[key] + '" role="presentation">' +
                        '<a href="#" data-toggle="tab" onclick="changeUrl(\'' + key + '\')">' +
                            key + ' (<span id="number">' + number + '</span>)');
            });
            header_selector.prepend(
                '<li id="all" role="presentation" class="active">' +
                    '<a href="#" data-toggle="tab" onclick="changeUrl(\'all\')">' +
                        'Total (<span id="number">' + total + '</span>)');

            // console.log(name);
        });
}
function updateheaders() {
    var Dataurl = "http://" + location.host + "/carriers/getPhysicalHeaders/";
    $.getJSON(Dataurl)
        .done(function (data) {
            var total = 0;
            $.each(data, function (key, number) {
                total += number;
                $("#" + headerids[key] + " #number").text(number)
            });
            $("#all #number").text(total)

        });
}


var id;
var text;
var table;

var date = moment();
var dateString = date.format("YYYY-MM-DD");
var exportFileName = "EventosDeBuses_" + dateString;

var modal_data = null;
$(document).ready(function () {
    createheaders();
    $.fn.dataTable.moment('DD-MM-YYYY HH:mm:ss');
    table = $("#bus-events-table").DataTable({
        scrollX: true,
        pageLength: 15,
        dom: 'Bfrtip',
        buttons: [
            $.extend(true, {}, exportButtonCommon, {
                extend: 'copy',
                text: 'Copiar',
                exportOptions: {
                    columns: [ 0, 2, 4, 3 ]
                }
            }),
            $.extend(true, {}, exportButtonCommon, {
                extend: 'csv',
                filename: exportFileName,
                exportOptions: {
                    columns: [ 1, 2, 4, 3 ]
                }
            }),
            $.extend(true, {}, exportButtonCommon, {
                extend: 'excel',
                filename: exportFileName,
                exportOptions: {
                    columns: [ 1, 2, 4, 3 ]
                }
            })
        ],
        order: [[2, 'desc']],
        ajax: 'http://' + location.host + '/carriers/getPhysicalTable/?name=all',
        columns: [
            {
                // copy
                title: "¿Arreglado?",
                visible: false,
                data: null,
                defaultContent: "[ ]"
            },
            {
                // for csv and excel
                title: "¿Arreglado?",
                visible: false,
                data: null,
                defaultContent: ""
            },
            {
                title: "Fecha",
                data: 'timeCreation',
                width: "20%"
            },
            {title: "Evento Reportado", data: 'type'},
            {title: "Patente", data: 'plate'},
            {
                title: "Arreglar",
                class: "text-center",
                render: function (data, type, row) {
                    modal_data = row;
                    return '<button ' +
                                'type="button" ' +
                                'class="btn-xs btn-primary" ' +
                                'onclick="openEventModal()" ' +
                                'style="margin-bottom: 0; margin-right: 0">' +
                                ' Arreglar ' +
                            '</button>';
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
});

function openEventModal() {
    if (modal_data) {
        $("#modal-physical-event").text(modal_data.type);
        $("#modal-physical-plate").text(modal_data.plate);
        $("#modal-event-confirmation").modal()
    }
}

function fix() {
    var url = "http://" + location.host + "/carriers/updatePhysical/";
    $.getJSON(url, {"id": id})
        .done(function (data) {
            if (data == 'True') {
                table.ajax.reload();
                updateheaders();
            }
            // else {
            //     console.log("Un error ocurrió");
            // }
        });
}
setInterval(function () {
    pdateheaders();
    table.ajax.reload();
}, 300000);

function changeUrl(key) {
    table.ajax.url('http://' + location.host + '/carriers/getPhysicalTable/?name=' + key).load();
}