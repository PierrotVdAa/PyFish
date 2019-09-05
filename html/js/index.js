window.addEventListener("load", function(){
   
    var corner1 = L.latLng(51,1);
    var corner2 = L.latLng(60, 8);
    var bounds = L.latLngBounds(corner1, corner2);
    
    
    var mymap = L.map('mapid').fitBounds(bounds);
    console.log('exec this')       
    
    var accessToken = "pk.eyJ1IjoiZXZlci1nZW9tYXIiLCJhIjoiY2swNmxtMzdpMDJnazNwbHZuc3lvaGt5cSJ9.BAHX_oY0LzawvUFoP82fsQ"
    
    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoiZXZlci1nZW9tYXIiLCJhIjoiY2swNmxtMzdpMDJnazNwbHZuc3lvaGt5cSJ9.BAHX_oY0LzawvUFoP82fsQ', 
    {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
	   maxZoom: 10,
	   id: 'mapbox.satellite',
	   accessToken: 'your.mapbox.access.token'
    }).addTo(mymap);

    
    var fishIcon = L.icon({
    iconUrl: 'resources/fish.png',
    iconSize: [20, 20],
    iconAnchor: [10, 10],
    popupAnchor: [0, 0],
});
    
    var markerCoors = [51.609704, 1.320196];
    
    var marker = L.marker(markerCoors, {icon:fishIcon}).addTo(mymap);
    marker.bindPopup("<b>Here's some good fish!</b><br>get over here capt'n.");

    var polygon = L.polygon([
	   [51.552125, 1.516433],
	   [51.552125, 1.839815],
	   [51.434955, 1.839815],
	   [51.434955, 1.516433],
        ],{color: 'red',weight: '1'}).addTo(mymap);
        
    polygon.bindPopup("<b>Just don't fish over here!</b><br>not allowed!");
    
});
