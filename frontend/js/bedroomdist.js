/**
 * Creates an bar chart of num postings vs num bedrooms using the D3.js API
 * @param {string} id - id of tag to place svg object within
 * @param {JSON} curr_neighbourhood_data - json object of the form
 *
 *        [{
 *         bedrooms : int,
 *         price : int,
 *         date_listed : int
 *        },]
 */
function bedroomDistribution (id, curr_neighbourhood_data) {
  // Margins to center and transform the graph
  var margin = {top: 20, right: 20, bottom: 30, left: 50},
      width = 500 - margin.left - margin.right,
      height = 300 - margin.top - margin.bottom;
  // Initializate x value mapping functions and axis
  var xScale = d3.scaleLinear().range([0, width]),
      xMap = function (d, i) { return xScale(i); },
      xAxis = d3.axisBottom()
                .scale(xScale);

  // Initializate y value mapping functions and axis
  var yScale = d3.scaleLinear().range([height, 0]),
      yMap = function (d) { return yScale(d); },
      yAxis = d3.axisLeft()
                .scale(yScale)
                .ticks(5);

  var formatCount = d3.format(",.0f");

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

    // Initialize an array of 0's of size maxBedrooms
    var maxBedrooms = d3.max(data, function (d) { return d.bedrooms; });
    var bedBinArray = new Array(maxBedrooms+1);
    bedBinArray.fill(0);

    // Bin postings by bedroom
    for (var i = 0; i < data.length; i++) {
      bedBinArray[data[i].bedrooms] += 1;
    }

    xScale.domain([0, maxBedrooms]);

    var histogram = d3.histogram()
          .domain(xScale.domain())
          .thresholds(xScale.ticks(maxBedrooms))
          (bedBinArray);

    yScale.domain([0, d3.max(histogram, function (d) { return d.length; })]);

    // // Transition callback
    // var neiTransition = d3.transition()
    //                       .duration(750);
    //
    // var prevPostings = svg.selectAll('bar')
    //       .data(data, function (d) { return d; });

    // prevPostings.exit()
    //             .attr('class', 'exit')
    //           .transition(neiTransition)
    //             .attr('y', 60)
    //             .style('fill-opacity', 1e-6)
    //             .remove();
    //
    // prevPostings.enter().append('rect')
    //             .attr('class', 'bar')
    //             .attr('x', xMap)
    //             .attr('width', width / (maxBedrooms+1))
    //             .attr('y', yMap)
    //             .attr('height', function (d) { return height - yScale(d); })
    //           .transition(neiTransition)
    //             .attr('y', 0)
    //             .style('fill-opacity', 1);

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

    bar.append("text")
      .attr("dy", ".75em")
      .attr("y", 6)
      .attr("x", (xScale(histogram[0].x1) - xScale(histogram[0].x0)) / 2)
      .attr("text-anchor", "middle")
      .text(function(d) { return formatCount(d.length); });

    svg.append('text')
      .attr('class', 'title')
      .attr('x', width / 2)
      .attr("dx", "15px")
      .attr('dy', '-5px')
      .style('text-anchor', 'middle')
      .text('Distribution of Bedrooms per Post');

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
