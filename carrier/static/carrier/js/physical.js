
$(document).ready(function () {
    var DATE_RANGE_INPUT = $("#dateRange");
    var LICENSE_PLATE_SELECT = $("#licensePlates");
    var UPDATE_BUTTON = $("#btnUpdateData");

    optionDateRangePicker.startDate = moment().subtract(3, "months");
    DATE_RANGE_INPUT.daterangepicker(optionDateRangePicker);

    $("#group :input").change(function () {
        updatechart();
    });

    LICENSE_PLATE_SELECT.select2({
        placeholder: "Todas las patentes",
        allowClear: true
    });

    UPDATE_BUTTON.click(function(){
        myFunction(true);
    });

    var resp = null;
    var types = 0;
    var chart;
    var chartdata = {
        "weekday": null,
        "plate": null,
        "service": null,
        "daily": null,
        "monthly": null,
        "yearly": null
    };

    function reloadchart() {
        chartdata = {
            "weekday": null,
            "plate": null,
            "service": null,
            "daily": null,
            "monthly": null,
            "yearly": null
        };
    }

    function updatechart() {
        if (resp !== null) {
            switch ($("input:checked", "#group").val()) {
                case "weekday":
                    if (chartdata["weekday"] === null) {
                        chartdata["weekday"] = [];
                        for (i = 0; i < types.length; i++) {
                            chartdata["weekday"].push([0, 0, 0, 0, 0, 0, 0]);
                        }
                        for (i = 0; i < resp.length; i++) {
                            var type = resp[i]["type"];
                            var day = (moment(resp[i]["timeCreation"], "DD-MM-YYYY HH:mm:SS").day() + 6) % 7;
                            chartdata["weekday"][type][day] += resp[i]["eventConfirm"];
                        }
                    }
                    var cols = [];
                    for (i = 0; i < types.length; i++) {
                        cols.push([types[i]].concat(chartdata["weekday"][i]));
                    }
                    makechart(cols, ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"], null, null, null, [], "category", null);
                    break;

                case "plate":
                    if (chartdata["plate"] === null) {
                        chartdata["plate"] = {
                            "plates": [],
                            "platetype": types.map(function(){ return []; })
                        };
                        for (i = 0; i < resp.length; i++) {
                            var type = resp[i]["type"];
                            var plate = resp[i]["plate"];
                            if (chartdata["plate"]["plates"].indexOf(plate) === -1) {
                                chartdata["plate"]["plates"].push(plate);
                                for (var j = 0; j < types.length; j++) {
                                    chartdata["plate"]["platetype"][j].push(0);
                                }
                            }
                            var p = chartdata["plate"]["plates"].indexOf(plate);
                            chartdata["plate"]["platetype"][type][p] += resp[i]["eventConfirm"];
                        }
                    }
                    var cols = [];
                    for (i = 0; i < types.length; i++) {
                        cols.push([types[i]].concat(chartdata["plate"]["platetype"][i]));
                    }
                    makechart(cols, chartdata["plate"]["plates"], null, undefined, null, [], "category", null);
                    break;

                case "service":
                    if (chartdata["service"] === null) {
                        var services = [];
                        var servicetype = types.map(function(){ return []; });
                        for (i = 0; i < resp.length; i++) {
                            var type = resp[i]["type"];
                            var service = resp[i]["service"];
                            if (services.indexOf(service) === -1) {
                                services.push(service);
                                for (var j = 0; j < types.length; j++) {
                                    servicetype[j].push(0);
                                }
                            }
                            var p = services.indexOf(service);
                            servicetype[type][p] += resp[i]["eventConfirm"];
                        }
                    }
                    var cols = [];
                    for (i = 0; i < types.length; i++) {
                        cols.push([types[i]].concat(servicetype[i]));
                    }
                    makechart(cols, services, null, undefined, null, [], "category", null);
                    break;

                case "daily":
                    if (chartdata["daily"] === null) {
                        var days = [];
                        var daystype = types.map(function(){ return []; });
                        for (i = 0; i < resp.length; i++) {
                            var type = resp[i]["type"];
                            var day = moment(resp[i]["timeCreation"], "DD-MM-YYYY HH:mm:SS").format("DD-MM-YYYY");

                            if (days.indexOf(day) === -1) {
                                days.push(day)
                                for (var j = 0; j < types.length; j++) {
                                    daystype[j].push(0);
                                }
                            }
                            var p = days.indexOf(day);
                            daystype[type][p] += resp[i]["eventConfirm"];
                        }
                    }
                    var cols = days;
                    cols.unshift("x");
                    cols = [cols];
                    for (i = 0; i < types.length; i++) {
                        cols.push([types[i]].concat(daystype[i]));
                    }
                    makechart(cols, null, null, "x", "%d-%m-%Y", [types], "timeseries", "%d-%m-%Y");
                    break;
                case "monthly":
                    if (chartdata["monthly"] === null) {
                        var months = [];
                        var monthstype = types.map(function(){ return []; });
                        for (i = 0; i < resp.length; i++) {
                            var type = resp[i]["type"];
                            var month = moment(resp[i]["timeCreation"], "DD-MM-YYYY HH:mm:SS").format("MM-YYYY");

                            if (months.indexOf(month) === -1) {
                                months.push(month);
                                for (var j = 0; j < types.length; j++) {
                                    monthstype[j].push(0);
                                }
                            }
                            var p = months.indexOf(month);
                            monthstype[type][p] += resp[i]["eventConfirm"];
                        }
                    }
                    var cols = months;
                    cols.unshift("x");
                    cols = [cols];
                    for (i = 0; i < types.length; i++) {
                        cols.push([types[i]].concat(monthstype[i]));
                    }
                    makechart(cols, null, null, "x", "%m-%Y", [types], "timeseries", "%m-%Y");
                    break;
                case "yearly":
                    if (chartdata["yearly"] === null) {
                        var years = [];
                        var yearstype = types.map(function(){ return []; });
                        for (i = 0; i < resp.length; i++) {
                            var type = resp[i]["type"];
                            var year = moment(resp[i]["timeCreation"], "DD-MM-YYYY HH:mm:SS").format("YYYY");

                            if (years.indexOf(year) === -1) {
                                years.push(year)
                                for (var j = 0; j < types.length; j++) {
                                    yearstype[j].push(0);
                                }
                            }
                            var p = years.indexOf(year);
                            yearstype[type][p] += resp[i]["eventConfirm"];
                        }
                    }
                    var cols = years;
                    cols.unshift("x");
                    cols = [cols];
                    for (i = 0; i < types.length; i++) {
                        cols.push([types[i]].concat(yearstype[i]));
                    }
                    makechart(cols, null, null, "x", "%Y", [types], "timeseries", "%Y");
                    break;
            }
        }
    }
    function makechart(columns, categories, height, x, xformat, groups, type, tickformat) {
        chart = c3.generate({
            size: {
                height: height
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

    var target = document.getElementsByClassName("x_content")[0];
    var spinner = new Spinner(spinnerOpt);

    function myFunction(refresh) {
        var Dataurl = "/carriers/getPhysicalData/";

        var data = {
            date_init: DATE_RANGE_INPUT.data("daterangepicker").startDate.format(),
            date_end: DATE_RANGE_INPUT.data("daterangepicker").endDate.format()
        };
        var licensePlates = LICENSE_PLATE_SELECT.val();
        console.log(licensePlates);
        if (licensePlates !== null) {
            data["license_plates[]"] = licensePlates;
        }

        // activate spinner
        spinner.spin(target);
        $.getJSON(Dataurl, data)
            .done(function (data) {
                console.log(data);
                if (refresh) {
                    $(".select2_plate").find("option").remove().val("");
                    //$("#plate").val(null).trigger("change");
                    var top = [];
                    var bottom = [];
                    $.each(data.allplates, function (key, value) {
                        if (value) {
                            top.push(key);
                        }
                        else {
                            bottom.push(key);
                        }
                    });
                    top.sort();
                    values = [];
                    $.each(top, function (index, value) {
                        if ($.inArray(value, licensePlates) >= 0) {
                            values.push(value);
                        }
                        LICENSE_PLATE_SELECT.append($("<option>", {
                            value: value,
                            text: value
                        }));
                    });
                    /*
                    bottom.sort();
                    $.each(bottom, function (index, value) {
                        $('.select2_plate').append($('<option>', {
                            value: value,
                            text: value + " (No hay datos)",
                        }));
                    });
                    $("#plate").val(values).trigger("change");*/
                }
                reloadchart();
                resp = data.reports;
                types = data.types;
                updatechart();
            }).always(function(){
                // hide spinner
                spinner.stop();
            });
    }
    function headers() {
        var URL = "/carriers/getPhysicalHeaders/";
        $.getJSON(URL)
            .done(function (data) {
                var html = '';
                $.each(data, function (key, number) {
                    html += '<div class="col-md-2 col-sm-4 col-xs-6 tile_stats_count">';
                    html += '<span class="count_top" title="' + key + '">' + key + '</span>';
                    html += '<div class="count" style="text-align:center">' + number + '</div>';
                    html += '</div>'
                });
                $("#headers").html(html);
            });
    }
    headers();
    UPDATE_BUTTON.click();
});