/**
 * Created by patricio on 11/29/16.
 */
var selecturl = 'http://' + location.host + '/carriers/getBusMapParameters';
var reports = {};
var map;
var routeGroup;
var categories = {};

$(function () {
    $('#date_init').datetimepicker({
        defaultDate: moment().subtract(3, 'months'),
        format: 'LL'
    });
    $('#date_end').datetimepicker({
        defaultDate: moment(),
        format: 'LL'
    });
    $("#filters").on("dp.change", function (e) {
        reloadData();
    });
    $("#service").change(function () {
        reloadData();
    });
    $("#plate").change(function () {
        reloadData();
    });
    $("#comuna").change(function () {
        reloadData();
    });

});


$(document).ready(function () {
    $(".select2_service").select2({
        placeholder: "Todos los recorridos",
        allowClear: true
    });
    $(".select2_plate").select2({
        placeholder: "Todas las patentes",
        allowClear: true
    });
    $(".select2_comuna").select2({
        placeholder: "Todas las comunas",
        allowClear: true
    });

    $.getJSON(selecturl)
        .done(function (data) {
            console.log(data.types)
            for (var key in data.types) {
                categories[key] = {}
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
    }, "/static/", "datasantiago");

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

function reloadData() {
    var Dataurl = 'http://' + location.host + '/carriers/getBusMap/';
    var data = {
        date_init: $('#date_init').data("DateTimePicker").date().format("YYYY-MM-DD"),
        date_end: $('#date_end').data("DateTimePicker").date().add(1, 'days').format("YYYY-MM-DD")
    };
    var service = $(".select2_service").val();
    console.log(service)
    var plate = $(".select2_plate").val();
    var comuna = $(".select2_comuna").val();
    if (service != null) data['service'] = JSON.stringify(service);
    if (plate != null) data['plate'] = JSON.stringify(plate);
    if (comuna != null) data['comuna'] = JSON.stringify(comuna);

    $.getJSON(Dataurl, data)
        .done(function (data) {
            console.log(data);
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

            for (var i = 0; i < service.length; i++) {
                routeGroup.addLayer(reports[service[i]].routeLayer);
            }

            for (var key in data.data) {
                for (var i = 0; i < data.data[key].length; i++) {
                    var report = data.data[key][i];
                    console.log(report)
                    marker = L.marker([report.lat, report.lon], {}).bindPopup("Servicio: " + key + "<br>Fecha: " + report.report.timeStamp + "<br>Tipo: " + report.report.category + "-" + report.report.type);
                    categories[report.report.category][report.report.type].addLayer(marker);
                }
            }

        });
}