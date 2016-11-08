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
    $("#filters").on("dp.change", function (e) {
        myFunction();
    });
    $("#filters :input").keyup(function () {
        myFunction();
    });
    myFunction();
});
$(document).ready(function () {
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
                    for (i = 0; i < resp.length; i++) {
                        var type = resp[i]['type'];
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
            case "daily":
                if (chartdata['daily'] == null) {
                    var days = [];
                    var daystype = [];
                    for (i = 0; i < types.length; i++) {
                        daystype.push([]);
                    }
                    for (i = 0; i < resp.length; i++) {
                        var type = resp[i]['type'];
                        var day = moment(resp[i]['timeCreation'], "DD-MM-YYYY HH:mm:SS").format("DD-MM-YYYY")

                        if (days.indexOf(day) == -1) {
                            days.push(day)
                            for (var j = 0; j < types.length; j++) {
                                daystype[j].push(0);
                            }
                        }
                        var p = days.indexOf(day);
                        daystype[type][p]++;
                    }
                }
                var cols = days;
                cols.unshift("x");
                cols = [cols];
                for (i = 0; i < types.length; i++) {
                    cols.push([types[i]].concat(daystype[i]));
                }
                chart = c3.generate({
                    size: {
                        height: 600,
                    },
                    data: {
                        x: 'x',
                        xFormat: '%d-%m-%Y',
                        columns: cols,
                        type: 'bar',
                        groups: [types]
                    },
                    axis: {
                        x: {
                            type: 'timeseries',
                            tick: {
                                culling: false,
                                rotate: 90,
                                format: '%d-%m-%Y'
                            }

                        }
                    },
                    subchart: {
                        show: $('#date_end').data("DateTimePicker").date().diff($('#date_init').data("DateTimePicker").date(), 'months') > 2
                    }
                });
                break;
            case "monthly":
                if (chartdata['monthly'] == null) {
                    var months = [];
                    var monthstype = [];
                    for (i = 0; i < types.length; i++) {
                        monthstype.push([]);
                    }
                    for (i = 0; i < resp.length; i++) {
                        var type = resp[i]['type'];
                        var month = moment(resp[i]['timeCreation'], "DD-MM-YYYY HH:mm:SS").format("MM-YYYY")

                        if (months.indexOf(month) == -1) {
                            months.push(month)
                            for (var j = 0; j < types.length; j++) {
                                monthstype[j].push(0);
                            }
                        }
                        var p = months.indexOf(month);
                        monthstype[type][p]++;
                    }
                }
                var cols = months;
                cols.unshift("x");
                cols = [cols];
                for (i = 0; i < types.length; i++) {
                    cols.push([types[i]].concat(monthstype[i]));
                }
                chart = c3.generate({
                    data: {
                        x: 'x',
                        xFormat: '%m-%Y',
                        columns: cols,
                        type: 'bar',
                        groups: [types]
                    },
                    bar: {
                        width: {
                            ratio: 0.4
                        }
                    },
                    axis: {
                        x: {
                            type: 'timeseries',
                            tick: {
                                culling: false,
                                rotate: 90,
                                format: '%m-%Y'
                            }

                        }
                    }
                });
                break;
        }
    }
}

function updateDate(n) {
    switch (n) {
        case 1:
            $('#date_init').data("DateTimePicker").date(moment());
            $('#date_end').data("DateTimePicker").date(moment());
            break;
        case 2:
            $('#date_init').data("DateTimePicker").date(moment().subtract(1, 'months'));
            $('#date_end').data("DateTimePicker").date(moment());
            break;
        case 3:
            $('#date_init').data("DateTimePicker").date(moment().subtract(3, 'months'));
            $('#date_end').data("DateTimePicker").date(moment());
            break;
    }
}


function myFunction() {
    var Dataurl = "http://" + location.host + "/carriers/getPhysicalData/";
    var data = {
        carrier: '3',
        date_init: $('#date_init').data("DateTimePicker").date().format("YYYY-MM-DD"),
        date_end: $('#date_end').data("DateTimePicker").date().format("YYYY-MM-DD"),
        hour1: 00,
        hour2: 23,
        minute1: 00,
        minute2: 59
    };
    /*
     var service = $(".select2_multiple").val();
     var plate = $(".select2_plate").val();
     if (service != null) data['service'] = JSON.stringify(service);
     if (plate != null) data['plate'] = JSON.stringify(plate);
     */

    $.getJSON(Dataurl, data)
        .done(function (data) {
            console.log(data)
            reloadchart();
            resp = data.reports;
            types = data.types;
            updatechart();
        });
}
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
};
headers();
setInterval(function () {
    headers();
}, 30000);