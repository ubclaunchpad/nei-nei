var map;

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

	var api = new NeighbourhoodsAPI(map);
 	api.init(fixed_neighbourhoods_data);
}

function getPostings (cb) {
	request
		.get('/api/postings')
		.end(function (err, res) {
			cb(err, res);
		});
}
