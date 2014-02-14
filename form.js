$(document).ready(function() {
  var entitySelection = $(".entityVal").val();
  console.log(entitySelection);
  if (entitySelection === "individual") {
    $("#individual").show();
    $("#race").hide();
    $("#candidate").hide();
    $("#committee").hide();
    $("#submitSearch").hide();
  }
  $("#entity").on('change', '.entityVal', function() {
    entitySelection = $(".entityVal").val();
    console.log(entitySelection);
    if (entitySelection === "race") {
      $("#race").slideDown("fast");
      $("#submitSearch").slideDown("fast");
      $("#candidate").hide();
      $("#committee").hide();
      $("#individual").hide();
    }
    else if (entitySelection === "candidate") {
      $("#candidate").slideDown("fast");
      $("#submitSearch").slideDown("fast");
      $("#committee").hide();
      $("#race").hide();
      $("#individual").hide();
    }
    else if (entitySelection === "committee") {
     $("#committee").slideDown("fast");
     $("#submitSearch").slideDown("fast");
     $("#race").hide();
     $("#candidate").hide();
     $("#individual").hide();
    }
   else if (entitySelection === "individual") {
    $("#individual").slideDown("fast");
    $("#race").hide();
    $("#submitSearch").hide();
    $("#candidate").hide();
    $("#committee").hide();
   } 
  });
  $('#committeeForm').on('submit', 'form',  function(event) {
    event.preventDefault();
    $.ajax("name.cgi", {
      type: 'POST',
      data: $(this).serialize(),
      success: function(result) {
        $('#committeeForm').append('<p class="committeeResult">'+result+'</br><button type="button">Remove Results</button></p>');}
    });
  });
  $('#committeeForm').on('click', 'button', function() {
    $(this).closest('.committeeResult').remove();
  });
});
