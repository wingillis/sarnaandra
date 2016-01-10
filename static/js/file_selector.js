var filepath_input = document.getElementById('fp');
var select_field = document.getElementById('file_select');
var fullpath = '';

var change_select_field = function(data) {
	fullpath = data.fullpath;
	var file_select = $('#file_select');
	var files_select = $('#files');
	var folders = data.paths;
	var files = data.files;
	file_select.text('');
	files_select.text('');
	$.each(folders, function(i, item){
		file_select.append(item + '\n');
	});
	$.each(files, function(i, item) {
		files_select.append(item + '\n');
	});
	if (data.first) {
		filepath_input.value = fullpath;
	}
};

filepath_input.addEventListener('input', function() {
	$.ajax({url:'/filepath',
		data: {path:filepath_input.value},
		success: change_select_field});
});

var update_select_field = function() {
		$.ajax({url:'/filepath',
		data: {path:filepath_input.value},
		success: change_select_field});
};

// $('#file_select').change(function() {
// 	var folder = $('#file_select option:selected').text();
// 	filepath_input.value = fullpath + '/' + folder;
// 	update_select_field();
// });

$.ajax({url:'/filepath',
		data: {path:'__base__'},
		success: change_select_field});
