/**
 * Creates an exponential moving average plot using the D3.js API
 * @param {string} id - id of tag to place svg object within
 * @param {json} data - json object of the form
 *
 *        [{
 *         latitude : float,
 *         longitude : float,
 *         bedrooms : int,
 *         bathrooms : int,
 *         price : int,
 *         date_listed : int
 *        },]
 */
function postTimeSeries (id) {
  // Margins to center and transform the graph
  var margin = {top: 20, right: 20, bottom: 30, left: 50},
      width = 500 - margin.left - margin.right,
      height = 300 - margin.top - margin.bottom;
  // Initializate x value mapping functions and axis
  var xValue = function (d) { return new Date(d.date_listed * 1000); },
      xScale = d3.scaleTime().range([0, width]),
      xMap = function (d) { return xScale(xValue(d)); },
      xAxis = d3.axisBottom()
                .scale(xScale)
                .ticks(d3.timeMonth.every(1));

  // Initializate y value mapping functions and axis
  var yScale = d3.scaleLinear().range([height, 0]),
      yAxis = d3.axisLeft()
                .scale(yScale)
                .ticks(5);

  // Create canvas for SVG objects.
  var svg = d3.select("div#"+id)
           .append("svg")
              .attr("class", "chart")
              .attr("id", "chart1")
              .attr("preserveAspectRatio", "xMinYMin meet")
              .attr("viewBox", "0 0 500 350")
           .append("g")
             .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
  // Now to use real data in a callback
  d3.json('../../places/dashboard_test_data.json', function (error, data) {
    // TODO: robust error handling
    if (error) throw error;

    // Useful callbacks
    function sortMinToMaxCallback(a, b) {
      return a.date_listed - b.date_listed;
    }

    // TODO: function that grabs data from most recently clicked neighbourhood
    //  For now default to 'Outside' data points and 'All' data points as background
    outsideData = data[data.length - 1]['positions'].sort(sortMinToMaxCallback);

    var formatMonth = d3.timeFormat("%B");
    var monthExtent = d3.extent(outsideData, xValue);
    var monthBins = d3.timeMonths(d3.timeMonth.offset(monthExtent[0], -1), d3.timeMonth.offset(monthExtent[1], 1));

    var histogram = d3.histogram()
        .value(xValue)
        .thresholds(monthBins);

    var binnedData = histogram(outsideData);
    var numBins = binnedData.length;

    xScale.domain(monthExtent)
          .ticks(d3.timeMonth.every(1));
    yScale.domain([0, d3.max(binnedData, function (d) { return d.length; })]);

    svg.append('g')
       .attr('class', 'x-axis')
       .attr('transform', 'translate(0,'+height+')')
       .call(xAxis);

    svg.append('g')
       .attr('class', 'y-axis')
       .call(yAxis)

     svg.append('g').selectAll('bar')
             .data(binnedData)
           .enter()
             .append('rect')
             .attr('class', 'bar')
             .attr('x', function (d, i) { return i * (width / numBins); })
             .attr('width', (width / numBins) - 10)
             .attr('y', function (d) { return yScale(d.length); })
             .attr('height', function (d) { return height - yScale(d.length); });

     svg.append('text')
           .attr('class', 'title')
           .attr('x', width / 2.5)
           .attr("dx", "15px")
           .attr('dy', '-5px')
           .style('text-anchor', 'middle')
           .text('Posts per Month');

   });
}
