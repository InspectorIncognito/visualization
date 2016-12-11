function headers() {
        var Dataurl = "http://" + location.host + "/carriers/getPhysicalHeaders/";
        $.getJSON(Dataurl)
                .done(function (data) {
                    var html = ''
                    $.each(data, function (key, number) {
                        html += '<div class="col-md-2 col-sm-4 col-xs-6 tile_stats_count">';
                        html += '<span class="count_top" title="' + key + '">' + key + '</span>';
                        html += '<div class="count" style="text-align:center">' + number + '</div>'
                        html += '</div>'
                    });
                    $("#headers").html(html);
                });
    }
    headers();
    var id;
    var text;
    var table;
    $(document).ready(function () {
        $.fn.dataTable.moment( 'DD-MM-YYYY HH:mm:ss' );
        table = $('#example').DataTable({
            scrollX: true,
            "pageLength": 15,
            order: [[2, 'desc']],
            responsive: true,
            ajax: 'http://' + location.host + '/carriers/getPhysicalTable/',
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
                        headers();
                    }
                    else{
                        console.log("Un error ocurrió");
                    }
                });
    }
    setInterval(function () {
        headers();
        table.ajax.reload();
    }, 30000);