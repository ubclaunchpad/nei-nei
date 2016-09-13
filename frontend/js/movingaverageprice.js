/**
 * Creates an exponential moving average plot using the D3.js API
 * @param {string} id - id of tag to place svg object within
 * @param {JSON} curr_neighbourhood_data - json object of the form
 *
 *        [{
 *         bedrooms : int,
 *         price : int,
 *         date_listed : int
 *        },]
 */
function movingAverage (id, curr_neighbourhood_data) {
  // Margins to center and transform the graph
  var margin = {top: 20, right: 20, bottom: 30, left: 50},
      width = 500 - margin.left - margin.right,
      height = 300 - margin.top - margin.bottom;
  // Initializate x value mapping functions and axis
  var xValue = function (d) { return new Date(d.date_listed * 1000); },
      xScale = d3.scaleTime().range([0, width]),
      xMap = function (d) { return xScale(xValue(d)); },
      xAxis = d3.axisBottom()
                .scale(xScale);
  // Initializate y value mapping functions and axis
  var yValue = function (d) { return d.price; },
      yScale = d3.scaleLinear().range([height, 0]),
      yMap = function (d) { return yScale(yValue(d)); },
      yAxis = d3.axisLeft()
                .scale(yScale)
                .ticks(4);
  // Create area object
  var area = d3.area()
      .x( xMap )
      .y0( height )
      .y1( yMap )
      .curve(d3.curveBasis);

  var svg = d3.select("div#"+id)
           .append("svg")
              .attr("class", "chart")
              .attr("id", "chart1")
              .attr("preserveAspectRatio", "xMinYMin meet")
              .attr("viewBox", "0 0 500 350")
           .append("g")
             .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  function update(data) {

    function sortMinToMaxCallback(a, b) { return a.date_listed - b.date_listed; }
    function sortMaxToMinCallback(a, b) { return b.date_listed - a.date_listed; }

    // Consolidate all listings from api
    var allData = [];
    for (var hood in listingsDictionary) {
      allData = allData.concat(listingsDictionary[hood]);
    }
    allData = allData.sort(sortMinToMaxCallback);

    // TODO: Bin by date
    var formatDate = d3.timeFormat("%B %e %Y");

    data.forEach(function (d) {
      d.date_bin = formatDate(d.date_listed * 1000);
    });

    allData.forEach(function (d) {
      d.date_bin = formatDate(d.date_listed * 1000);
    });

    // Find earliest data point from each set to set domain
    var maxMinArray = [allData[d3.scan(allData, sortMinToMaxCallback)], data[d3.scan(data, sortMinToMaxCallback)]];
    // Find index of the largest time between the two
    var maxMinIndex = d3.scan(maxMinArray, sortMaxToMinCallback);
    var lowerCutoff = maxMinArray[maxMinIndex].date_listed;
    var upperCutoff = maxMinArray[maxMinIndex == 0 ? 1 : 0].date_listed;
    // Filter to normalize lower bound
    function filterCallback(d) {
      return d.date_listed >= lowerCutoff;
    };
    data = data.filter(filterCallback);
    allData = allData.filter(filterCallback);
    // Set first element's x of both arrays to lowerCutoff
    allData[0].date_listed = lowerCutoff;
    data[0].date_listed = lowerCutoff;

    // Exponential moving average function
    function calculateEMA(currPrice, dayRange, prevEMA) {
      var k = 2 / (dayRange + 1);
      return (currPrice * k) + (prevEMA * (1 - k));
    }
    function emaOverRange(rawData, dayRange, emaData) {
      var tempEMA = 0,
          lastEMA = rawData[0].price;
      emaData.push({
        'price': lastEMA,
        'date_listed': rawData[0].date_listed
      });
      for (var i = 1; i < rawData.length; i++) {
        tempEMA = calculateEMA(rawData[i].price, dayRange, lastEMA);
        emaData.push({
          'price': tempEMA,
          'date_listed': rawData[i].date_listed
        });
        lastEMA = tempEMA;
      }
    }

    // 25 day exponential moving average
    // TODO: convert dayRange to user input
    var dayRange = 25;
    var movingAvgDataHood = [],
        movingAvgDataAll = [];
    emaOverRange(data, dayRange, movingAvgDataHood);
    emaOverRange(allData, dayRange, movingAvgDataAll);

    xScale.domain(d3.extent(movingAvgDataAll, xValue))
          .ticks(d3.timeMonth.every(1));
    yScale.domain([0, d3.max(movingAvgDataAll, yValue)]);

    svg.append('g')
       .attr('class', 'x-axis')
       .attr('transform', 'translate(0,'+height+')')
       .call(xAxis);

    svg.append('g')
       .attr('class', 'y-axis')
       .call(yAxis)

    svg.append('g').append('path')
            .attr('class', 'area')
            .attr('d', area(movingAvgDataAll))
            .attr('stroke', 'grey')
            .attr('stroke-width', 1)
            .attr('fill', 'red');

    svg.append('g').append('path')
            .attr('class', 'area')
            .attr('d', area(movingAvgDataHood))
            .attr('stroke', 'grey')
            .attr('stroke-width', 1)
            .attr('fill', 'steelblue');

     svg.append('text')
           .attr('class', 'title')
           .attr('x', width / 2.2)
           .attr('dx', '15px')
           .attr('dy', '-5px')
           .style('text-anchor', 'middle')
           .text('Exp. Moving Average');
   }

   update(curr_neighbourhood_data);
}
