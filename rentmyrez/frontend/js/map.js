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
	});
}

function getPostings (cb) {
	request
		.get('/api/postings')
		.end(function (err, res) {
			cb(err, res);
		});
}
