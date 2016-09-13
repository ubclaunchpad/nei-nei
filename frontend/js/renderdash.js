/**
 * Data controller for neighbourhood (onClick) -> dashboard (d3.js)
 * @param {JSON} nei_name : name of neighbourhood clicked (NOTE: optional?)
 *
 *        [{
 *         bedrooms : int,   // Don't worry about 0's
 *         price : int,      // Normalized per bedroom
 *         date_listed : int // Unix Standard Time, seconds
 *         ...               // Whatever else is in there, doesn't matter
 *        },]
 */
function passDataToDashboard (clicked_neighbourhood_data) {
  var bedrooms, curr_neighbourhood_data = [];
  clicked_neighbourhood_data.forEach(function (listing) {
    // No listings can offer 0 bedrooms
    bedrooms = listing.bedrooms == 0 ? 1 : listing.bedrooms;
    curr_neighbourhood_data.push({
      'bedrooms':parseInt(bedrooms),
      // Normalized price per bed
      'price':parseInt(Math.floor(listing.price / bedrooms)),
      'date_listed':listing.date_listed
    });
  });

  // Purge the DOM before rerendering
  ['chart-box-1', 'chart-box-2', 'chart-box-3'].forEach(purgeNode)
  // Calls graph wrapper functions on page load to render each in the dashboard
  movingAverage("chart-box-1", curr_neighbourhood_data);
  bedroomDistribution("chart-box-2", curr_neighbourhood_data);
  postTimeSeries("chart-box-3", curr_neighbourhood_data);
}

function purgeNode(id) {
  el = document.getElementById(id);
  while (el.firstChild) {
    el.removeChild(el.firstChild)
  }
}


// TODO: not passing data to d3 rendering function calls
function initializeDashData () {
  // Consolidate all listings from api
  var dataFromAllHoods = [];
  for (var hood in listingsDictionary) {
    if (listingsDictionary.hasOwnProperty(hood)) {
      dataFromAllHoods = dataFromAllHoods.concat(listingsDictionary[hood]);
    }
  }

  movingAverage("chart-box-1", dataFromAllHoods);
  bedroomDistribution("chart-box-2", dataFromAllHoods);
  postTimeSeries("chart-box-3", dataFromAllHoods);
}

initializeDashData();
