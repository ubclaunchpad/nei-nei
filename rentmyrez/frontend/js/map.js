var map;
var heatmap;
var mapJSONData;

function initMap() {
	var mapDiv = document.getElementById('map');
	map = new google.maps.Map(mapDiv, {
		center: {lat: 49.2827, lng: -123.1207},
		zoom: 3,
		mapTypeId: google.maps.MapTypeId.TERRAIN
	});

	// Create a <script> tag and set the USGS URL as the source.
	//var script = document.createElement('script');

	//script.src = 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_week.geojsonp';
	
	//script.src = 'js/output.json';
	//document.getElementsByTagName('head')[0].appendChild(script);
	console.log(123);

	loadJSON(function(response){
		//console.log("response: " + response);
		mapJSONData = JSON.parse(response);
		//console.log("actual json: " + mapJSONData);
		addData(mapJSONData);

	});

	
}

	function addData(results) {
	// results = arrayOfJSONObjects...


//window.eqfeed_callback = function (results) {
	// var heatmapData = [];
	// for (var i = 0; i < results.features.length; i++) {
	// 	var coords = results.features[i].geometry.coordinates;
	// 	var latLng = new google.maps.LatLng(coords[1], coords[0]);
	// 	var magnitude = results.features[i].properties.mag;
 //      var weightedLoc = {
 //        location: latLng,
 //        weight: Math.pow(4, magnitude)
 //      };
	// 	heatmapData.push(weightedLoc);
	// }
	var heatmapData = [];
	
	for (var i = 0; i < results.length; i++) {

		var coords = results[i];
		var latLng = new google.maps.LatLng(coords.latitude,coords.longitude);
		var pricingScale = coords.price / coords.numBeds;
	
		if (coords == null || coords.latitude == null || coords.longitude == null ||
			coords.price == null || coords.numBeds == null) {

			// do nothing basically
		} else {
			var weightedLoc = {
				location: latLng,
				weight: pricingScale/100000
			}
			heatmapData.push(weightedLoc);
		}
	}

	heatmap = new google.maps.visualization.HeatmapLayer({
		data: heatmapData,
		dissipating: false,
		map: map
	});
}

// function getPostings (cb) {
// 	request
// 		.get('/api/postings')
// 		.end(function (err, res) {
// 			cb(err, res);
// 		});
// }

function loadJSON(callback) {
	// check it out for more information
	// https://codepen.io/KryptoniteDove/post/load-json-file-locally-using-pure-javascript

	// this function allows you use a pure JSON file instead of using a js file 

	var xobj = new XMLHttpRequest();
	xobj.overrideMimeType("application/json");
	// load json file here
	xobj.open('GET', 'js/output.json', true);
	xobj.onreadystatechange = function() {
		if (xobj.readyState == 4 && xobj.status == "200") {
			callback(xobj.responseText);
		}
	};
	xobj.send(null);
}

function toggleHeatmap() {
	heatmap.setMap(heatmap.getMap() ? null : map);
}


