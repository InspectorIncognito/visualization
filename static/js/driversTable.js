var table;
        var date = moment();
        var dateString = date.format("DD-MM-YYYY");
        var fileName = "Reportes diarios " + dateString + " Comportamiento del Conductor";
        $(document).ready(function () {
            $.fn.dataTable.moment( 'DD-MM-YYYY HH:mm:ss' );
            table = $('#example').dataTable({
                scrollX: true,
                pageLength: 15,
                order: [[1, "desc"]],
                dom: 'Bfrtip',
                buttons: [
                    {extend: 'copy', text: 'Copiar'}, {
                        extend: 'csv',
                        filename: fileName
                    }, {extend: 'excel', filename: fileName},

                ],
                ajax: 'http://' + location.host + '/carriers/getDriversTable/',
                columns: [
                    {title: "Reporte", data: 'type'},
                    {title: "Fecha", data: 'timeCreation'},
                    {title: "Patente", data: 'plate'},
                    {title: "Servicio", data: 'service'},
                    {title: "Lugar", data: 'commune'},
                    {title: "Paradero 1", data: 'busStop1'},
                    {title: "Paradero 2", data: 'busStop2'}
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
        }, 30000);