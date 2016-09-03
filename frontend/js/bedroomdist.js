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
function bedroomDistribution (id) {
  // Margins to center and transform the graph
  var margin = {top: 20, right: 20, bottom: 30, left: 50},
      width = 500 - margin.left - margin.right,
      height = 300 - margin.top - margin.bottom;
  // Initializate x value mapping functions and axis
  var xScale = d3.scaleLinear().range([0, width]),
      xMap = function (d, i) { return xScale(i); },
      xAxis = d3.axisBottom()
                .scale(xScale);
  // TODO: count number of postings for each number of bedrooms and map that number to bar chart height
  // Initializate y value mapping functions and axis
  var yScale = d3.scaleLinear().range([height, 0]),
      yMap = function (d) { return yScale(d); },
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

    function filterCallback(d) {
      return d.bedrooms <= 8;
    }

    // TODO: function that grabs data from most recently clicked neighbourhood
    //  For now default to 'Outside' data points and 'All' data points as background
    outsideData = data[data.length - 1]['positions'].sort(sortMinToMaxCallback).filter(filterCallback);

    // Initialize an array of 0's of size maxBedrooms
    var maxBedrooms = d3.max(outsideData, function (d) { return d.bedrooms; });
    var bedBinArray = new Array(maxBedrooms+1);
    bedBinArray.fill(0);

    /** Bin postings by bedroom
     * @param {array} data: list of data for postings, with x and y values
     * @param {array} bedBinArray: empty array to hold predicted line coordinates
     */
    function binPostingByBeds (data, bedBinArray) {
      for (var i = 0; i < data.length; i++) {
        bedBinArray[data[i].bedrooms] += 1;
      }
    }

    binPostingByBeds(outsideData, bedBinArray);
    // console.log(bedBinArray)

    xScale.domain([0, maxBedrooms]);
    yScale.domain([0, d3.max(bedBinArray)]);

    svg.append('g')
       .attr('class', 'x-axis')
       .attr('transform', 'translate(0,'+height+')')
       .call(xAxis);

   function adjustTextLabels(selection) {
     selection.selectAll('major tick')
       .attr('transform', 'translate(' + maxBedrooms / width + ',0)');
   }

    svg.append('g')
       .attr('class', 'y-axis')
       .call(yAxis)

    var maxOfBins = d3.max(bedBinArray);

     svg.append('g').selectAll('bar')
             .data(bedBinArray)
           .enter()
             .append('rect')
             .attr('class', 'bar')
             .attr('x', xMap)
             .attr('width', width / (maxBedrooms+1))
             .attr('y', yMap)
             .attr('height', function (d) { return height - yScale(d); });

      svg.append('text')
            .attr('class', 'title')
            .attr('x', width / 2)
            .attr("dx", "15px")
            .attr('dy', '-5px')
            .style('text-anchor', 'middle')
            .text('Distribution of Bedrooms per Post');
   });
}
