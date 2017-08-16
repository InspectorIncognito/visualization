/**
 * Created by patricio on 11/29/16.
 */
var selecturl = "/carriers/getBusMapParameters";
var reports = {};
var map;
var routeGroup;
var categories = {};

$(document).ready(function () {
    var DATE_RANGE_INPUT = $("#dateRange");
    var ROUTES = $("#routes");
    var LICENSE_PLATES = $("#licensePlates");
    var COMMUNES = $("#communes");

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

    $.getJSON(selecturl)
        .done(function (data) {
            //console.log(data.types)
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
            fillSelect(data);
            createMap();
        });
});

function createMap() {
    var beauchefLocation = L.latLng(-33.4579141, -70.6646977);
    map = L.map("mapid", {editable: true}).setView(beauchefLocation, 15);


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


    function reloadData() {
        var Dataurl = "/carriers/getBusMap/";

        var data = {
            date_init: DATE_RANGE_INPUT.data("daterangepicker").startDate.format(),
            date_end: DATE_RANGE_INPUT.data("daterangepicker").endDate.format()
        };

        var routes = ROUTES.val();
        var licensePlates = LICENSE_PLATES.val();
        var communes = COMMUNES.val();
        if (routes !== null) data['routes[]'] = routes;
        if (licensePlates !== null) data['licensePlates[]'] = licensePlates;
        if (communes !== null) data['communes[]'] = communes;

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
                }
                else {
                    for (var i = 0; i < routes.length; i++) {
                        routeGroup.addLayer(reports[routes[i]].routeLayer);
                    }
                }

                for (var i = 0; i < data.data.length; i++) {
                    var report = data.data[i];
                    //console.log(report)
                    marker = L.marker([report.lat, report.lon], {}).bindPopup("Servicio: " + report.report.service +
                            "<br>Sentido: " + report.report.direction +
                            "<br>Fecha: " + report.report.timeStamp +
                            "<br>Tipo: " + report.report.category + "-" + report.report.type +
                            "<br>Patente: " + report.report.plate);
                    categories[report.report.category][report.report.type].addLayer(marker);
                }
            });
    }
    reloadData();
}

function fillSelect(d) {
    for (var i = 0; i < d.services.length; i++) {
        $('#service').append($('<option>', {
            value: d.services[i],
            text: d.services[i]
        }));
    }
    for (var i = 0; i < d.plates.length; i++) {
        $('#plate').append($('<option>', {
            value: d.plates[i],
            text: d.plates[i]
        }));
    }
    for (var i = 0; i < d.comunas.length; i++) {
        $('#comuna').append($('<option>', {
            value: d.comunas[i],
            text: d.comunas[i]
        }));
    }
}
