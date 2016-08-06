/**
 * Provides a public interface for turning on and off neighbourhood
 * overlays. Also provides an interface for highlighting particular
 * neighbourhood to indicate they are selected.
 * @param {google.maps.Map} map - reference to the map object
 *   that overlays should be displayed over.
 */
function NeighbourhoodsAPI (map) {
	// Keeps track of initial data used to draw polygons and names
	var neighbourhoods = {};
	// Keeps track of whether overlays are hidden or visible
	var visible = true;
	// Keeps track of which, if any neighbourhood is highlighted
	var highlighted = null;

	/**
	 * Initializes the API with the neighbourhood polygons
	 * to be displayed.
	 * @param {array} polygons - array of objects with a `name`
	 *   key specifying the name of the neighbourhood and a
	 *   `polygons` key specifying the set of lat/lng pairs that
	 *   define the neighbourhood's bounds.
	 */
	this.init = function (polygons) {
		// Put the data inside polygons inside a local private variable
		// like `neighbourhoods` so that it can be used later. Decide
		// whether its reasonable to actually display the neighbourhoods
		// on the map here, or if that should be done in a different method.

		visible = true;
	  //window.alert("neighbourhoods" + polygons[0].polygon[0].lat);
		var polygon;

		polygons.forEach(function (hood) {
			// Construct the polygon
			polygon = new google.maps.Polygon({
				paths: hood.polygon,
				strokeColor: '#FF0000',
				strokeOpacity: 0.8,
				strokeWeight: 2,
				fillColor: '#FF0000',
				fillOpacity: 0.35
			});

			neighbourhoods[hood.name] = polygon;
			// window.alert("neighbourhood " + hood.name + " has polygon " + neighbourhoods[hood.name]);

			if (visible === true) {
				polygon.setMap(map);
			};
		});

	}

	/**
	 * Sets all neighbourhood overlays to visible.
	 */
	this.displayAll = function () {
		// Set all neighbourhood overlays to be visible on the map.
		if (visible === false) {
			visible = true;
		}
	}

	/**
	 * Sets all neighbourhood overlays to hidden.
	 */
	this.hideAll = function () {
		// Set all neighbourhood overlays to be invisible on the map.
		visible = false;
	}

	/**
	 * Toggles highlight state of a neighbourhood.
	 * If it is already highlighted, unhighlight it.
	 * If it is not already highlighted, highlight it.
	 * If another neighbourhood is highlighted, unhighlight that neighbourhood.
	 * @param {string} neighbourhood - the name of the neighbourhood
	 *   to (un)highlight
	 */
	this.highlight = function (neighbourhoodName) {
		// Toggle highlight state of a neighbourhood.
		// Update internal state of which neighbourhoods are highlighted,
		// then update the map to reflect the change.
	}

	/**
	 * Update the fillColor and strokeColor for the polygon of given neighbourhoodName.
	 * @param {string} neighbourhoodName - the name of the neighbourhood to update
	 *   colour for;
	 * 	 {string} colour - the colour to set the neighbourhood overlay to
	 */
	this.updateColour = function (neighbourhoodName, colour) {
		neighbourhoods[neighbourhoodName].fillColor = colour;
		neighbourhodds[neighbourhoddName].strokeColor = colour;
	}
}
