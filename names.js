$(document).ready(function() {
  $('.committees').on('submit', 'form',  function(event) {
    event.preventDefault();
    $.ajax("name.cgi", {
      type: 'POST',
      data: $('form').serialize(),
      success: function(result) {
        $(this).append(result);}
    });
  });
});
