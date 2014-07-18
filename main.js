function queryBy(showSection) {
	this.showQueryBy = function() {
		$('#refine').find('form').trigger('reset');
			$('#race, #candidate, #committee, #submitSearch, #individual').hide()
			$(showSection).slideDown('fast')
	}
}

$(document).ready(function() {

	//show individual search as default
	var start = new queryBy('#individual');
	start.showQueryBy();

	//slide down search options on selection
	$("#entity").on('change', '.entityVal', function() {
		var entitySelection = $('.entityVal').val()
		if (entitySelection == 'individual') {
			var selection = new queryBy('#individual');
			selection.showQueryBy();
		}
		else {
			var selection = new queryBy('#'+entitySelection+', #submitSearch');
			selection.showQueryBy();
		}
	});

	//ajax call for committees
	$('#committeeForm').on('submit', 'form',  function(event) {
		event.preventDefault();
		var working = $('#committeeForm').find('#working')
		$.ajax('nameCGI.cgi', {
		type: 'POST',
		data: $(this).serialize(),
		dataType: 'json',
		success: function(result) {
			$('#refine').prepend('<p class="'+result[0].committeeID+'"><button type="button">Remove Result</button></p>')
			$.each(result, function(index, committee) {
				$('#refine').find('p').first().prepend('<input type="checkbox" name="committeeID" value="'+committee.committeeID+'">'+committee.committeeName+', '+committee.candidateName+', '+committee.cycle+'</br>');				
			});
		},
		//indicate activity
		beforeSend: function() {
			working.show();
		},
		complete: function() {
			working.hide();
		}
		});
	});

	//remove committee selections
	$('#dataSearch').on('click', 'button', function(event) {
		$(this).parent().remove();
	});

	//ajax call for transaction data
	$('#dataSearch').on('submit', 'form', function(event) {
		event.preventDefault();
		var working = $('#dataSearch').find('#working')
		var currentType = $('.entityVal').val()
		var formData = 'entityOneType='+currentType+'&'+$(this).serialize()+'&download='
		console.log(formData);
		$.ajax('cfCGI.cgi', {
		type: 'POST',
		data: formData,
		dataType: 'json',
		success: function(result) {
			console.log(result);
			var tabTemplate = "<li><a href='#{href}'>#{label}</a> <span class='ui-icon-close' role='presentation'><img src='close.png'></span></li>"
			var tabs = $("#tabs").tabs()
			//jquery-ui tabs
			$.each(result, function(index, committee) {
			var label = committee['committeeName'],
				id = "tabs-"+committee['committeeID'],
				li = $( tabTemplate.replace( /#\{href\}/g, "#" + id ).replace( /#\{label\}/g, label ) );
				if ($('#'+id).length) {
					$('#'+id).children().remove();
				}
				else {
					tabs.find( ".ui-tabs-nav" ).append(li);
					tabs.append( "<div id='" + id + "'></div>" );
					tabs.tabs( "refresh" );
				}
			//generate table
			d3.select('#'+id)
			.append('table')
			.selectAll('tr')
			.data(committee['transactions'])
			.enter().append('tr')
			.selectAll('td')
			.data(function(d){return d;})
			.enter().append("td")
			.text(function(d) {return d;});
			});
		},
		beforeSend: function() {
			working.show();
		},
		complete: function() {
			working.hide();
		}
		});
	});

	//remove tabs
	var tabs = $("#tabs").tabs()
	tabs.delegate( "span.ui-icon-close", "click", function() {
		var panelId = $( this ).closest( "li" ).remove().attr( "aria-controls" );
		$( "#" + panelId ).remove();
		tabs.tabs( "refresh" );
	});
	tabs.bind( "keyup", function( event ) {
		if ( event.altKey && event.keyCode === $.ui.keyCode.BACKSPACE ) {
			var panelId = tabs.find( ".ui-tabs-active" ).remove().attr( "aria-controls" );
			$( "#" + panelId ).remove();
			tabs.tabs( "refresh" );
		}
	});

	//minimize search
	$('#min').on('click', 'img', function() {
		type = $(this).data();
		if (type['type'] === 'min') {
			$('#min').append('<img class="min" data-type="max" src="arrow-right-2.png">');
			$('#committeeForm, #dataSearch').hide();
			$('#search').removeClass('searchMax').addClass('searchMin');
			$('#results').removeClass('resultsMin').addClass('resultsMax');
			$(this).remove();
		}
		else {
			$('#min').append('<img class="min" data-type="min" src="arrow-left-2.png">');
			$('#committeeForm, #dataSearch').show()
			$('#search').removeClass('searchMin').addClass('searchMax');
			$('#results').removeClass('resultsMax').addClass('resultsMin');
			$(this).remove();
		}
	});

});
