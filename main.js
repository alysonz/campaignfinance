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
		},
		beforeSend: function() {
			working.show();
		},
		complete: function() {
			working.hide();
		}
		});
	});
});
