/**
 * Created by patricio on 11/29/16.
 */
var url = 'http://' + location.host + '/carriers/getMap/';
var reports;
var resumen;
var detalle;
$.getJSON(url)
    .done(function (data) {
        console.log(data)
        reports = data;
    });

$(document).ready(function () {
    /**
     * SET MAP
     */

    var beauchefLocation = L.latLng(-33.4579141, -70.6646977);
    var map = L.map("mapid", {editable: true}).setView(beauchefLocation, 15);


    var routeLayer1 = L.featureGroup([]);
    var busStopsLayer1 = L.layerGroup([]);
    var routeReports = L.layerGroup([]);

    var overlays = {
        "servicio": routeLayer1,
        "paradas": busStopsLayer1,
        "reportes": routeReports
    };
    L.control.layers({}, overlays).addTo(map);

    function drawRoute(service, direction, busStopsLayer, routeLayer) {
        routeReports.clearLayers();
        // draw bus stops related to service
        busStopsLayer = GTFS.drawStopsForService(busStopsLayer, service, direction);

        // draw route
        var routes = GTFS.getRoutes([service + direction]);
        console.log(routes);
        GTFS.drawRoutes(routeLayer, routes);

        var line = [];
        $.each(routes[0].route, function (i, v) {
            line.push([v.latitud, v.longitud]);
        });

        var routeWithArrows = L.polylineDecorator(line, {
            patterns: [
                {
                    offset: 0,
                    endOffset: 0,
                    repeat: '40',
                    symbol: L.Symbol.arrowHead(
                        {
                            pixelSize: 10,
                            polygon: true,
                            pathOptions: {
                                fillOpacity: 1,
                                color: GTFS.getRouteColor(service),
                                stroke: true
                            }
                        })
                }
            ]
        });
        var popupMessage = "<h4>" + service + direction + "</h4>";
        routeWithArrows.bindPopup(popupMessage);
        routeLayer.bindPopup(popupMessage);

        routeLayer.addLayer(routeWithArrows);
        routeLayer.addTo(map);
        //busStopsLayer.addTo(map);

        map.fitBounds(routeLayer.getBounds());

        markers = reports.data[service];
        for (i = 0; i < markers.length; i++) {
            marker = L.marker([markers[i].lat, markers[i].lon]);
            routeReports.addLayer(marker);
        }


        console.log("Map updated with service: " + service + direction);
    };


    /**
     * LOAD DATA
     */
    GTFS.loadData(function () {
        var baseLayer = GTFS.setLayerControl(map);
        // SET BUTTON ACTION
        var drawServiceButton1 = $("#seeBuses1");

        var clickFunction = function (e) {
            var index = $(e.target).attr('id').substr(-1);
            var serviceCode = $("#serviceCode" + index).val();
            var direction = $("input[name=direction" + index + "]:checked").val();

            drawRoute(serviceCode, direction, busStopsLayer1, routeLayer1);


            var serviceInfo = GTFS.data.service[serviceCode];
            var origin = serviceInfo.origin;
            var destination = serviceInfo.destiny;
            if (direction == "I") {
                $("#serviceOrigin" + index).text(origin);
                $("#serviceDestination" + index).text(destination);
            } else {
                $("#serviceOrigin" + index).text(destination);
                $("#serviceDestination" + index).text(origin);
            }
        };

        drawServiceButton1.click(clickFunction);

        // press enter on serviceCode input
        var keyPressFunction = function (e) {
            var key = e.which;
            // the enter key code
            if (key == 13) {
                var index = $(e.target).attr('id').substr(-1);
                $('#seeBuses' + index).trigger("click");
                return false;
            }
        }
        $("#serviceCode1").keypress(keyPressFunction);

        // change radio button
        $("input[type=radio][name=direction1]").change(function () {
            if ($("#serviceCode1").val()) {
                drawServiceButton1.trigger("click");
            }
        });
    }, "/static/", "datasantiago");
});