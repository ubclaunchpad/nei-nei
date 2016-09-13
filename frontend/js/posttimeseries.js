/**
 * Creates a  using the D3.js API
 * @param {string} id - id of tag to place svg object within
 * @param {JSON} curr_neighbourhood_data - json object of the form
 *
 *        [{
 *         bedrooms : int,
 *         price : int,
 *         date_listed : int
 *        },]
 */
function postTimeSeries (id, curr_neighbourhood_data) {
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

 function update(data) {

    // Useful callbacks
    function sortMinToMaxCallback(a, b) {
      return a.date_listed - b.date_listed;
    }

    var monthExtent = d3.extent(data, xValue);
    var monthBins = d3.timeMonths(d3.timeMonth.offset(monthExtent[0], -1), d3.timeMonth.offset(monthExtent[1], 1));

    xScale.domain(monthExtent)
        .ticks(d3.timeMonth.every(1));

    var histogram = d3.histogram()
        .domain(xScale.domain())
        .value(xValue)
        .thresholds(monthBins) // change
        (data);

    yScale.domain([0, d3.max(histogram, function (d) { return d.length; })]);

    var bar = svg.selectAll('bar')
        .data(histogram)
      .enter().append('g')
        .attr('class', 'bar')
        .attr('transform', function (d) {
          return 'translate(' + xScale(d.x0) + "," + yScale(d.length) + ')'; });

    bar.append('rect')
      .attr('x', 1)
      .attr('width', xScale(histogram[0].x1) - xScale(histogram[0].x0) - 1)
      // .attr('y', yMap)
      .attr('height', function (d) { return height - yScale(d.length); });

     svg.append('text')
           .attr('class', 'title')
           .attr('x', width / 2)
           .attr("dx", "15px")
           .attr('dy', '-5px')
           .style('text-anchor', 'middle')
           .text('Posts per Month');

     svg.append('g')
        .attr('class', 'x-axis')
        .attr('transform', 'translate(0,'+height+')')
        .call(xAxis);

     svg.append('g')
        .attr('class', 'y-axis')
        .call(yAxis)
   }

   update(curr_neighbourhood_data);
}
