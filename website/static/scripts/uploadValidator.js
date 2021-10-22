function get_filename(file){
	var label= document.getElementById('file-label')
	label.innerHTML=file.value.split('\\').pop()
}
function validate_form(){
	var file = document.getElementById('txt-file')
	if (file.value !=''){
		document.getElementById('submit-btn').value='processing'
		return true
	}
	else{
		file.click()
		return false
	}
}