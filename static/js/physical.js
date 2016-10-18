$(function () {
    $('#date_init').datetimepicker({
        defaultDate: moment().subtract(3, 'months'),
        format: 'LL'
    });
    $('#date_end').datetimepicker({
        defaultDate: moment(),
        format: 'LL'
    });
    $('#hour1').datetimepicker({
        defaultDate: moment().set({'hour': 0, 'minute': 0}),
        format: 'LT'
    });
    $('#hour2').datetimepicker({
        defaultDate: moment().set({'hour': 23, 'minute': 59}),
        format: 'LT'
    });
    $("#group :input").change(function () {
        updatechart();
    });
    $("#filters :input").change(function () {
        myFunction();
    });
    myFunction();
});
$(document).ready(function() {
        $(".select2_single").select2({});
        $(".select2_group").select2({});
        $(".select2_multiple").select2({});
      });
var resp = null;
var types = 0;
var chartdata = {
    'weekday': null,
    'plate': null,
    'service': null,
    'daily': null,
    'monthly': null
};
var chart;
function reloadchart() {
    chartdata = {
        'weekday': null,
        'plate': null,
        'service': null,
        'daily': null,
        'monthly': null
    };
}

function updatechart() {
    if (resp != null) {
        switch ($('input:checked', '#group').val()) {
            case "weekday":
                if (chartdata['weekday'] == null) {
                    chartdata['weekday'] = [];
                    for (i = 0; i < types.length; i++) {
                        chartdata['weekday'].push([0, 0, 0, 0, 0, 0, 0]);
                    }
                    console.log(chartdata['weekday']);
                    for (i = 0; i < resp.length; i++) {
                        var type = resp[i]['type'];
                        console.log(type);
                        var day = (moment(resp[i]['timeCreation'], "DD-MM-YYYY HH:mm:SS").day() + 6) % 7;
                        chartdata['weekday'][type][day]++;
                    }
                }
                var cols = [];
                for (i = 0; i < types.length; i++) {
                    cols.push([types[i]].concat(chartdata['weekday'][i]));
                }
                chart = c3.generate({
                    data: {
                        columns: cols,
                        type: 'bar'
                    },
                    axis: {
                        x: {
                            type: 'category',
                            categories: ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
                        },
                        y: {
                            tick: {
                                outer: false
                            }
                        }
                    }
                });
                break;

            case "plate":
                if (chartdata['plate'] == null) {
                    chartdata['plate'] = {
                        'plates': [],
                        'platetype': []
                    }
                    chartdata['plate']['plates'] = [];
                    chartdata['plate']['platetype'] = [];
                    for (i = 0; i < types.length; i++) {
                        chartdata['plate']['platetype'].push([]);
                    }
                    for (i = 0; i < resp.length; i++) {
                        var type = resp[i]['type'];
                        var plate = resp[i]['plate'];
                        if (chartdata['plate']['plates'].indexOf(plate) == -1) {
                            chartdata['plate']['plates'].push(plate)
                            for (var j = 0; j < types.length; j++) {
                                chartdata['plate']['platetype'][j].push(0);
                            }
                        }
                        var p = chartdata['plate']['plates'].indexOf(plate);
                        chartdata['plate']['platetype'][type][p]++;
                    }
                }
                var cols = [];
                for (i = 0; i < types.length; i++) {
                    cols.push([types[i]].concat(chartdata['plate']['platetype'][i]));
                }
                chart = c3.generate({
                    data: {
                        columns: cols,
                        type: 'bar',
                    },
                    axis: {
                        x: {
                            type: 'category',
                            tick: {
                                rotate: 90,
                                multiline: false
                            },
                            categories: chartdata['plate']['plates']
                        },
                        y: {
                            tick: {
                                outer: false
                            }
                        }
                    }
                });
                break;

            case "service":
                if (chartdata['service'] == null) {
                    var services = [];
                    var servicetype = [];
                    for (i = 0; i < types.length; i++) {
                        servicetype.push([]);
                    }
                    for (i = 0; i < resp.length; i++) {
                        var type = resp[i]['type'];
                        var service = resp[i]['service'];
                        console.log(service)
                        if (services.indexOf(service) == -1) {
                            services.push(service)
                            for (var j = 0; j < types.length; j++) {
                                servicetype[j].push(0);
                            }
                        }
                        var p = services.indexOf(service);
                        servicetype[type][p]++;
                    }
                }
                var cols = [];
                for (i = 0; i < types.length; i++) {
                    cols.push([types[i]].concat(servicetype[i]));
                }
                chart = c3.generate({
                    data: {
                        columns: cols,
                        type: 'bar'
                    },
                    axis: {
                        x: {
                            type: 'category',
                            tick: {
                                rotate: 90,
                                multiline: false
                            },
                            categories: services
                        },
                        y: {
                            tick: {
                                outer: false
                            }
                        }
                    }
                });
                break;
        }
    }
}
function myFunction() {
    var Dataurl = "http://localhost:8000/carriers/getPhysicalData/";
    var data = {
        carrier: '3',
        date_init: $('#date_init').data("DateTimePicker").date().format("YYYY-MM-DD"),
        date_end: $('#date_end').data("DateTimePicker").date().format("YYYY-MM-DD"),
        hour1: $('#hour1').data("DateTimePicker").date().format("HH"),
        hour2: $('#hour2').data("DateTimePicker").date().format("HH"),
        minute1: $('#hour1').data("DateTimePicker").date().format("mm"),
        minute2: $('#hour2').data("DateTimePicker").date().format("mm")
    };
    var service = $(".select2_multiple").val();
    console.log(service)
    var plate = document.getElementById("plate").value;
    if (service != null) data['service'] = JSON.stringify(service);
    if (plate != '') data['plate'] = plate;

    $.getJSON(Dataurl, data)
        .done(function (data) {
            reloadchart();
            console.log(data);
            resp = data.reports;
            types = data.types;
            updatechart();
        });
}