$(function () {
    $('#date_filter').datetimepicker({
        defaultDate: moment().subtract(3, 'months'),
        // defaultDate: moment(),
        format: 'LL'
    });
    $("#filters").on("dp.change", function (e) {
        myFunction(true);
    });
    myFunction(true);
});


var resp = null;
var types = 0;
var chartdata = {
    'weekday': null,
    'daytype': null,
    'periodHour': null,
    'periodTransantiago': null,
    'plate': null,
    'service': null,
    'daily': null,
    'monthly': null,
    'yearly': null
};
var chart;
function reloadchart() {
    chartdata = {
        'weekday': null,
        'daytype': null,
        'periodHour': null,
        'periodTransantiago': null,
        'plate': null,
        'service': null,
        'daily': null,
        'monthly': null,
        'yearly': null
    };
}

function updatechart() {
    if (resp != null) {

    }
}

function makechart(columns, categories, height, x, xformat, groups, type, tickformat) {
    chart = c3.generate({
        size: {
            height: height,
        },
        data: {
            x: x,
            xFormat: xformat,
            columns: columns,
            type: 'bar',
            groups: groups
        },
        bar: {
            width: {
                ratio: 0.4
            }
        },
        axis: {
            x: {
                type: type,
                tick: {
                    culling: false,
                    rotate: 45,
                    format: tickformat
                },
                categories: categories

            }
        }
    });
}


// # http://localhost/carriers/getActiveUsers/?date=2016-10-24
// # {
// #   "half_hours": [
// #       {
// #           "half_hour": "2016-10-24 00:00:00-03:00 2016-10-25 00:29:59-03:00",
// #           "active_events": 1419,
// #           "active_users": 2,
// #           "reporting_users": 0,
// #           "reports": 0
// #       },
// #       ...
// # ]}
function myFunction(refresh) {
    var url = "http://" + location.host + "/carriers/getActiveUsers/";
    var url_opts = {
        date_init: $('#date_filter').data("DateTimePicker").date().format("YYYY-MM-DD")
    };

    $.getJSON(url, url_opts)
        .done(function (data) {
            if (refresh) {

            }
            console.log(data);
            reloadchart();
            updatechart();
        });
}
