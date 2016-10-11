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
});

var resp = 0;
var types = 0;
var chartdata = {
    'weekday': 0,
    'plate': 0,
    'service': 0,
    'daily': 0,
    'monthly': 0
};
var chart;
function reloadchart() {
    chartdata = {
        'weekday': 0,
        'plate': 0,
        'service': 0,
        'daily': 0,
        'monthly': 0
    };
}
function updatecharhgrethert() {
    chart = c3.generate({
        data: {
            x: 'x',
//        xFormat: '%Y%m%d', // 'xFormat' can be used as custom format of 'x'
            columns: [
                ['x', '2013-01-01', '2013-01-02', '2013-01-03', '2013-01-04', '2013-01-05', '2013-01-06'],
//            ['x', '20130101', '20130102', '20130103', '20130104', '20130105', '20130106'],
                ['data1', 100, 200, 100, 400, 150, 250],
                ['data2', 130, 340, 200, 100, 250, 350]
            ],
            type: 'bar',
            groups: [
                ['data1', 'data2']
            ]
        },
        axis: {
            x: {
                type: 'timeseries',
                tick: {
                    format: '%Y-%m-%d'
                }
            }
        }
    });
}
function updatechart() {
    if (true) {
        switch ($('input:checked', '#group').val()) {
            case "weekday":
                if (chartdata['weekday'] == 0) {
                    chartdata['weekday'] = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]];
                    console.log(chartdata['weekday']);
                    for (i = 0; i < resp.length; i++) {
                        var type = resp[i]['type'];
                        console.log(type);
                        var day = (moment(resp[i]['timeCreation'], "DD-MM-YYYY HH:mm:SS").day() + 6) % 7;
                        chartdata['weekday'][type][day]++;
                    }
                }
                chart = c3.generate({
                    data: {
                        columns: [
                            [types[0]].concat(chartdata['weekday'][0]),
                            [types[1]].concat(chartdata['weekday'][1]),
                            [types[2]].concat(chartdata['weekday'][2]),
                            [types[3]].concat(chartdata['weekday'][3])
                        ],
                        type: 'bar',

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
                if (chartdata['plate'] == 0) {
                    var plates = [];
                    platetype = [[], [], [], []];
                    for (i = 0; i < resp.length; i++) {
                        var type = resp[i]['type'];
                        var plate = resp[i]['plate'];
                        console.log(plate)
                        if (plates.indexOf(plate) == -1) {
                            plates.push(plate)
                            platetype[0].push(0);
                            platetype[1].push(0);
                            platetype[2].push(0);
                            platetype[3].push(0);
                        }
                        var p = plates.indexOf(plate);
                        platetype[type][p]++;
                    }
                }
                chart = c3.generate({
                    data: {
                        columns: [
                            [types[0]].concat(platetype[0]),
                            [types[1]].concat(platetype[1]),
                            [types[2]].concat(platetype[2]),
                            [types[3]].concat(platetype[3])
                        ],
                        type: 'bar',

                    },
                    axis: {
                        x: {
                            type: 'category',
                            tick: {
                                rotate: 90,
                                multiline: false
                            },
                            categories: plates
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
                if (chartdata['service'] == 0) {
                    var services = [];
                    servicetype = [[], [], [], []];
                    for (i = 0; i < resp.length; i++) {
                        var type = resp[i]['type'];
                        var service = resp[i]['service'];
                        console.log(service)
                        if (services.indexOf(service) == -1) {
                            services.push(service)
                            servicetype[0].push(0);
                            servicetype[1].push(0);
                            servicetype[2].push(0);
                            servicetype[3].push(0);
                        }
                        var p = services.indexOf(service);
                        servicetype[type][p]++;
                    }
                }
                chart = c3.generate({
                    data: {
                        columns: [
                            [types[0]].concat(servicetype[0]),
                            [types[1]].concat(servicetype[1]),
                            [types[2]].concat(servicetype[2]),
                            [types[3]].concat(servicetype[3])
                        ],
                        type: 'bar',

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
    var Dataurl = "http://localhost:8000/carriers/getDriversData/";
    var data = {
        carrier: '3',
        date_init: $('#date_init').data("DateTimePicker").date().format("YYYY-MM-DD"),
        date_end: $('#date_end').data("DateTimePicker").date().format("YYYY-MM-DD"),
        hour1: $('#hour1').data("DateTimePicker").date().format("HH"),
        hour2: $('#hour2').data("DateTimePicker").date().format("HH"),
        minute1: $('#hour1').data("DateTimePicker").date().format("mm"),
        minute2: $('#hour2').data("DateTimePicker").date().format("mm")
    };
    var service = document.getElementById("service").value;
    var plate = document.getElementById("plate").value;
    if (service != '') data['service'] = service;
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