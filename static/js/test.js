/**
 * Created by patricio on 11/28/16.
 */
var url = 'http://' + location.host + '/carriers/getCount/';
var reports;
var resumen;
var detalle;
$.getJSON(url)
    .done(function (data) {
        console.log(data)
        reports = data;
        makechart()
    });

function makechart() {
    resumen = c3.generate({
        bindto: '#resumen',
        data: {
            // iris data from R
            json: reports.datatype,
            type: 'pie',
            onmouseover: function (d, i) {
                makedetail(d.id);
            }
        },
        tooltip: {
            format: {
                value: function (x) {
                    return x;
                }
            }
        }
    });
}
function makedetail(type) {
    $("#detailtext").text(type);
    detalle = c3.generate({
        bindto: '#detalle',
        data: {
            // iris data from R
            json: reports.groups[type],
            type: 'pie'
        },
        tooltip: {
            format: {
                value: function (x) {
                    return x;
                }
            }
        }
    });
}

