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
	var resultArray = jQuery.parseJSON(result);
        var committeeArray = new Array();
        for (var i=0; i < resultArray.length; i++) {
         committeeArray[i] = '<input class="checkCommittee" type="checkbox" value="'+resultArray[i][0]+'">'+resultArray[i][1]+", "+resultArray[i][4]+'</br>';
        }
        $('#committeeForm').append('<p class="committeeResult">'+committeeArray.join("")+'<button type="button">Remove Results</button></p>');
        }
    });
  });
  
  $('#committeeForm').on('click', 'button', function() {
    $(this).closest('.committeeResult').remove();
  });
  var nameID = new Array();
  $('#committeeForm').on('click', '.checkCommittee', function() {
    var nameIDValue = $(this).val();
    if (nameID.indexOf(nameIDValue) === -1) {
      nameID.push(nameIDValue);
    }
    else {
      nameID.splice((nameID.indexOf(nameIDValue)), 1);
    }
    console.log(nameID);
  });
  $('#refine').on('submit', 'form', function(event) {
    event.preventDefault();
    console.log('committeeNameID="'+nameID[i]+'"&'+'entityOneType="committee"&'+$(this).serialize());
    if (nameID.length > 0) {
      console.log(nameID);
      for (var i=0; i < nameID.length; i++) {
        $.ajax("cfCGI.cgi", {
          type: 'POST',
          data: ('committeeNameID='+nameID[i]+'&'+'entityOneType=committee&'+$(this).serialize()),
          success: function(result) {
          var dataArray = jQuery.parseJSON(result);
          console.log(dataArray);
          $('#results').append('<p class="dataResult">'+dataArray+"</p></br></br>");
          }
        });
      }
    }
  });  
});
