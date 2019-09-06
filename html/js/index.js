window.addEventListener("load", function(){
   
    //---------Make Map--------------
    //var corner1 = L.latLng(51,1);
    //var corner2 = L.latLng(60, 8);
    
    var startLat = 51;
    var endLat = 53;
    var startLon = 1.5;
    var endLon = 3.5;
    
    var corner1 = L.latLng(startLat,startLon);
    var corner2 = L.latLng(endLat, endLon);
    
    var bounds = L.latLngBounds(corner1, corner2);
    
    var mymap = L.map('mapid').fitBounds(bounds);
    
    var accessToken = "pk.eyJ1IjoiZXZlci1nZW9tYXIiLCJhIjoiY2swNmxtMzdpMDJnazNwbHZuc3lvaGt5cSJ9.BAHX_oY0LzawvUFoP82fsQ"
      L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoiZXZlci1nZW9tYXIiLCJhIjoiY2swNmxtMzdpMDJnazNwbHZuc3lvaGt5cSJ9.BAHX_oY0LzawvUFoP82fsQ', 
    {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
	   maxZoom: 15,
	   id: 'mapbox.streets',
	   accessToken: 'your.mapbox.access.token'
    }).addTo(mymap);
   
    //---------Plot Markers--------------
    
       // Plot CD
    
    
    var fishIcon = L.icon({
    iconUrl: 'resources/warning.svg',
    iconSize: [20, 20],
    iconAnchor: [10, 10],
    popupAnchor: [0, 0],
});
    
   
    
     d3.csv('resources/Sorted_Cd_data.csv').then(function(data){
    //d3.csv('resources/fishprob.csv').then(function(data){
        
        let keys = Object.keys(data[0]);    
        var scale = 5;  
        var markerCoors = [];
         
        for(var ii = 0; ii<data.length; ii++){
            
            markerCoors.push([data[ii][keys[0]],data[ii][keys[1]]]);
            
        }
         
        for(var ii = 0; ii<markerCoors.length; ii++){
            var marker = L.marker(markerCoors[ii], {icon:fishIcon}).addTo(mymap);
            marker.bindPopup("<b>Cadmium Contamination!</b><br> CD ppm > 50 .");
        }
        });
    
    //---------Plot polygons--------------
     d3.csv('resources/boxes.csv').then(function(data){
         
         for(var ii=0; ii<1000; ii++){
             
        
//             if(data[ii].StartLatitude>0 &&
//                data[ii].StartLongitude>-180 && 
//                data[ii].EndLatitude<90 && 
//                data[ii].EndLlongitude<360
//               ){
         
                var polygon = L.polygon([
                   [data[ii].StartLatitude, data[ii].StartLongitude],
                   [data[ii].StartLatitude, data[ii].EndLongitude],
                   [data[ii].EndLatitude, data[ii].EndLongitude],
                   [data[ii].EndLatitude, data[ii].StartLongitude],
                    ],{color: 'red',weight: '1'}).addTo(mymap);

                
             
                polygon.bindPopup("<b>Vulnerable Zone</b><br>ICES VMEDataSet201994");
                
             //}
            }
         });

    //---------Plot Heatmaps--------------
   
    //d3.tsv('resources/waves.csv').then(function(data){
    d3.csv('resources/predicted.csv').then(function(data){
        
        let keys = Object.keys(data[0]);    
        var heatmap = []
        var scale = 10;  
        for(var ii = 0; ii<data.length; ii++){
    
                heatmap.push([data[ii][keys[0]], data[ii][keys[1]],data[ii][keys[2]]*scale]);
            
                //heatmap.push([data[ii][keys[1]], data[ii][keys[2]],data[ii][keys[0]]*scale]); // waves
        }
        
        var heat = L.heatLayer(heatmap, 
                               {radius: 15}).addTo(mymap);
        });
    
    
//    d3.tsv('resources/waves.csv').then(function(data){
//    //d3.csv('resources/predicted.csv').then(function(data){
//        
//        let keys = Object.keys(data[0]);    
//        var heatmap = []
//        var scale = 10;  
//        console.log(data)
//        for(var ii = 0; ii<data.length; ii++){
//    
//             heatmap.push([data[ii][keys[1]], data[ii][keys[2]],data[ii][keys[0]]*scale]); // waves
//        }
//        
//        var heat = L.heatLayer(heatmap, 
//                               {radius: 15}).addTo(mymap);
//        });
//    
//    
    
    
//    var sensorTab = new Vue({
//    
//    el:"#sensor-list",
//    
//    data: {
// 
//    },
//    
//    methods:{
//    
//    },
//})
//
//    
//    console.log("dat workd jo!")            
//
//
});

Number.prototype.mod = function(n) {
    return ((this%n)+n)%n;
};
