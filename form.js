//wait for DOM to load fully
$(document).ready(function() {
  //log the entity selection on load of page, which should always be individual
  var entitySelection = $(".entityVal").val();
  console.log(entitySelection);
  if (entitySelection === "individual") {
    //hide all of the committee search option, show only individual
    $("#individual").show();
    $("#race, #candidate, #committee, #submitSearch").hide();
  }
  $("#entity").on('change', '.entityVal', function() {
    //when the user chooses a new search method, get that selection
    entitySelection = $(".entityVal").val();
    console.log(entitySelection);
    //if race, reset form, show race options, hide all other options
    if (entitySelection === "race") {
      $('#refine').find('form').trigger('reset');
      $("#race, #submitSearch").slideDown("fast");
      $("#candidate, #committee, #individual").hide();
    }
    //if candidate, reset form, show candidate options, hide all other options
    else if (entitySelection === "candidate") {
      $('#refine').find('form').trigger('reset');
      $("#candidate, #submitSearch").slideDown("fast");
      $("#committee, #race, #individual").hide();
    }
    //if committee, reset form, show committee options, hide all other options
    else if (entitySelection === "committee") {
     $('#refine').find('form').trigger('reset');
     $("#committee, #submitSearch").slideDown("fast");
     $("#race, #candidate, #individual").hide();
    }
   //if individual, don't reset form, hide all committee search options, show only individual
   else if (entitySelection === "individual") {
    $("#individual").slideDown("fast");
    $("#race, #submitSearch, #candidate, #committee").hide();
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
        $('#committeeForm').find('#working').removeClass('hide').addClass('show');
      },
      timeout: 10000,
      //set error message
      error: function (request, errorType, errorMessage) {
        $('#refine').find('#working').removeClass('show').addClass('hide');
        alert('Error: '+errorType+'. Try narrowing search parameters.');
      },
      success: function(result) {
        //parse JSON
				var resultArray = jQuery.parseJSON(result);
        //set blank array for iterating through results and adding style
        var committeeArray = new Array();
				console.log(resultArray);
        for (var i=0; i < resultArray.length; i++) {
         //iterate through results array, add checkbox input with class, add id and committee name data to input , committee information text inside of input
					if (resultArray[i][3] !== 0) {
         	committeeArray[i] = '<input class="checkCommittee '+resultArray[i][0]+'" type="checkbox" value="'+resultArray[i][0]+'" data-ID="'+resultArray[i][0]+'" data-committeeName="'+resultArray[i][1]+'" data-cycle="'+resultArray[i][3]+'">'+resultArray[i][1]+", "+resultArray[i][2]+', '+resultArray[i][3]+'</br>';
					}
					else {
						committeeArray[i] = '<input class="checkCommittee '+resultArray[i][0]+'" type="checkbox" value="'+resultArray[i][0]+'" data-ID="'+resultArray[i][0]+'" data-committeeName="'+resultArray[i][1]+'" data-cycle="NA">'+resultArray[i][1]+'</br>';
					}
        }
        //append styled array to results paragraph, add button to get rid of checkbox block
        $('#committeeForm').append('<p class="committeeResult">'+committeeArray.join("")+'<button type="button">Remove Results</button></p>');
      },
      //hide working animation when done
      complete: function() {
        $('#committeeForm').find('#working').removeClass('show').addClass('hide');
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
        var formData = 'committeeNameID='+nameID[i]["id"]+'&'+'entityOneType=committee&'+$(this).serialize()+'&download=';
	console.log(formData);
        $.ajax("cfCGI.cgi", {
          type: 'POST',
          data: formData,
          //show working animation
          beforeSend: function() {
          $('#refine').find('#working').removeClass('hide').addClass('show');
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
            //set locator for paragraph with class of committee id
            var paragraph = $('#results').find(".id"+committeeID);
            //prepare existing committee tabs to receive siblings by removing all selected styling
            $('#results').find('#data').children().removeClass('show');
            $('#results').find("#tabBar").children().removeClass('highlight');
            //if there is not a paragraph with the class of the result committee id
            if (paragraph.length < 1) {
              var committeeID = dataArray[0][0];
              var paragraph = $('#data').find(".id"+committeeID);
              console.log(dataArray);
              //in tab bar, create a new overall tab container with class and data with committee id
              $('#tabBar').append('<div id="tab" data-id="'+committeeID+'" class="id'+committeeID+'"></div>');
              //add close tab image to tab container
              $('#tabBar').find(".id"+committeeID).append('<img src="close.png">'); 
              $('#data').append('<div id="dataResult" class="id'+committeeID+'">'+'</div>');
							//if the second list contains only one item, it's an error message
              if (dataArray[2].length < 2) {
                var id = dataArray[0][0];
                //grab data array from the committee result input checkbox with the same committee id
                var committeeArray = $('.committeeResult').find("."+id).data();
                //select committee name value from that data array for the results headline since we can't find it in the error results
                var committeeName = committeeArray["committeename"]
                //add error text to tab
                $('#tabBar').find(".id"+committeeID).append('<div id="tabName" class="error">Error</div>');
                //set headline so we know which committee selection threw the error
								var cycle = $('#search').children('#committeeForm').find('input.'+committeeID).data();
                $('#data').find(".id"+committeeID).append('<h3>'+committeeName+' ('+cycle['cycle']+')</h3><p class="dataResult error">'+dataArray[2]+'</p>');
							}
              //if the data does look like it has returned without an 'undefined' error
              else {
                //set committee name from results
								var committeeName = dataArray[2][1];
								dataArray.splice(0,1);
                console.log(dataArray);
                //set tab to contain committee name 
                $('#tabBar').find(".id"+committeeID).append('<div id="tabName">'+committeeName+'</div>');
                //insert committee name as headline, link for downloading from download.CGI with the same formData, and add results array
								var cycle = $('#search').children('#committeeForm').find('input.'+committeeID).data();
                $('#data').find(".id"+committeeID).append('<h3>'+committeeName+' ('+cycle['cycle']+')</h3><a href="http://wildfire.codercollective.org/testcampaignfinance/download.cgi?'+formData+'&download=True'+'">Download Data</a>');
								$('#data').find(".id"+committeeID).find("h3").append(' <p id="recordCount"> ('+(dataArray.length-1)+' transaction records)</p>');
                d3.select('#data .id'+committeeID)
                .append('table')
                .selectAll('tr')
                .data(dataArray)
                .enter().append('tr')
                .selectAll('td')
                .data(function(d){return d;})
                .enter().append("td")
                .text(function(d) {return d;});
								$('#data').find(".id"+committeeID).find('table').find('tr').first().wrap('<thead></thead>');
								$('#data').find(".id"+committeeID).find('table').find('thead').prepend('<tr class="sort"></tr>')
								for (var i=0; i < dataArray[0].length; i++) {
									$('#data').find(".id"+committeeID).find('table').find('.sort').append('<td><div id="centerSort"><img id="sortUp" src="arrow-right-2.png"><img id="sortDown" src="arrow-left-2.png"></div></td>');
								}
              }
            }
            //if this is a duplicated request, ie, there is already a tab with results for the committee in question
            else {
              var dataArray = jQuery.parseJSON(result);
              var committeeID = dataArray[0][0];
							$('#data').children('.id'+committeeID).find('table, a, p').remove();
              //if the duplication is now an error
              if (dataArray[2].length < 2) {
                //if the old tab did not have error text, replace text with error
                if(($('#tabBar').find(".id"+committeeID).find(".error")).length < 1) {
                  $('#tabBar').find(".id"+committeeID).find("#tabName").remove();
                  $('#tabBar').find(".id"+committeeID).append('<div id="tabName" class="error">Error</div>');
                }
                //replace data results with error message from cfquery.py
                $('#data').find(".id"+committeeID).append('<p class="dataResult error">'+dataArray[2]+'</p>');
              }
              //if results are not an error
              else {
              var committeeName = dataArray[2][1];
							dataArray.splice(0,1);
              //but the previous results /were/ an error
              if(($('#tabBar').find(".id"+committeeID).find(".error")).length > 0) {
                //replace error text with the committee name
                $('#tabBar').find(".id"+committeeID).find("#tabName").remove();
                $('#tabBar').find(".id"+committeeID).append('<div id="tabName">'+committeeName+'</div>');
 //               $('#data').children('.id'+committeeID).children('p').remove();
							}
							$('#data').find(".id"+committeeID).append('<a href="http://wildfire.codercollective.org/testcampaignfinance/download.cgi?'+formData+'&download=True'+'">Download Data</a>')
							$('#data').children('.id'+committeeID).find('h3').append(' <p id="recordCount"> ('+(dataArray.length-1)+' transaction records)</p>');
              //replace old results with new results
              d3.select('#data .id'+committeeID)
              .append('table')
              .selectAll('tr')
              .data(dataArray)
              .enter().append('tr')
              .selectAll('td')
              .data(function(d){return d;})
              .enter().append("td")
              .text(function(d) {return d;});
              }
            }
          },
          //remove working animation, remove selected styling from everything, add selected styling to first tab and corresponding data result
          complete: function () {
            $('#refine').find('#working').removeClass('show').addClass('hide');
            $('#results').find('#data').children().addClass('hide');
            $('#results').find('#dataResult').removeClass('hide').addClass('show');
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
      var formData = 'entityOneType=individual&'+$(this).serialize()+'&download=';
      console.log(formData);
      $.ajax("cfCGI.cgi", {
        type: 'POST',
        data: formData,
        //add working animation
        beforeSend: function() {
        $('#refine').find('#working').removeClass('hide').addClass('show');
        },
        timeout: 10000,
        //add error message for timeout
        error: function (request, errorType, errorMessage) {
          $('#refine').find('#working').removeClass('show').addClass('hide');
          alert('Error: '+errorType+'. Try narrowing search parameters.');
        },
        success: function(result) {
          //parse results
          var dataArray = jQuery.parseJSON(result);
          //grab individual name from results
          var name = dataArray[0][0]+ dataArray[0][1];
          //set variable to locate class with individual name to see if a tab is already open
          var paragraph = $('#results').find(".id"+name);
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
            $('#tabBar').append('<div id="tab" data-id="'+name+'" class="id'+name+'">'+'</div>');
            //add close tab image
            $('#tabBar').find(".id"+name).append('<img src="close.png">');
						//if first item of third list has only one item it is an error message
						$('#data').append('<div id="dataResult" class="id'+name+'">'+'</div>');
						if (dataArray[2].length < 2) {
							$('#tabBar').find(".id"+name).append('<div id="tabName" class="error">Error</div>');
							var paragraph = $('#data').find(".id"+name);
							$(paragraph).append("<h3>"+tabName+'</h3><p class="error">'+dataArray[2][0]+'</p>');
						}
            else{
							//add tab text container and tab name
							dataArray.splice(0,1);
            	$('#tabBar').find(".id"+name).append('<div id="tabName">'+tabName+'</div>');
            	var paragraph = $('#data').find(".id"+name);
            	//add headline, download link and data results and hide all tabs
            	$(paragraph).append('<h3>'+tabName+'</h3><a href="http://wildfire.codercollective.org/testcampaignfinance/download.cgi?'+formData+'&download=True'+'">Download Data</a>');
							$(paragraph).find("h3").append('<p id="recordCount"> ('+(dataArray.length-1)+' transaction records)</p>');
            	d3.select('#data .id'+name)
            	.append('table')
            	.selectAll('tr')
            	.data(dataArray)
            	.enter().append('tr')
            	.selectAll('td')
            	.data(function(d){return d;})
            	.enter().append("td")
            	.text(function(d) {return d;})
            	$('#data').children().addClass('hide');
						}
					}
          //if a tab does exist for the searched individual
          else {
            var dataArray = jQuery.parseJSON(result);
            var name = dataArray[0][0]+ dataArray[0][1];
						var tabName = dataArray[0][0]+' '+ dataArray[0][1];
            //remove existing data from results container and replace with new results
            $('#data').children('.id'+name).find('table, p, a').remove();
						//if the new data contains an error
						if (dataArray[2].length < 2) {
							//and the previous tab was not an error
							var errorTab =  $('#tabBar').find(".id"+name).children('.error');
							if (errorTab.length < 1) {
								$('#tabBar').find(".id"+name).find("#tabName").remove();
								$('#tabBar').find(".id"+name).append('<div id="tabName" class="error">Error</div>');
							}
							var paragraph = $('#data').find(".id"+name);
							$(paragraph).append('<p class="error">'+dataArray[2][0]+'</p>');
						}
						//if new data is not an error
						else {
							dataArray.splice(0,1);
							var paragraph = $('#data').find('#dataResult.id'+name)
							//but the last data was an error
							var errorTab =  $('#tabBar').find(".id"+name).children('.error')
							if (errorTab.length > 0) {
								$('#tabBar').find(".id"+name).find(".error").remove()
								$('#tabBar').find(".id"+name).append('<div id="tabName">'+tabName+'</div>');
							}
							$(paragraph).find("h3").append('<p id="recordCount"> ('+(dataArray.length-1)+' transaction records)</p>');
							$(paragraph).append('<a href="http://wildfire.codercollective.org/testcampaignfinance/download.cgi?'+formData+'&download=True'+'">Download Data</a>');
							d3.select('#data .id'+name)
							.append('table')
            	.selectAll('tr')
            	.data(dataArray)
            	.enter().append('tr')
            	.selectAll('td')
            	.data(function(d){return d;})
            	.enter().append("td")
            	.text(function(d) {return d;})
						}
					}	
        },
        //remove working animation, hide all tabs, show first tab and first data result
        complete: function() {
          $('#refine').find('#working').removeClass('show').addClass('hide');
          $('#results').find('#data').children().addClass('hide');
          $('#results').find('#dataResult').removeClass('hide').addClass('show');
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
    //remove the show class where it exists and add hide
    $('#results').find('#data').children('.show').removeClass('show').addClass('hide');
    //remove hide from the results with class matching tab data and add show
    $('#data').find(".id"+committeeData["id"]).removeClass('hide').addClass('show');
  });
  //on clicking the close image in the tab
  $('#tabBar').on('click', 'img',  function () {
    //grab data from parent tab container, check to see if parent is highlighted
    var committeeData = $(this).closest('#tab').data();
    var committeeTab = $(this).parent('.highlight');
    //if parent is not highlighted, remove tab and corresponding results container
    if (committeeTab.length < 1) {
      $(this).closest('#tab').remove();
      $('#data').find(".id"+committeeData["id"]).remove();
    }
    //if the tab container is highlighted
    else {
      //remove tab and corresponding data result, highligh first tab and show first data result
      $(this).closest('#tab').remove();
      $('#data').find(".id"+committeeData["id"]).remove();
      $('#data').find('#dataResult').removeClass('hide').addClass('show');
      $('#tabBar').find("#tab").addClass('highlight');
    }
  });  
	//on click, minimize search
	$('#search').find('#min').on('click', 'img', function() {
		type = $(this).data();
		if (type['type'] === 'min') {
			$(this).parent().append('<img class="min" data-type="max" src="arrow-right-2.png">');
			$(this).closest('#search').children('#committeeForm, #refine').removeClass('show').addClass('hide');
			$(this).closest('#search').removeClass('searchMax').addClass('searchMin');
			$('#results').removeClass('resultsMin').addClass('resultsMax');
			$(this).remove();
		}
		else {
			$(this).parent().append('<img class="min" data-type="min" src="arrow-left-2.png">');
			$(this).closest('#search').children('#committeeForm, #refine').removeClass('hide').addClass('show');
			$(this).closest('#search').removeClass('searchMin').addClass('searchMax');
			$('#results').removeClass('resultsMax').addClass('resultsMin');
			$(this).remove();
		}
	});

	//sort
//	$('#results').find('table').find('thead').find('.sort').find('#center').on('click', '#sortUp', function () {
	//	var resultTable = tabulate(
//	});

});
