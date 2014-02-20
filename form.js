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
         committeeArray[i] = '<input class="checkCommittee" type="checkbox" value="'+resultArray[i][0]+'"'+'data-ID="'+resultArray[i][0]+'"'+' data-committeeName="'+resultArray[i][1]+'">'+resultArray[i][1]+", "+resultArray[i][4]+'</br>';
        }
        $('#committeeForm').append('<p class="committeeResult">'+committeeArray.join("")+'<button type="button">Remove Results</button></p>');
        }
    });
  }); 
  var dropList = new Array();
  $('#committeeForm').on('click', 'button', function() {
    dropList = $.map($(this).siblings(), function(el) {
    return $(el).data();});
    $(this).closest('.committeeResult').remove();
    console.log(dropList);
    for (var i=0; i < dropList.length; i++) {
      if (nameID.indexOf(dropList[i]) !== -1) {
        nameID.splice((nameID.indexOf(dropList[i])), 1);
      }
    }
  });
  var nameID = new Array();
  $('#committeeForm').on('click', '.checkCommittee', function() {
    var nameIDValue = $(this).val();
    var committeeNameData = $(this).data();
    if (nameID.indexOf(committeeNameData) === -1) {
      nameID.push(committeeNameData);
    }
    else {
      nameID.splice((nameID.indexOf(committeeNameData)), 1);
    }
    console.log(nameID);
  });
  $('#refine').on('submit', 'form', function(event) {
    event.preventDefault();
    console.log($(this));
    if (nameID.length > 0) {
      console.log($(this).val());
      for (var i=0; i < nameID.length; i++) {
        var formData = 'committeeNameID='+nameID[i]["id"]+'&'+'entityOneType=committee&'+$(this).serialize();
        $.ajax("cfCGI.cgi", {
          type: 'POST',
          data: formData,
          success: function(result) {
            var dataArray = jQuery.parseJSON(result);
            var committeeID = dataArray[0][0];
            var paragraph = $('#results').find("."+committeeID);
            $('#results').find('#data').children().removeClass('show');
            $('#results').find("#tabBar").children().removeClass('highlight');
            if (paragraph.length < 1) {
              var dataArray = jQuery.parseJSON(result);
              var committeeID = dataArray[0][0];
              var committeeName = dataArray[2][1];
              var paragraph = $('#results').find("."+committeeID);
              console.log(dataArray);
              $('#results').find('#tabBar').append('<p id="tab" data-id="'+committeeID+'">'+committeeName+'</p>');
              $('#results').find('#data').append('<p id="dataResult" class="'+committeeID+'">'+'</p>');
              $('#results').find("."+committeeID).append('<h3>'+committeeName+'</h3>');
              $('#results').find("."+committeeID).append('<a href="http://wildfire.codercollective.org/testcampaignfinance/download.cgi?'+formData+'">Download Data</a>')
              $('#results').find("."+committeeID).append('<p class="dataResult">'+dataArray+'</p>');
            }
          },
          complete: function () {
            $('#results').find('#data').children().addClass('hide');
            $('#results').find('#dataResult').removeClass('hide');
            $('#results').find('#dataResult').addClass('show');
            $('#results').find("#tab").addClass('highlight');
          }
        });
      }
    }
    else {
      var formData = 'entityOneType=individual&'+$(this).serialize();
      $.ajax("cfCGI.cgi", {
        type: 'POST',
        data: formData,
        success: function(result) {
          var dataArray = jQuery.parseJSON(result);
          var name = dataArray[0][0]+ dataArray[0][1];
          var paragraph = $('#results').find("."+name);
          $('#results').find('#data').children().removeClass('show');
          $('#results').find("#tabBar").children().removeClass('highlight');
          if (paragraph.length < 1) {
            var dataArray = jQuery.parseJSON(result);
            console.log(dataArray);
            var tabName = dataArray[0][0]+' '+ dataArray[0][1];
            var name = dataArray[0][0]+ dataArray[0][1];
            $('#results').find('#tabBar').append('<p id="tab" data-id="'+name+'">'+tabName+'</p>');
            $('#results').find('#data').append('<p id="dataResult" class="'+name+'">'+'</p>');
            var paragraph = $('#results').find("."+name);
            $(paragraph).append("<h3>"+tabName+"</h3>");
            $(paragraph).append('<a href="http://wildfire.codercollective.org/testcampaignfinance/download.cgi?'+formData+'">Download Data</a>');
            $(paragraph).append('<p class="dataResult">'+dataArray+"</p>");
            $('#results').find('#data').children().addClass('hide');
          }
        },
        complete: function() {
          $('#results').find('#data').children().addClass('hide');
          $('#results').find('#dataResult').removeClass('hide');
          $('#results').find('#dataResult').addClass('show');
          $('#results').find("#tab").addClass('highlight');
        }
      });
    }
  });
  $('#tabBar').on('click', '#tab', function () {
    committeeData = $(this).data();
    console.log(committeeData["id"]);
    $('#tabBar').children().removeClass('highlight');
    $(this).addClass('highlight');
    $('#results').find('#data').children().removeClass('show');
    $('#results').find('#data').children().addClass('hide');
    $('#data').find("."+committeeData["id"]).removeClass('hide');
    $('#data').find("."+committeeData["id"]).addClass('show');    
    
  });  
});
