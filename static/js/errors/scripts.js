$(document).ready(function() {
  showPolygons();
  setInterval(function(){
    showPolygons();
  },2500)
})

function showPolygons() {
  
  $('[class="processed"]').removeAttr('class');
  var polyCount = $('polygon').length;
  
  $('polygon').each(function(ind, el) {
    setTimeout(function() {
       $('polygon:eq(' + ind + ')').attr('class', 'processed');
    }, Math.random() * 2000);
  });
}