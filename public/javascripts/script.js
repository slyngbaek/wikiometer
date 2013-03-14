$(function(){  // $(document).ready shorthand
   if ($('#score').length == 0) {
      $('#score-card').hide();
   }
   else {
      $('#score-card').css('visibility','visible').hide().fadeIn('slow');
   }
});
