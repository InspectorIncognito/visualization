$(document).ready(function () {

    var target = document.getElementsByClassName("x_panel")[0];
    var chart;

    function updatechart(data, update) {
        if (update) {
            chart.load({
                data: data
            });
        } else {
            makechart(data, 600);
        }
    }

    function makechart(data, height) {
        var opts = {
            size: {
                height: height
            },
            //xFormat: "%Y-%m-%dT%H:%M:%S%Z",
            //xFormat: null,
            data: {
                json: data,
                keys: {
                    x: "half_hour",
                    value: ["active_users", "reporting_users", "reports"]
                },
                type: "line",
                names: {
                    active_users: "Usuarios activos",
                    reporting_users: "Usuarios que reportan",
                    reports: "Eventos reportados"
                }
            },
            bar: {
                width: {
                    ratio: 0.4
                }
            },
            axis: {
                x: {
                    type: "timeseries",
                    localtime: true,
                    tick: {
                        culling: true,
                        rotate: 45,
                        format: "%Y-%m-%d %H:%M:%S"
                    }
                }
            }
        };
        opts = Object.assign({}, opts);
        chart = c3.generate(opts);
    }

    function updateDays(update) {
        var url = "/carriers/getActiveUsers/";
        var data = {
            date_init: DATE_RANGE_INPUT.data("daterangepicker").startDate.format(),
            date_end: DATE_RANGE_INPUT.data("daterangepicker").endDate.format()
        };

        $(target).spin(spinnerOpt);
        $.getJSON(url, data)
            .done(function (data) {
                updatechart(data["half_hours"], update);
            }).always(function(){
                $(target).spin(false);
            });
    }

    var DATE_RANGE_INPUT = $("#dateRange");

    optionDateRangePicker.startDate = moment().subtract(1, "days");
    DATE_RANGE_INPUT.daterangepicker(optionDateRangePicker);
    DATE_RANGE_INPUT.on("apply.daterangepicker", function() {
        updateDays(true);
    });
    updateDays(false);
});