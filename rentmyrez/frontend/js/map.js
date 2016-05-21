var map;

function initMap() {
	var mapDiv = document.getElementById('map');
	map = new google.maps.Map(mapDiv, {
		center: {lat: 44.540, lng: -78.546},
		zoom: 8,
		mapTypeId: google.maps.MapTypeId.TERRAIN
	});

	// Create a <script> tag and set the USGS URL as the source.
	var script = document.createElement('script');

	script.src = 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_week.geojsonp';
	document.getElementsByTagName('head')[0].appendChild(script);

	map.data.setStyle(function(feature) {
		console.log('feature', feature);
		var magnitude = feature.getProperty('mag');
		console.log('magnitude', magnitude);
		return {
			icon: getCircle(magnitude)
		};
	});
}

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

window.eqfeed_callback = function (results) {
  map.data.addGeoJson(results);
}

function getPostings (cb) {
	request
		.get('/api/postings')
		.end(function (err, res) {
			cb(err, res);
		});
}
