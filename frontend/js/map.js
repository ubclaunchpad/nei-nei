var markerMap, heatmap, mapJSONData, neighbourhoodMarkerMap;
var neighbourhoodDictionary = {};

function initMap() {

	var markerMapDiv = document.getElementById('markerMap');

	// second map with the markers
	markerMap = new google.maps.Map(markerMapDiv, {
		center: {lat: 49.2827, lng: -123.1207},
		zoom: 13,
		mapTypeId: google.maps.MapTypeId.TERRAIN
	});

	// promise ajax call. 
	var promise = new Promise(function(resolve, reject) {

		loadJSON('http://localhost:8000/api/listings',
  		function(err,data) {
  			if (err != null) {
  				console.log("Error: " + err);
  				//reject(err);
  			} else {
  				mapJSONData = data;
  				addMarkers(mapJSONData, markerMap);
  				resolve();

  			}
  		});
	});

	promise.then(function() {
		// callback to hand promise resolution
		loadJSON('http://localhost:8000/api/neighbourhoods', 
			function(err, data) {
				if (err != null) {
	  				console.log("Error: " + err);
	  			} else {
					neighbourhoodAPIInput = data.map(function(nbhObj) {
						return {
							name: nbhObj.name,
							polygon: nbhObj.boundary.map(function(latLng) {
								return {
									lat: latLng.latitude,
									lng: latLng.longitude
								};
							})
						}
					});
				}

			neighbourhoodMarkerMap = new NeighbourhoodsAPI(markerMap);
			neighbourhoodMarkerMap.init(neighbourhoodAPIInput);
			neighbourhoodMarkerMap.displayAll();
			colourNeighbourhoods();
			}
		);
	}, 	
		// callback to handle promise rejection 
		function(value) {
			console.log("Promise was not fulfilled due to Error: " + value);
		}
	);
  	
}

function colourNeighbourhoods(){

	var blue = '#0099ff';
	var green = '#66ff99';
	var red = '#ff6666';
	var yellow = '#ffff99';

	var neighbourhoodColour = '#ff6666';
	neighbourhoodMarkerMap.updateColour("Riley Park", blue);

	var neighbourhoodKeys = Object.keys(neighbourhoodDictionary);
	
	for (var property in neighbourhoodKeys) {
		var neighbourhoodColor;
		var neighbourhoodPPB = 
			neighbourhoodDictionary[neighbourhoodKeys[property]][0] / 
			neighbourhoodDictionary[neighbourhoodKeys[property]][1];

		// console.log(neighbourhoodPPB);

		switch (neighbourhoodPPB >= 0) {
			case neighbourhoodPPB <= 500:
				neighbourhoodColor = blue;
				break;
			case neighbourhoodPPB <= 1000:
				neighbourhoodColor = green; 
				break;
			case neighbourhoodPPB <= 1500:
				neighbourhoodColor = yellow;
				break;
			case neighbourhoodPPB > 1500:
				neighbourhoodColor = red;
				break;
			default:
				neighbourhoodColor = red;
		}
		
		neighbourhoodMarkerMap.updateColour(neighbourhoodKeys[property], neighbourhoodColor);
	}
	
}


function addMarkers(results, someMap) {

	var icon; 
	for (var x = 0; x < results.length; x++) {
		if ((results[x].latitude != null) && (results[x].longitude != null)
			&& (results[x].price < 100000) && (results[x].bedrooms > 0)) {
			// skip listings with 0 bedrooms. 

				// price per bedroom 
				var ppb = results[x].price / results[x].bedrooms; 

				switch (ppb >= 0) {
					case ppb <= 500:
						icon = 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png';
						break;
					case ppb <= 1000:
						icon = 'http://maps.google.com/mapfiles/ms/icons/green-dot.png';
						break;
					case ppb <= 1500:
						icon = 'http://maps.google.com/mapfiles/ms/icons/yellow-dot.png';
						break;
					case ppb > 1500:
						icon = 'http://maps.google.com/mapfiles/ms/icons/red-dot.png';
						break;
					default:
						icon = 'http://maps.google.com/mapfiles/ms/icons/red-dot.png';
				}



				//if listing's neighbourhood != null 
				if (results[x].neighbourhood != null) {

					

					// if neighbourhood key isn't in dictionary
					if (!(results[x].neighbourhood in neighbourhoodDictionary)) {
						// then add it inside the dictionary obj
						var priceCount = [ppb, 1];
						var neighbourhoodKey = results[x].neighbourhood; 
						neighbourhoodDictionary[neighbourhoodKey] = priceCount;
					} else {
						// else neighbourhood key is in dictionary
						var tempPriceCount = neighbourhoodDictionary[results[x].neighbourhood];
						tempPriceCount[0] = tempPriceCount[0] + ppb;
						tempPriceCount[1] = tempPriceCount[1] + 1;
						neighbourhoodDictionary[results[x].neighbourhood] = tempPriceCount;

					}
					
				} else {
					icon = 'http://maps.google.com/mapfiles/ms/icons/pink-dot.png';
				}

				

				var marker = new google.maps.Marker({
				    position: {lat: results[x].latitude, 
				    		   lng: results[x].longitude},
				    map: someMap,
				    icon: icon
		  		});

		  		marker.addListener('click', function(res, m) {
		  			if (typeof res === undefined) {
		  				throw new Error('undefined listing');
		  			} else {

		  				var contentString = '<div id="tooltip">Price: $' + res.price 
							+ '<br> Listing url: <a target="_blank" href="' 
							+ res.listing_url + '">Click here</a></div>';

				  		var infowindow = new google.maps.InfoWindow({
		          			content: contentString
		        		});

		  				infowindow.open(someMap, m);

		  				console.log("Latitude: " + res.latitude + 
		  					" Longitude: " + res.longitude);
		  			}
		  			
		  		}.bind(null, results[x], marker));

		  		
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
		if (xobj.readyState == 4 && xobj.status == 200) {
			callback(null, xobj.response);
		} else {
			callback(xobj.status);
		}
	};
	xobj.send();
}
