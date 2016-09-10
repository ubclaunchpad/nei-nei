$(document).ready(function () {

  var dashExpanded = true;

  $('.dash-button').click(function () {
    if (!dashExpanded) {
      $('#dashboard').css('display', 'inline-block');
      $('#markerMap').css('width', '75vw');
      $('.dash-button').text('Contract');
      dashOut = true;
    } else {
      $('#dashboard').css('display', 'none');
      $('#markerMap').css('width', '95vw');
      $('.dash-button').text('Expand');
      dashOut = false;
    }
  });
});
