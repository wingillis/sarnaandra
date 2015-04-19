var add_another_data_type = $('#addDataTypeFilter');

add_another_data_type.click(function() {
	var div_copy = $('#additionalDataTypes').clone();
	$('#copyToHere').append(div_copy);
});