$(function () {
    $('input').iCheck();
    $('#date_init').datetimepicker({
        format: 'LL'
    });
    $('#date_end').datetimepicker({
        format: 'LL'
    });
    $('#hour1').datetimepicker({
        format: 'LT'
    });
    $('#hour2').datetimepicker({
        format: 'LT'
    });
    $('input').iCheck({
        checkboxClass: 'icheckbox_flat-blue',
        radioClass: 'iradio_flat-blue'
    });
});

var test = 0;

var chart = c3.generate({
    data: {
        x: 'x',
//        xFormat: '%Y%m%d', // 'xFormat' can be used as custom format of 'x'
        columns: [
            ['x', '2013-01-01', '2013-01-02', '2013-01-03', '2013-01-04', '2013-01-05', '2013-01-06'],
//            ['x', '20130101', '20130102', '20130103', '20130104', '20130105', '20130106'],
            ['data1', 30, 200, 100, 400, 150, 250],
            ['data2', 130, 340, 200, 500, 250, 350]
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

setTimeout(function () {
    chart.unload({
        ids: ['data2']
    });
}, 1000);

function myFunction() {
    var flickerAPI = "http://localhost:8000/carriers/getDriversData/";
    var data = {
        date_init: $('#date_init').data("DateTimePicker").date().format("YYYY-MM-DD"),
        date_end: $('#date_end').data("DateTimePicker").date().format("YYYY-MM-DD"),
        hour1: '1',
        hour2: '20'
    };

    $.getJSON(flickerAPI, data)
        .done(function (data) {
            console.log(data);
        });


    console.log($('#date_init').data("DateTimePicker").date().toDate());

    console.log(document.getElementById("date_end").value);
    console.log(document.getElementById("hour1").value);
    console.log(document.getElementById("hour2").value);
    console.log(document.getElementById("service").value);
    console.log(document.getElementById("plate").value);
}