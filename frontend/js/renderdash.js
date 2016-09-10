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
 *
 * @return {JSON} : JSON object list of the form
 *
 *        [{
 *         bedrooms : int,   // Range: 0 - max
 *         price : int,      // Normalized per bedroom
 *         date_listed : int // Unix Standard Time, seconds
 *        },]
 */
function passDataToDashboard (clicked_neighbourhood_data) {
  console.log(clicked_neighbourhood_data);
  var size = clicked_neighbourhood_data.length;
  var curr_neighbourhood_data = new Array(size);
  for (var i = 0; i < size; i++) {
    curr_neighbourhood_data.push({
      'bedrooms' : clicked_neighbourhood_data[i].bedrooms,
      'price' : clicked_neighbourhood_data[i].price,
      'date_listed' : clicked_neighbourhood_data[i].date_listed
    });
  }
  return curr_neighbourhood_data;
}

var curr_neighbourhood_data = passDataToDashboard("");

// Calls graph wrapper functions on page load to render each in the dashboard
movingAverage("chart-box-1", curr_neighbourhood_data);
bedroomDistribution("chart-box-2", curr_neighbourhood_data);
postTimeSeries("chart-box-3", curr_neighbourhood_data);
