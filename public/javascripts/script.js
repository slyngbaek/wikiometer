$(function(){  // $(document).ready shorthand
   if ($('#score').length == 0) {
      $('#score-card').hide();
   }
   else {
      $('#score-card').css('visibility','visible').hide().fadeIn('slow');
   }

   // $("form").submit(function(e) {
   //     e.preventDefault(); // Prevents the page from refreshing
   //     var $this = $(this); // `this` refers to the current form element
   //     $.post(
   //         $this.attr("action"), // Gets the URL to sent the post to
   //         $this.serialize(), // Serializes form data in standard format
   //         function(data) { /** code to handle response **/ },
   //         "json" // The format the response should be in
   //     );
   // });
});
