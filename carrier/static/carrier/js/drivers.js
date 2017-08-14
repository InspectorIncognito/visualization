
DATE_RANGE_INPUT = $("#dateRange");
LICENSE_PLATE_SELECT = $("#licensePlates");
ROUTE_SELECT = $("#routes");
UPDATE_BUTTON = $("#btnUpdateData");

$(function () {
    var optionDateRangePicker = {
        startDate: moment().subtract(29, "days"),
        endDate: moment(),
        dateLimit: {
            days: 60
        },
        alwaysShowCalendars: true,
        showCustomRangeLabel: false,
        showDropdowns: false,
        showWeekNumbers: false,
        timePicker: false,
        timePickerIncrement: 1, // minutes
        timePicker12Hour: true,
        ranges: {
            "Hoy": [moment(), moment()],
            "Ayer": [moment().subtract(1, "days"), moment().subtract(1, "days")],
            "Últimos 7 días": [moment().subtract(6, "days"), moment()],
            "Últimos 30 Días": [moment().subtract(29, "days"), moment()],
            "Este mes": [moment().startOf("month"), moment().endOf("month")],
            "Mes anterior": [moment().subtract(1, "month").startOf("month"), moment().subtract(1, "month").endOf("month")]
        },
        opens: "right",
        buttonClasses: ["btn btn-default"],
        applyClass: "btn-sm btn-success",
        cancelClass: "btn-sm",
        format: "DD/MM/YYYY",
        separator: " to ",
        locale: {
            applyLabel: "Aceptar",
            cancelLabel: "Cancelar",
            fromLabel: "Desde",
            toLabel: "A",
            customRangeLabel: "Elegir",
            daysOfWeek: ["Do", "Lu", "Ma", "Mi", "Ju", "Vi", "Sa"],
            monthNames: ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],
            firstDay: 1
        }
    };
    DATE_RANGE_INPUT.daterangepicker(optionDateRangePicker);

    $("#group :input").change(function () {
        updatechart();
    });
    UPDATE_BUTTON.click(function(){
        myFunction(true);
    });
    myFunction(true);
});

$(document).ready(function () {
    ROUTE_SELECT.select2({
        placeholder: "Todos los recorridos",
        allowClear: true
    });
    LICENSE_PLATE_SELECT.select2({
        placeholder: "Todas las patentes",
        allowClear: true,
        language: {
            noResults: function(){
                return "Sin resultados";
            }
        }
    });
});

var resp = [];
var types = [];
var authorityPeriods = [];
var chartdata = {
    "weekday": null,
    "daytype": null,
    "periodHour": null,
    "periodTransantiago": null,
    "plate": null,
    "service": null,
    "daily": null,
    "monthly": null,
    "yearly": null
};
var chart;

function reloadchart() {
    chartdata = {
        "weekday": null,
        "daytype": null,
        "periodHour": null,
        "periodTransantiago": null,
        "plate": null,
        "service": null,
        "daily": null,
        "monthly": null,
        "yearly": null
    };
}

function updatechart() {
    if (resp !== null) {
        var cols = [];
        function buildDataSource(xAxisLabels, yDataFilter, type, groups) {
            var cols = [];

            var categories = {};
            var answer = {};

            resp.forEach(function(val, i){
                var data = yDataFilter(val);
                if (answer[val.type] === undefined) {
                    answer[val.type] = [];
                }
                answer[val.type][data.x] += data.y;
                categories[data.label] = data.x;
            });

            types.forEach(function(type, i){
                cols.push([type].concat(chartdata["weekday"][i]));
            });

            return {
                columns: cols,
                categories: xAxisLabels,
                height: null,
                x: null,
                xFormat: null,
                groups: groups,
                type: type,
                tickFormat: null
            };
        }
        switch ($("input:checked", "#group").val()) {
            case "weekday":
                el = "weekday";
                dataDict = chartdata[el];
                if (dataDict === null) {
                    xAxisLabels = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sabado", "Domingo"];
                    yDataFilter = function (val) {
                        var date = moment(val.timeCreation, "DD-MM-YYYY HH:mm:SS");
                        xAxisIndex = date.weekday();
                        label = date.format("DDDD");
                        return {
                            label: label,
                            x: xAxisIndex,
                            y: val.eventConfirm
                        };
                    };
                    type = "category";
                    dataDict = buildDataSource(el, xAxisLabels, yDataFilter, type);
                }

                makeChart(dataDict.columns, dataDict.categories, dataDict.height, dataDict.x, dataDict.xFormat, dataDict.groups, dataDict.type, dataDict.tickFormat);
                break;

            case "daytype":
                if (chartdata["daytype"] === null) {
                    chartdata["daytype"] = {
                        "daytypes": [],
                        "daytypetype": types.map(function(){ return []; })
                    };
                    resp.forEach(function(val){
                        var type = val.type;
                        var daytype = val.typeOfDay;
                        if (chartdata["daytype"]["daytypes"].indexOf(daytype) === -1) {
                            chartdata["daytype"]["daytypes"].push(daytype);
                            types.forEach(function(_, j){
                                chartdata["daytype"]["daytypetype"][j].push(0);
                            });
                        }
                        var p = chartdata["daytype"]["daytypes"].indexOf(daytype);
                        chartdata["daytype"]["daytypetype"][type][p] += val.eventConfirm;
                    });
                }
                types.forEach(function(val, i){
                    cols.push([val].concat(chartdata["daytype"]["daytypetype"][i]));
                });
                makeChart(cols, chartdata["daytype"]["daytypes"], null, undefined, null, [], "category", null);
                break;

            case "periodHour":
                if (chartdata["halfhour"] === null) {
                    chartdata["halfhour"] = {
                        "halfhours": [],
                        "halfhourtype": types.map(function(){ return []; })
                    };
                    resp.forEach(function(val){
                        var type = val.type;
                        var halfhour = val.periodHour;
                        if (chartdata["halfhour"]["halfhours"].indexOf(halfhour) === -1) {
                            chartdata["halfhour"]["halfhours"].push(halfhour);
                            types.forEach(function(_, j){
                                chartdata["halfhour"]["halfhourtype"][j].push(0);
                            });
                        }
                        var p = chartdata["halfhour"]["halfhours"].indexOf(halfhour);
                        chartdata["halfhour"]["halfhourtype"][type][p] += val.eventConfirm;
                    });
                }
                types.forEach(function(val, i){
                    cols.push([val].concat(chartdata["halfhour"]["halfhourtype"][i]));
                });
                makeChart(cols, chartdata["halfhour"]["halfhours"], null, undefined, null, [], "category", null);
                break;

            case "periodTransantiago":
                var el = "periodTransantiago";
                if (chartdata[el] === null) {
                    chartdata[el] = {
                        "periods": null,
                        "periodtype": types.map(function(){ return []; })
                    };

                    var dataDict = {};

                    resp.forEach(function(val, i){
                        var type = ""+val.type;
                        var periodName = val.periodTransantiago;

                        if (!(periodName in dataDict)) {
                            dataDict[periodName] = {};
                            types.map(function(_, j){ dataDict[periodName][""+j] = 0; });
                        }
                        dataDict[periodName][type] += val.eventConfirm;
                    });

                    var typeArray = types.map(function(){ return []; });
                    authorityPeriods.forEach(function(name, i){
                        typeArray.forEach(function(type, i){
                            var value = 0;
                            if (name in dataDict){
                                value = dataDict[name][i];
                            }
                            type.push(value);
                        });
                    });

                    chartdata[el]["periods"] = authorityPeriods;
                    chartdata[el]["periodtype"] = typeArray;
                }
                types.forEach(function(val, i){
                    cols.push([types[i]].concat(chartdata[el]["periodtype"][i]));
                });
                makeChart(cols, chartdata[el]["periods"], null, undefined, null, [], "category", null);
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
                for (i = 0; i < types.length; i++) {
                    cols.push([types[i]].concat(chartdata["plate"]["platetype"][i]));
                }
                makeChart(cols, chartdata["plate"]["plates"], null, undefined, null, [], "category", null);
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
                for (i = 0; i < types.length; i++) {
                    cols.push([types[i]].concat(servicetype[i]));
                }
                makeChart(cols, services, null, undefined, null, [], "category", null);
                break;

            case "daily":
                if (chartdata["daily"] === null) {
                    var days = [];
                    var daystype = types.map(function(){ return []; });
                    for (i = 0; i < resp.length; i++) {
                        var type = resp[i]["type"];
                        var day = moment(resp[i]["timeCreation"], "DD-MM-YYYY HH:mm:SS").format("DD-MM-YYYY");

                        if (days.indexOf(day) === -1) {
                            days.push(day);
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
                makeChart(cols, null, null, "x", "%d-%m-%Y", [types], "timeseries", "%d-%m-%Y");
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
                makeChart(cols, null, null, "x", "%m-%Y", [types], "timeseries", "%m-%Y");
                break;
            case "yearly":
                if (chartdata["yearly"] === null) {
                    var years = [];
                    var yearstype = types.map(function(){ return []; });
                    for (i = 0; i < resp.length; i++) {
                        var type = resp[i]["type"];
                        var year = moment(resp[i]["timeCreation"], "DD-MM-YYYY HH:mm:SS").format("YYYY");

                        if (years.indexOf(year) === -1) {
                            years.push(year);
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
                makeChart(cols, null, null, "x", "%Y", [types], "timeseries", "%Y");
                break;
        }
    }
}

function makeChart(columns, categories, height, x, xFormat, groups, type, tickFormat) {
    var opts = {
        size: {
            height: height
        },
        data: {
            x: x,
            xFormat: xFormat,
            columns: columns,
            type: "bar",
            groups: groups
        },
        bar: {
            width: {
                ratio: 0.4
            }
        },
        axis: {
            x: {
                type: type, // timeseries, category, indexed
                tick: {
                    culling: false,
                    rotate: 45,
                    format: tickFormat
                },
                categories: categories
            }
        }
    };
    chart = c3.generate(opts);
}

var spinnerOpt = {
    scale: 4,
    color: "#169F85",
    top: "80px"
};
var target = document.getElementById("filters");
var spinner = new Spinner(spinnerOpt).spin(target);

function myFunction(refresh) {
    const URL = "http://" + location.host + "/carriers/getDriversData/";

    var data = {
        date_init: DATE_RANGE_INPUT.data("daterangepicker").startDate.format(),
        date_end: DATE_RANGE_INPUT.data("daterangepicker").endDate.format()
    };

    var routes = ROUTE_SELECT.val();
    var licensePlates = LICENSE_PLATE_SELECT.val();
    if (routes !== null) {
        data["routes"] = JSON.stringify(routes);
    }
    if (licensePlates !== null) {
        data["licensePlates"] = JSON.stringify(licensePlates);
    }

    // activate spinner
    spinner.spin(target);
    $.getJSON(URL, data)
        .done(function (data) {
            console.log(data);

            if (refresh) {
                LICENSE_PLATE_SELECT.find("option").remove().val("");
                //LICENSE_PLATE_SELECT.val(null).trigger("change");


                // order by license plates with reports
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
                $.each(top, function (key, value) {
                    if ($.inArray(value, licensePlates) >= 0) {
                        values.push(value);
                    }

                    LICENSE_PLATE_SELECT.append($("<option>", {
                        value: value,
                        text: value
                    }));
                });
                bottom.sort();
                /*
                $.each(bottom, function (index, value) {
                    LICENSE_PLATE_SELECT.append($("<option>", {
                        value: value,
                        text: value + " (No hay datos)",
                    }));
                });
                LICENSE_PLATE_SELECT.val(values).trigger("change");*/
            }

            reloadchart();
            resp = data.reports;
            types = data.types;
            console.log(types);
            authorityPeriods = data.authorityPeriods;
            updatechart();
        }).always(function(){
            // hide spinner
            spinner.stop();
        });
}
