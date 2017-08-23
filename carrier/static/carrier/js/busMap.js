/**
 * Created by patricio on 11/29/16.
 */
$(document).ready(function () {
    var reports = {};
    var map;
    var routeGroup;
    var categories = {};

    var DATE_RANGE_INPUT = $("#dateRange");
    var ROUTES = $("#routes");
    var LICENSE_PLATES = $("#licensePlates");
    var COMMUNES = $("#communes");
    var BUTTON = $("#btnUpdateData");

    var target = document.getElementsByClassName("x_panel")[0];
    var spinner = new Spinner(spinnerOpt).spin(target);

    DATE_RANGE_INPUT.daterangepicker(optionDateRangePicker);
    ROUTES.select2({
        placeholder: "Todos los servicios",
        allowClear: true
    });
    LICENSE_PLATES.select2({
        placeholder: "Todas las patentes",
        allowClear: true
    });
    COMMUNES.select2({
        placeholder: "Todas las comunas",
        allowClear: true
    });

    BUTTON.click(function () {
        updateData();
    });

    function updateData() {
        // activate spinner
        spinner.spin(target);
        var Dataurl = "/carriers/getBusMap/";

        var data = {
            date_init: DATE_RANGE_INPUT.data("daterangepicker").startDate.format(),
            date_end: DATE_RANGE_INPUT.data("daterangepicker").endDate.format()
        };

        var routes = ROUTES.val();
        var licensePlates = LICENSE_PLATES.val();
        var communes = COMMUNES.val();
        if (routes !== null) data["routes[]"] = routes;
        if (licensePlates !== null) data["licensePlates[]"] = licensePlates;
        if (communes !== null) data["communes[]"] = communes;

        $.getJSON(Dataurl, data)
            .done(function (data) {
                routeGroup.eachLayer(function (layer) {
                    map.removeLayer(layer);
                });
                for (var cat in categories) {
                    for (var subcat in categories[cat]) {
                        categories[cat][subcat].eachLayer(function (layer) {
                            categories[cat][subcat].removeLayer(layer)
                        });
                    }
                }
                if (routes === null) {
                    for (var key in reports) {
                        routeGroup.addLayer(reports[key].routeLayer);
                    }
                } else {
                    for (var i = 0; i < routes.length; i++) {
                        routeGroup.addLayer(reports[routes[i]].routeLayer);
                    }
                }

                for (var i = 0; i < data.data.length; i++) {
                    var report = data.data[i];
                    marker = L.marker([report.lat, report.lon], {}).bindPopup("Servicio: " + report.report.service +
                        "<br>Sentido: " + report.report.direction +
                        "<br>Fecha: " + report.report.timeStamp +
                        "<br>Tipo: " + report.report.category + "-" + report.report.type +
                        "<br>Patente: " + report.report.plate);
                    categories[report.report.category][report.report.type].addLayer(marker);
                }
            }).always(function () {
            spinner.stop();
        });
    }

    (function () {
        // activate spinner
        spinner.spin(target);
        var URL = "/carriers/getBusMapParameters";
        $.getJSON(URL)
            .done(function (data) {
                console.log(data);
                for (var key in data.types) {
                    categories[key] = {};
                    for (var i = 0; i < data.types[key].length; i++) {
                        categories[key][data.types[key][i]] = L.layerGroup([]);
                    }
                }
                for (var i = 0; i < data.services.length; i++) {
                    reports[data.services[i]] = {};
                    reports[data.services[i]].routeLayer = L.layerGroup([]);
                    reports[data.services[i]].reportsLayer = {};
                    for (var cat in categories) {
                        reports[data.services[i]].reportsLayer[cat] = {};
                        for (var subcat in categories[cat]) {
                            reports[data.services[i]].reportsLayer[cat][subcat] = L.layerGroup([]);
                        }
                    }
                }
                createMap();
            }).always(function () {
            spinner.stop();
        });
    })();

    function createMap() {
        var beauchefLocation = L.latLng(-33.4579141, -70.6646977);
        map = L.map("mapid", {editable: false}).setView(beauchefLocation, 12);

        routeGroup = L.layerGroup([]);

        var overlays = {
            "ruta": routeGroup
        };

        L.control.groupedLayers(overlays, categories, {groupCheckboxes: true}).addTo(map);

        GTFS.loadData(function () {
            var baseLayer = GTFS.setLayerControl(map);
            for (var key in reports) {
                try {
                    reports[key].routeLayer = L.layerGroup([]);
                    GTFS.drawRoutes(reports[key].routeLayer, GTFS.getRoutes([key + "I", key + "R"]));
                }
                catch (err) {
                }
            }
        }, "/static/carrier/", "datasantiago");
        updateData();
    }
});