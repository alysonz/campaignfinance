//wait for DOM to load fully
$(document).ready(function() {
  //log the entity selection on load of page, which should always be individual
  var entitySelection = $(".entityVal").val();
  console.log(entitySelection);
  if (entitySelection === "individual") {
    //hide all of the committee search option, show only individual
    $("#individual").show();
    $("#race").hide();
    $("#candidate").hide();
    $("#committee").hide();
    $("#submitSearch").hide();
  }
  $("#entity").on('change', '.entityVal', function() {
    //when the user chooses a new search method, get that selection
    entitySelection = $(".entityVal").val();
    console.log(entitySelection);
    //if race, reset form, show race options, hide all other options
    if (entitySelection === "race") {
      $('#refine').find('form').trigger('reset');
      $("#race").slideDown("fast");
      $("#submitSearch").slideDown("fast");
      $("#candidate").hide();
      $("#committee").hide();
      $("#individual").hide();
    }
    //if candidate, reset form, show candidate options, hide all other options
    else if (entitySelection === "candidate") {
      $('#refine').find('form').trigger('reset');
      $("#candidate").slideDown("fast");
      $("#submitSearch").slideDown("fast");
      $("#committee").hide();
      $("#race").hide();
      $("#individual").hide();
    }
    //if committee, reset form, show committee options, hide all other options
    else if (entitySelection === "committee") {
     $('#refine').find('form').trigger('reset');
     $("#committee").slideDown("fast");
     $("#submitSearch").slideDown("fast");
     $("#race").hide();
     $("#candidate").hide();
     $("#individual").hide();
    }
   //if individual, don't reset form, hide all committee search options, show only individual
   else if (entitySelection === "individual") {
    $("#individual").slideDown("fast");
    $("#race").hide();
    $("#submitSearch").hide();
    $("#candidate").hide();
    $("#committee").hide();
   } 
  });
  $('#committeeForm').on('submit', 'form',  function(event) {
  //when the user submits a committee search
    event.preventDefault();
    $.ajax("name.cgi", {
      type: 'POST',
      data: $(this).serialize(),
      //show working animation
      beforeSend: function() {
        $('#committeeForm').find('#working').removeClass('hide');
        $('#committeeForm').find('#working').addClass('show');
      },
      timeout: 10000,
      //set error message
      error: function (request, errorType, errorMessage) {
        $('#refine').find('#working').removeClass('show');
        $('#refine').find('#working').addClass('hide');
        alert('Error: '+errorType+'. Try narrowing search parameters.');
      },
      success: function(result) {
        //parse JSON
	var resultArray = jQuery.parseJSON(result);
        //set blank array for iterating through results and adding style
        var committeeArray = new Array();
        for (var i=0; i < resultArray.length; i++) {
         //iterate through results array, add checkbox input with class, add id and committee name data to input , committee information text inside of input
         committeeArray[i] = '<input class="checkCommittee '+resultArray[i][0]+'" type="checkbox" value="'+resultArray[i][0]+'"'+'data-ID="'+resultArray[i][0]+'"'+' data-committeeName="'+resultArray[i][1]+'">'+resultArray[i][1]+", "+resultArray[i][4]+'</br>';
        }
        //append styled array to results paragraph, add button to get rid of checkbox block
        $('#committeeForm').append('<p class="committeeResult">'+committeeArray.join("")+'<button type="button">Remove Results</button></p>');
      },
      //hide working animation when done
      complete: function() {
        $('#committeeForm').find('#working').removeClass('show');
        $('#committeeForm').find('#working').addClass('hide');
      }
    });
  }); 
  //create blank array for getting rid of checkbox blocks
  var dropList = new Array();
  //on click of remove button
  $('#committeeForm').on('click', 'button', function() {
    //grab all data arrays from the siblings of the remove button, which will be all of the committee id and name data of the checkbox inputs. store in blank array
    dropList = $.map($(this).siblings(), function(el) {
    return $(el).data();});
    //remove the results paragraph that the button belongs to
    $(this).closest('.committeeResult').remove();
    console.log(dropList);
    //iterate through array of checkbox data
    for (var i=0; i < dropList.length; i++) {
      //if the id has a index in the nameID list, drop it
      if (nameID.indexOf(dropList[i]) !== -1) {
        nameID.splice((nameID.indexOf(dropList[i])), 1);
      }
    }
  });
  //create array for loading the ids of selected committees
  var nameID = new Array();
  //on checking or unchecking a checkbox
  $('#committeeForm').on('click', '.checkCommittee', function() {
    //retrieve value from input tag
    var nameIDValue = $(this).val();
    //retrieve data from input tag
    var committeeNameData = $(this).data();
    //if nameID does not have the data from the selected input, add it to the list
    if (nameID.indexOf(committeeNameData) === -1) {
      nameID.push(committeeNameData);
    }
    //nameID does have the data from the selected input, drop it
    else {
      nameID.splice((nameID.indexOf(committeeNameData)), 1);
    }
    console.log(nameID);
  });
  //on submitting the main form with filter options
  $('#refine').on('submit', 'form', function(event) {
    //do not load CGI
    event.preventDefault();
    console.log($(this));
    //if there are committee ids in the nameID list
    if (nameID.length > 0) {
      console.log($(this).val());
      //iterate through list and send ajax call for each id
      for (var i=0; i < nameID.length; i++) {
        //add committee id and committee as entity to list of information to sent to CGI script
        var formData = 'committeeNameID='+nameID[i]["id"]+'&'+'entityOneType=committee&'+$(this).serialize();
	console.log(formData);
        $.ajax("cfCGI.cgi", {
          type: 'POST',
          data: formData,
          //show working animation
          beforeSend: function() {
          $('#refine').find('#working').removeClass('hide');
          $('#refine').find('#working').addClass('show');
          },
          timeout: 10000,
          //set error message
          error: function (request, errorType, errorMessage) {
            alert('Error: '+errorType+'. Try narrowing search parameters.');
          },
          success: function(result) {
            console.log(result);
            //parse results
            var dataArray = jQuery.parseJSON(result);
            //get committee id from results
            var committeeID = dataArray[0][0];
            //set locator for paragraph with class if committee id
            var paragraph = $('#results').find("."+committeeID);
            //prepare existing committee tabs to receive siblings by removing all selected styling
            $('#results').find('#data').children().removeClass('show');
            $('#results').find("#tabBar").children().removeClass('highlight');
            //if there is not a paragraph with the class of the result committee id
            if (paragraph.length < 1) {
              //give results to if statement (for some reason it was undefined if I didn't do this again)
              var dataArray = jQuery.parseJSON(result);
              var committeeID = dataArray[0][0];
              var paragraph = $('#data').find("."+committeeID);
              console.log(dataArray);
              //in tab bar, create a new overall tab container with class and data with committee id
              $('#tabBar').append('<div id="tab" data-id="'+committeeID+'" class="'+committeeID+'"></div>');
              //add close tab image to tab container
              $('#tabBar').find("."+committeeID).append('<img src="close.png">'); 
              //if the second list contains only one item, it's an error message
              if (dataArray[2].length < 2) {
                //so in the main data field, add a containder for the results with the class of the committee id
                $('#data').append('<div id="dataResult" class="'+committeeID+'">'+'</div>');
                console.log(formData);
                var id = dataArray[0][0];
                //grab data array from the committee result input checkbox with the same committee id
                var committeeArray = $('.committeeResult').find("."+id).data();
                //select committee name value from that data array for the results headline since we can't find it in the error results
                var committeeName = committeeArray["committeename"]
                //add error text to tab
                $('#tabBar').find("."+committeeID).append('<div id="tabName" class="error">Error</div>');
                //set headline so we know which committee selection threw the error
                $('#data').find("."+committeeID).append('<h3>'+committeeName+'</h3>');
                //print out results we did get back since that should contain a detailed error message from cfquery.py
                $('#data').find("."+committeeID).append('<p class="dataResult error">'+dataArray[2]+'</p>');
                
              }
              //if the data does look like it has returned without an 'undefined' error
              else {
                //set committee name from results
                var committeeName = dataArray[2][1];
                //set tab to contain committee name 
                $('#tabBar').find("."+committeeID).append('<div id="tabName">'+committeeName+'</div>');
                //create results container with id of committee
                $('#data').append('<div id="dataResult" class="'+committeeID+'">'+'</div>');
                //insert committee name as headline, link for downloading from download.CGI with the same formData, and add results array
                $('#data').find("."+committeeID).append('<h3>'+committeeName+'</h3>');
                $('#data').find("."+committeeID).append('<a href="http://wildfire.codercollective.org/testcampaignfinance/download.cgi?'+formData+'">Download Data</a>')
                $('#data').find("."+committeeID).append('<p class="dataResult">'+dataArray+'</p>');
              }
            }
            //if this is a duplicated request, ie, there is already a tab with results for the committee in question
            else {
              var dataArray = jQuery.parseJSON(result);
              var committeeID = dataArray[0][0];
              //if the duplication is now an error
              if (dataArray[2].length < 2) {
                //if the old tab did not have error text, replace text with error
                if(($('#tabBar').find("."+committeeID).find(".error")).length < 1) {
                  $('#tabBar').find("."+committeeID).find("#tabName").remove();
                  $('#tabBar').find("."+committeeID).append('<div id="tabName" class="error">Error</div>');
                }
                //leave headline in place but remove download link and data results
                $('#data').children('.'+committeeID).children('p').remove();
                $('#data').children('.'+committeeID).children('a').remove();
                //replace data results with error message from cfquery.py
                $('#data').find("."+committeeID).append('<p class="dataResult error">'+dataArray[2]+'</p>');
              }
              //if results are not an error
              else {
              var committeeName = dataArray[2][1];
              //but the previous results /were/ an error
              if(($('#tabBar').find("."+committeeID).find(".error")).length > 0) {
                //replace error text with the committee name
                $('#tabBar').find("."+committeeID).find("#tabName").remove();
                $('#tabBar').find("."+committeeID).append('<div id="tabName">'+committeeName+'</div>');
              }
              //load replace old results with new results
              $('#data').children('.'+committeeID).children('p').remove();
              $('#data').children('.'+committeeID).append('<p class="dataResult">'+dataArray+'</p>');  
              }
            }
          },
          //remove working animation, remove selected styling from everything, add selected styling to first tab and corresponding data result
          complete: function () {
            $('#refine').find('#working').removeClass('show');
            $('#refine').find('#working').addClass('hide');
            $('#results').find('#data').children().addClass('hide');
            $('#results').find('#dataResult').removeClass('hide');
            $('#results').find('#dataResult').addClass('show');
            $('#results').find("#tab").addClass('highlight');
          }
        });
      }
    }   
    //for individual searches, parse form information on submit to retrieve values for entityOneFirstName and ''LastName 
    var individualName = ($(this).serialize()).split('&');
    individualName[0] = individualName[0].split('=');
    individualName[0] = individualName[0][1].split('=');
    individualName[1] = individualName[1].split('=');
    individualName[1] = individualName[1][1];
    individualName = individualName[0]+individualName[1];
    console.log(individualName);
    //if there was input into the first and last name fields for an individual search
    if (individualName.length > 0) {
      //prepare data to send to cfCGI.cgi
      var formData = 'entityOneType=individual&'+$(this).serialize();
      console.log(formData);
      $.ajax("cfCGI.cgi", {
        type: 'POST',
        data: formData,
        //add working animation
        beforeSend: function() {
        $('#refine').find('#working').removeClass('hide');
        $('#refine').find('#working').addClass('show');
        },
        timeout: 10000,
        //add error message for timeout
        error: function (request, errorType, errorMessage) {
          $('#refine').find('#working').removeClass('show');
          $('#refine').find('#working').addClass('hide');
          alert('Error: '+errorType+'. Try narrowing search parameters.');
        },
        success: function(result) {
          //parse results
          var dataArray = jQuery.parseJSON(result);
          //grab individual name from results
          var name = dataArray[0][0]+ dataArray[0][1];
          //set variable to locate class with individual name to see if a tab is already open
          var paragraph = $('#results').find("."+name);
          //remove all select styles
          $('#results').find('#data').children().removeClass('show');
          $('#results').find("#tabBar").children().removeClass('highlight');
          //if there is not already a paragraph for the searched individual
          if (paragraph.length < 1) {
            var dataArray = jQuery.parseJSON(result);
            console.log(dataArray);
            //make a tab name with a space
            var tabName = dataArray[0][0]+' '+ dataArray[0][1];
            //make a class name without a space
            var name = dataArray[0][0]+ dataArray[0][1];
            //add a tab container with class of individual
            $('#tabBar').append('<div id="tab" data-id="'+name+'" class="'+name+'">'+'</div>');
            //add close tab image
            $('#tabBar').find("."+name).append('<img src="close.png">');
            //add tab text container and tab name
            $('#tabBar').find("."+name).append('<div id="tabName">'+tabName+'</div>');
            //add data result container with class of individual
            $('#data').append('<div id="dataResult" class="'+name+'">'+'</div>');
            var paragraph = $('#data').find("."+name);
            //add headline, download link and data results and hide all tabs
            $(paragraph).append("<h3>"+tabName+"</h3>");
            $(paragraph).append('<a href="http://wildfire.codercollective.org/testcampaignfinance/download.cgi?'+formData+'">Download Data</a>');
            $(paragraph).append('<p class="dataResult">'+dataArray+"</p>");
            $('#data').children().addClass('hide');
          }
          //if a tab does exist for the searched individual
          else {
            var dataArray = jQuery.parseJSON(result);
            var name = dataArray[0][0]+ dataArray[0][1];
            //remove existing data from results container and replace with new results
            $('#data').children('.'+name).children('p').remove();
            $('#data').children('.'+name).append('<p class="dataResult">'+dataArray+'</p>');
          }
        },
        //remove working animation, hide all tabs, show first tab and first data result
        complete: function() {
          $('#refine').find('#working').removeClass('show');
          $('#refine').find('#working').addClass('hide');
          $('#results').find('#data').children().addClass('hide');
          $('#results').find('#dataResult').removeClass('hide');
          $('#results').find('#dataResult').addClass('show');
          $('#results').find("#tab").addClass('highlight');
        }
      });
    }
  });
  //on selecting a tab for tab navigation
  $('#tabBar').on('click', '#tabName', function () {
    //get tab's data
    var committeeData = $(this).closest('#tab').data();
    console.log(committeeData["id"]);
    //remove highlighted from all tabs
    $('#tabBar').children().removeClass('highlight');
    //add highlighted to the tab that was clicked
    $(this).closest("#tab").addClass('highlight');
    //remove the show class from all results, add hide to all results
    $('#results').find('#data').children().removeClass('show');
    $('#results').find('#data').children().addClass('hide');
    //remove hide from the results with class matching tab data and add show
    $('#data').find("."+committeeData["id"]).removeClass('hide');
    $('#data').find("."+committeeData["id"]).addClass('show'); 
  });
  //on clicking the close image in the tab
  $('#tabBar').on('click', 'img',  function () {
    //grab data from parent tab container, check to see if parent is highlighted
    var committeeData = $(this).closest('#tab').data();
    var committeeTab = $(this).parent('highlighted');
    //if parent is not highlighted, remove tab and corresponding results container
    if (committeeTab.length < 1) {
      $(this).closest('#tab').remove();
      $('#data').find("."+committeeData["id"]).remove();
    }
    //if the tab container is highlighted
    else {
      //remove tab and corresponding data result, highligh first tab and show first data result
      $(this).closest('#tab').remove();
      $('#data').find("."+committeeData["id"]).remove();
      $('#data').find('#dataResult').removeClass('hide');
      $('#data').find('#dataResult').addClass('show');
      $('#tabBar').find("#tab").addClass('highlight');
    }
  });  
});
