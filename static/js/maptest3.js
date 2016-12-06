/**
 * Created by patricio on 11/29/16.
 */
var url = 'http://' + location.host + '/carriers/getMap/';
var reports;
var map;

$(document).ready(function () {
    /**
     * SET MAP
     */
    $(".select2_multiple").select2({
        allowClear: true
    });
    $.getJSON(url)
        .done(function (data) {
            reports = data;
            rest();


        });
})

function rest() {
    var beauchefLocation = L.latLng(-33.4579141, -70.6646977);
    map = L.map("mapid", {editable: true}).setView(beauchefLocation, 15);

    var routeGroup = L.layerGroup([]);
    var reportsGroup = L.layerGroup([]);

    var overlays = {
        "ruta": routeGroup,
        "reportes": reportsGroup
    };

    L.control.layers({}, overlays).addTo(map);

    for (var key in reports.data) {

        if (reports.data.hasOwnProperty(key)) {


            reports.data[key].reportsLayer = L.layerGroup([]);

            $('#service').append($('<option>', {
                value: key,
                text: key,
            }));

            markers = reports.data[key];
            for (i = 0; i < markers.length; i++) {
                var info = markers[i];
                marker = L.marker([info.lat, info.lon]).bindPopup("Servicio: " + key + "<br>Fecha: " + info.report.timeStamp + "<br>Tipo: " + info.report.category + "-" + info.report.type);
                reports.data[key].reportsLayer.addLayer(marker);
            }
            //reportsGroup.addLayer(reports.data[key].reportsLayer);
            //reports.data[key].reportsLayer.addTo(map)
        }
    }


    /**
     * LOAD DATA
     */
    GTFS.loadData(function () {
        var baseLayer = GTFS.setLayerControl(map);
        for (var key in reports.data) {
            try {
                if (reports.data.hasOwnProperty(key)) {
                    reports.data[key].routeLayer = L.layerGroup([]);
                    console.log(key)
                    GTFS.drawRoutes(reports.data[key].routeLayer, GTFS.getRoutes([key + "I", key + "R"]));

                    //reports.data[key].routeLayer.addTo(map)
                    //routeGroup.addLayer(reports.data[key].routeLayer);

                }
            }
            catch (err) {
            }
        }

        $("#service").change(function () {
            updatemap(routeGroup, reportsGroup, reports);
        });
        var selectedItems = [];
        var allOptions = $("#service option");
        allOptions.each(function () {
            selectedItems.push($(this).val());
        });
        $("#service").val(selectedItems).trigger("change");
    }, "/static/", "datasantiago");


}

function updatemap(routelayer, reportslayer, rep) {
    routelayer.eachLayer(function (layer) {
        map.removeLayer(layer);
    });
    reportslayer.eachLayer(function (layer) {
        map.removeLayer(layer);
    });
    var selected = $(".select2_multiple").val()
    for (var i = 0; i < selected.length; i++) {
        routelayer.addLayer(rep.data[selected[i]].routeLayer)
        reportslayer.addLayer(rep.data[selected[i]].reportsLayer)
    }
}