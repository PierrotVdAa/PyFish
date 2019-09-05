window.addEventListener("load", function(){
   
    //---------Make Map--------------
    var corner1 = L.latLng(51,1);
    var corner2 = L.latLng(60, 8);
    var bounds = L.latLngBounds(corner1, corner2);
    
    var mymap = L.map('mapid').fitBounds(bounds);
    
    var accessToken = "pk.eyJ1IjoiZXZlci1nZW9tYXIiLCJhIjoiY2swNmxtMzdpMDJnazNwbHZuc3lvaGt5cSJ9.BAHX_oY0LzawvUFoP82fsQ"
     L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoiZXZlci1nZW9tYXIiLCJhIjoiY2swNmxtMzdpMDJnazNwbHZuc3lvaGt5cSJ9.BAHX_oY0LzawvUFoP82fsQ', 
    {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
	   maxZoom: 10,
	   id: 'mapbox.satellite',
	   accessToken: 'your.mapbox.access.token'
    }).addTo(mymap);

    
    //---------Plot Markers--------------
    var fishIcon = L.icon({
    iconUrl: 'resources/fish.png',
    iconSize: [20, 20],
    iconAnchor: [10, 10],
    popupAnchor: [0, 0],
});
    
    var markerCoors = [[51.609704, 1.320196],[51.65, 1.35]];
    
    for(ii = 0; ii<markerCoors.length; ii++){
        var marker = L.marker(markerCoors[ii], {icon:fishIcon}).addTo(mymap);
        marker.bindPopup("<b>Here's some good fish!</b><br>get over here capt'n.");
    }
    
    //---------Plot polygons--------------
    var polygon = L.polygon([
	   [51.552125, 1.516433],
	   [51.552125, 1.839815],
	   [51.434955, 1.839815],
	   [51.434955, 1.516433],
        ],{color: 'red',weight: '1'}).addTo(mymap);
        
    polygon.bindPopup("<b>Just don't fish over here!</b><br>not allowed!");
 
    
    
    //---------Plot Heatmaps--------------
    d3.csv('resources/fishprob.csv').then(function(data){
        
        var keys = Object.keys(data[0]);    
        var heatmap = []
        
        for(var ii = 0; ii<data.length; ii++){
    
                heatmap.push([data[ii][keys[0]], data[ii][keys[1]],data[ii][keys[2]]]);
        }
        
        var heat = L.heatLayer(heatmap, 
                               {radius: 5}).addTo(mymap);

        });
    
    console.log("dat workd jo!")        
    
});
