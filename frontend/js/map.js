var map;
var markerMap; 
var heatmap;
var mapJSONData;

function initMap() {
	var mapDiv = document.getElementById('map');
	var markerMapDiv = document.getElementById('markerMap');
	
	// first map 
	map = new google.maps.Map(mapDiv, {
		center: {lat: 49.2827, lng: -123.1207},
		zoom: 13,
		mapTypeId: google.maps.MapTypeId.TERRAIN
	});

	// second map with the markers
	markerMap = new google.maps.Map(markerMapDiv, {
		center: {lat: 49.2827, lng: -123.1207},
		zoom: 13,
		mapTypeId: google.maps.MapTypeId.TERRAIN
	});

	

  	loadJSON('http://localhost:8000/listings',
  		function(err,data) {
  			if (err != null) {
  				console.log("Error: " + err);
  			} else {
  				mapJSONData = data;
  				addMarkers(mapJSONData, markerMap);

  			}
  	});
}

function addMarkers(results, someMap) {

	var icon; 
	for (var x = 0; x < results.length; x++) {
		if ((results[x].latitude != null) && (results[x].longitude != null)
			&& (results[x].price < 100000)) {

				switch (results[x].price >= 0) {
					case results[x].price <= 500:
						icon = 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png';
						break;
					case results[x].price <= 1000:
						icon = 'http://maps.google.com/mapfiles/ms/icons/green-dot.png';
						break;
					case results[x].price <= 1500:
						icon = 'http://maps.google.com/mapfiles/ms/icons/yellow-dot.png';
						break;
					case results[x].price > 1500:
						icon = 'http://maps.google.com/mapfiles/ms/icons/red-dot.png';
						break;
					default:
						icon = 'http://maps.google.com/mapfiles/ms/icons/red-dot.png';
				}

				var marker = new google.maps.Marker({
				    position: {lat: results[x].latitude, 
				    		   lng: results[x].longitude},
				    map: someMap,
				    icon: icon
		  		});
		}

	}
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

function loadJSON(url, callback) {
	// this function allows you use a pure JSON file instead of using a js file
	var xobj = new XMLHttpRequest();
	xobj.open("get", url, true);
	xobj.responseType = "json";
	xobj.onreadystatechange = function() {
		if (xobj.readyState == 4 && xobj.status == "200") {
			callback(null, xobj.response);
		} else {
			callback(xobj.status);
		}
	};
	xobj.send(null);
}

function toggleHeatmap() {
	heatmap.setMap(heatmap.getMap() ? null : map);
}
