/**
 * Created by patricio on 11/29/16.
 */
var url = 'http://' + location.host + '/carriers/getMap/';
var reports;

$(document).ready(function () {
    /**
     * SET MAP
     */
    $.getJSON(url)
        .done(function (data) {
            reports = data;
            rest();


        });
})

function rest() {
    var beauchefLocation = L.latLng(-33.4579141, -70.6646977);
    var map = L.map("mapid", {editable: true}).setView(beauchefLocation, 15);

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

            markers = reports.data[key];
            for (i = 0; i < markers.length; i++) {
                var info = markers[i];
                marker = L.marker([info.lat, info.lon]).bindPopup("Servicio: "+key +"<br>Fecha: " + info.report.timeStamp+"<br>Tipo: " + info.report.category+ "-" + info.report.type);
                reports.data[key].reportsLayer.addLayer(marker);
            }
            reportsGroup.addLayer(reports.data[key].reportsLayer);
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
                    GTFS.drawRoutes(reports.data[key].routeLayer, GTFS.getRoutes([key + "I",key + "R"]));

                    //reports.data[key].routeLayer.addTo(map)
                    routeGroup.addLayer(reports.data[key].routeLayer);

                }
            }
            catch (err) {
            }
        }


    }, "/static/", "datasantiago");


}