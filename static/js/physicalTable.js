var name;
var headerids = {}
function createheaders() {
    var Dataurl = "http://" + location.host + "/carriers/getPhysicalHeaders/";
    $.getJSON(Dataurl)
        .done(function (data) {
            var n = 0;
            var total = 0;
            $("#headers ul").html("");
            $.each(data, function (key, number) {
                n++;
                total += number;
                headerids[key]="header"+n
                $("#headers ul").append('<li id="' + headerids[key] + '" role="presentation"><a href="#" data-toggle="tab" onclick="changeUrl(\'' + key + '\')">' +
                    key + ' (<span id="number">' + number + '</span>)');
            });
            $("#headers ul").prepend('<li id="all" role="presentation" class="active"><a href="#" data-toggle="tab" onclick="changeUrl(\'all\')">Total (<span id="number">' + total + '</span>)');


            console.log(name)


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

$(document).ready(function () {
    createheaders();
    $.fn.dataTable.moment('DD-MM-YYYY HH:mm:ss');
    table = $('#example').DataTable({
        scrollX: true,
        pageLength: 15,
        dom: 'Bfrtip',
        order: [[2, 'desc']],
        ajax: 'http://' + location.host + '/carriers/getPhysicalTable/?name=all',
        columns: [
            {title: "Reporte", data: 'type'},
            {title: "Patente", data: 'plate'},
            {title: "Fecha", data: 'timeCreation'},
            {
                title: "Arreglar",
                data: null,
                "defaultContent": "<button type='button' class='btn-xs btn-primary' id='si'>Arreglar</button>"
            },
        ],
        language: {
            "url": "//cdn.datatables.net/plug-ins/1.10.12/i18n/Spanish.json"
        }
    });

    $('#example tbody').on('click', 'button', function () {
        var data = table.row($(this).parents('tr')).data();
        id = data.id;
        console.log(data)
        $('#confirmationtext').html('Reporte: ' + data.type + '<br>Patente: ' + data.plate)
        $("#myModal").modal()
    });

});
function fix() {
    var url = "http://" + location.host + "/carriers/updatePhysical/";
    $.getJSON(url, {"id": id})
        .done(function (data) {
            if (data == 'True') {
                table.ajax.reload();
                updateheaders();
            }
            else {
                console.log("Un error ocurrió");
            }
        });
}
setInterval(function () {
    updateheaders();
    table.ajax.reload();
}, 3000);

function changeUrl(key) {
    table.ajax.url('http://' + location.host + '/carriers/getPhysicalTable/?name=' + key).load();
}