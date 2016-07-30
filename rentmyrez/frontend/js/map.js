var map;
var heatmap;
var mapJSONData;

function initMap() {
	var mapDiv = document.getElementById('map');
	map = new google.maps.Map(mapDiv, {
		center: {lat: 49.2827, lng: -123.1207},
		zoom: 13,
		mapTypeId: google.maps.MapTypeId.TERRAIN
	});

	loadJSON(function(response){
		mapJSONData = JSON.parse(response);
		addData(mapJSONData);
	});
}

	function addData(results) {
	// Note: results = arrayOfJSONObjects
	var heatmapData = [];
	
	for (var i = 0; i < results.length; i++) {
		var coords = results[i];
		var latLng = new google.maps.LatLng(coords.latitude,coords.longitude);
		var pricingScale = coords.price / coords.numBeds;
	
		if (coords == null || coords.latitude == null || coords.longitude == null ||
			coords.price == null || coords.numBeds == null) {
			// do nothing
		} else {
			var weightedLoc = {
				location: latLng,
				weight: pricingScale/10
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

function loadJSON(callback) {
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


