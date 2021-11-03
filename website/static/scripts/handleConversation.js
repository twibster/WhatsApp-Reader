function delete_conversation(id,unique_id){
	$.getJSON('/delete_conversation?id='+id+'&u='+unique_id,
	      function(data){
	        if (data==1){
	        	reloadAsGet();
	        }
	    }
	);
}
function change_pov(id,unique_id){
	pov = displayRadioValue().replace('+','%2B')
	$.getJSON('/change_pov?id='+id+'&u='+unique_id+'&pov='+pov,
	      function(data){
	        if (data==1){
	        	reloadAsGet();
	        }
	    }
	);
}
function displayRadioValue() {
    var pov_radios = document.getElementsByName('pov');

    for(i = 0; i < pov_radios.length; i++) {
        if(pov_radios[i].checked){
        	return pov_radios[i].value
        }
    }
}
function reloadAsGet(){
    var loc = window.location;
    window.location = loc.protocol + '//' + loc.host + loc.pathname + loc.search;
}