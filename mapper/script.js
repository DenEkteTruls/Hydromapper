
var map = L.map("map").setView([59.419501, 10.487164], 11);

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
  maxZoom: 22,
  id: 'mapbox/streets-v11',
  tileSize: 512,
  zoomOffset: -1,
  accessToken: 'pk.eyJ1IjoiZGVuZWt0ZXRydWxzIiwiYSI6ImNrOWgwbzJiNjA4OHozbm13bjZxMjVwZTMifQ.VtqneIR4Cwwx-iYGjhLFxw'
}).addTo(map);


var lines = [];
var markers = [];


function save()
{
    if(markers.length > 0) {
        var new_data = [];
        markers.forEach((marker) => {
            new_data.push(marker._latlng);
        });
        document.write(JSON.stringify(new_data));
    } else {
        alert("No markers!");
    }
}


function reset()
{
    markers.forEach((marker) => {
        map.removeLayer(marker);
    });

    lines.forEach((line) => {
        map.removeLayer(line);
    });

    markers = [];
    lines = [];
}


function open_()
{
    var a = window.prompt("NAV-DATA");
    if(a) {
        reset();
        JSON.parse(a).forEach((pos) => {
            var marker = L.marker([pos.lat, pos.lng]).bindPopup("Waypoint: "+markers.length).addTo(map);
            markers.push(marker);
            if(markers.length > 1) {
                var line = L.polyline([markers[markers.length-2]._latlng, markers[markers.length-1]._latlng], {color: "red"}).addTo(map);
                lines.push(line);
            }
        });
    }
}


function add(e)
{
    var marker = L.marker(e.latlng).bindPopup("Waypoint: "+markers.length).addTo(map);
    markers.push(marker);
    if(markers.length > 1) {
        var line = L.polyline([markers[markers.length-2]._latlng, markers[markers.length-1]._latlng], {color: "red"}).addTo(map);
        lines.push(line);
    }
}


map.on("click", (e) => { add(e); });