var map;
var heatmap;
var mapJSONData;

function initMap() {
	var mapDiv = document.getElementById('map');
	map = new google.maps.Map(mapDiv, {
<<<<<<< HEAD
		center: {lat: 49.2414, lng: -123.1135},
		zoom: 12,
=======
		center: {lat: 49.2827, lng: -123.1207},
		zoom: 13,
>>>>>>> 6aea383a1a0831378c3192efaec93c6f96c3f665
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
		var latLng = new google.maps.LatLng(coords.lat,coords.lng);
		var pricingScale = coords.price / coords.beds;

		if (coords == null || coords.lat == null || coords.lng == null ||
			coords.price == null || coords.beds == null || pricingScale > 100000) {
			// do nothing
		} else {
			console.log(pricingScale);
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

function loadJSON(callback) {
	// this function allows you use a pure JSON file instead of using a js file
	var xobj = new XMLHttpRequest();
	xobj.overrideMimeType("application/json");
	// load json file here
	xobj.open('GET', '../../scripts/api/data/raw_listings_data.json', true);
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
