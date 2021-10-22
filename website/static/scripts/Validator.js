function get_filename(file){
	var label= document.getElementById('file-label')
	label.style.marginTop='-45'
	label.innerHTML=file.value.split('\\').pop()
}
function validate_form(){
	var file = document.getElementById('txt-file')
	if (file.value !=''){
		document.getElementById('submit-btn').value='PROCESSING'
		return true
	}
	else{
		file.click()
		return false
	}
}