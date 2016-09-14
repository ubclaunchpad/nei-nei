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
  var margin = {top: 20, right: 20, bottom: 30, left: 50},
      width = 500 - margin.left - margin.right,
      height = 300 - margin.top - margin.bottom;

  var xScale = d3.scaleBand().range([0, width]);

  var yScale = d3.scaleLinear().range([height, 0]);

  var xAxis = d3.axisBottom()
      .scale(xScale);

  var yAxis = d3.axisLeft()
      .scale(yScale)
      .ticks(5);

  var svg = d3.select("div#"+id)
      .append("svg")
        .attr("class", "chart")
        .attr("id", "chart1")
        .attr("preserveAspectRatio", "xMinYMin meet")
        .attr("viewBox", "0 0 500 350")
      .append("g")
        .attr("transform", "translate(" + (margin.left + margin.bottom) + "," + margin.top + ")");

  function update(data) {

    var maxBeds = d3.max(data, function (d) { return d.bedrooms; }),
        bedBins = new Array(maxBeds+1),
        bedDomain = new Array(maxBeds);

    bedBins.fill(0);

    data.forEach(function (d) {
      bedBins[d.bedrooms] += 1;
    });

    for (var i = 0; i < maxBeds; i++) {
      bedDomain[i] = i + 1;
    }

    xScale.domain(bedDomain);
    yScale.domain([0, d3.max(bedBins, function(d) { return d; })]);

    svg.append("text")
      .attr('class', 'x-axis-title')
      .attr("y", height)
      .attr('x', width / 2)
      .attr("dy", "3em")
      .style("text-anchor", "middle")
      .text("Number of Beds");

    svg.append("text")
      .attr('class', 'y-axis-title')
      .attr("transform", "rotate(-90)")
      .attr("y", 0 - margin.left)
      .attr('x', 0 - (height / 2))
      .attr("dy", "0.25em")
      .style("text-anchor", "middle")
      .text("Number of Posts");

    svg.append("g")
        .attr("class", "x-axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis)
        .selectAll("text")
          .style("text-anchor", "center")
          .text(function (d) { return d; });

    svg.append("g")
        .attr("class", "y-axis")
        .call(yAxis)
      .append("text");

    svg.selectAll("bar")
        .data(bedBins)
      .enter().append("rect")
        .attr('class', 'bar')
        .attr("x", function(d, i) { return xScale(i); })
        .attr("width", xScale.bandwidth() - 1)
        .attr("y", function(d) { return yScale(d); })
        .attr("height", function(d) { return height - yScale(d); });

    svg.append('text')
      .attr('class', 'title')
      .attr('x', width / 2)
      .attr("dx", "15px")
      .attr('dy', '-5px')
      .style('text-anchor', 'middle')
      .text('Distribution of Posts per Bedrooms');

   }

  update(curr_neighbourhood_data);

}
