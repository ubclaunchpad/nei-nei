
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

   var monthFormat = d3.timeFormat('%b');
   var months = [], currMonth;

   data.forEach(function (d) {
     currMonth = monthFormat(d.date_listed*1000);
     d.month_bin = currMonth;
     if (!months.includes(currMonth)) {
       months.push(currMonth);
     }
   });

   // Initializate x value mapping functions and axis
   var xScale = d3.scaleOrdinal().domain(months).range([0, width]);

   var histogram = d3.histogram()
         .domain(xScale.domain())
         .value(function(d) { return d.month_bin;});

    var bins = histogram(data);

    yScale.domain([0, d3.max(bins, function (d) { return d.length; })]);

    var bar = svg.selectAll('bar')
        .data(bins)
      .enter().append('g')
        .attr('class', 'bar')
        .attr('transform', function (d) {
          return 'translate(' + xScale(d.x0) + "," + yScale(d.length) + ')'; });

    bar.append('rect')
       .attr('width', xScale(bins[0].x1) - xScale(bins[0].x0) - 1)
       .attr('height', function (d) { return height - yScale(d.length); });

     svg.append('text')
        .attr('class', 'title')
        .attr('x', width / 2)
        .attr("dx", "15px")
        .attr('dy', '-5px')
        .style('text-anchor', 'middle')
        .text('Posts per Month');
        
    
     xAxis = d3.axisBottom().scale(xScale);

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
