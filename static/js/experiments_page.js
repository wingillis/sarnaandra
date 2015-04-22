var add_file_filter = function() {
    var div_copy = $('#additionalDataTypes').clone();
    var add_div = $('#copyToHere')
    add_div.append(div_copy);
    dataTypeNumber++;
    add_div.find('#dtype0').attr('name', dtype_id + dataTypeNumber).attr('id', dtype_id + dataTypeNumber);
    add_div.find('#extension0').attr('name', extension_id + dataTypeNumber).attr('id', extension_id + dataTypeNumber);
    add_div.find('#addDataTypeFilter0').attr('id', 'addDataTypeFilter' + dataTypeNumber);
    add_div.find('#addDataTypeFilter' + dataTypeNumber).click(add_file_filter);

}


var dataTypeNumber = 0;

var add_another_data_type = $('#addDataTypeFilter' + dataTypeNumber);
var data_type_name = $('#dtype');

// refer to this variable when adding new inputs
var dtype_id = data_type_name.attr('id');


data_type_name.attr('id', dtype_id + dataTypeNumber);
data_type_name.attr('name', dtype_id + dataTypeNumber);


var extension_name = $('#extension');

// refer to this variable when adding new inputs
var extension_id = extension_name.attr('id');

extension_name.attr('id', extension_id + dataTypeNumber);
extension_name.attr('name', extension_id + dataTypeNumber);

// allows user to add more file types for experiment to track
add_another_data_type.click(add_file_filter);

