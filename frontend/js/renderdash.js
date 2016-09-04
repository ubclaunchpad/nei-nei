/**
 * Data controller for neighbourhood (onClick) -> dashboard (d3.js)
 * @param {string} nei_name : name of neighbourhood clicked (NOTE: optional?)
 * @return {JSON} : JSON object list of the form
 *
 *        [{
 *         bedrooms : int,   // Don't worry about 0's
 *         price : int,      // Normalized per bedroom
 *         date_listed : int // Unix Standard Time, seconds
 *        },]
 */
function passDataToDashboard (nei_name) {
  return curr_neighbourhood_data;
}

var curr_neighbourhood_data = passDataToDashboard("");

// Calls graph wrapper functions on page load to render each in the dashboard
movingAverage("chart-box-1", curr_neighbourhood_data);
bedroomDistribution("chart-box-2", curr_neighbourhood_data);
postTimeSeries("chart-box-3", curr_neighbourhood_data);
