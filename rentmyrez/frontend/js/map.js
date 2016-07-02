var map;
var testNeighbourhood;

function initMap() {
	var mapDiv = document.getElementById('map');

	var fixed_neighbourhoods_data = neighbourhoods_data.map(function (hood) {
		return {
			name: hood.name,
			polygon: hood.polygon.map(function (latlng) {
		    return {
		      lat: Number(latlng.lng),
		      lng: Number(latlng.lat)
		    }
		  })
		}
	});

	map = new google.maps.Map(mapDiv, {
		center: {lat: 49.2414, lng: -123.1135},
		zoom: 12,
		mapTypeId: google.maps.MapTypeId.TERRAIN
	});

	fixed_neighbourhoods_data.forEach(function (hood) {
		// Construct the polygon
	  testNeighbourhood = new google.maps.Polygon({
	    paths: hood.polygon,
	    strokeColor: '#FF0000',
	    strokeOpacity: 0.8,
	    strokeWeight: 2,
	    fillColor: '#FF0000',
	    fillOpacity: 0.35
	  });

		testNeighbourhood.setMap(map);
	})

}

	// Create a <script> tag and set the USGS URL as the source.
	// var script = document.createElement('script');
  //
	// script.src = 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_week.geojsonp';
	// document.getElementsByTagName('head')[0].appendChild(script);
  //
	// map.data.setStyle(function(feature) {
	// 	console.log('feature', feature);
	// 	var magnitude = feature.getProperty('mag');
	// 	console.log('magnitude', magnitude);
	// 	return {
	// 		icon: getCircle(magnitude)
	// 	};
// 	});
//
// 	map.data.setStyle({
// 		icon: '//example.com/path/to/image.png',
// 		fillColor: 'green',
// 		strokeWeight: 10,
// 	});
//
// map.data.loadGeoJson('https://storage.googleapis.com/maps-devrel/google.json');}
//
// map.data.addListener('click', function(event) {
//    map.data.overrideStyle(event.feature, {fillColor: 'red'});
// });
//
// map.data.addListener('mouseover', function(event) {
// 	document.getElementById('info-box').textContent =
// 		event.feature.getProperty('letter');
// });

function getCircle(magnitude) {
  var circle = {
    path: google.maps.SymbolPath.CIRCLE,
    fillColor: 'red',
    fillOpacity: .2,
    scale: Math.pow(2, magnitude) / 2,
    strokeColor: 'white',
    strokeWeight: .5
  };
  return circle;
}

// window.eqfeed_callback = function (results) {
// 	var heatmapData = [];
// 	for (var i = 0; i < results.features.length; i++) {
// 		var coords = results.features[i].geometry.coordinates;
// 		var latLng = new google.maps.LatLng(coords[1], coords[0]);
// 		var magnitude = results.features[i].properties.mag;
//       var weightedLoc = {
//         location: latLng,
//         weight: Math.pow(2, magnitude)
//       };
// 		heatmapData.push(latLng);
// 	}
// 	var heatmap = new google.maps.visualization.HeatmapLayer({
// 		data: heatmapData,
// 		dissipating: false,
// 		map: map
// 	});
// }

function getPostings (cb) {
	request
		.get('/api/postings')
		.end(function (err, res) {
			cb(err, res);
		});
}
