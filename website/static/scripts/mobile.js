var isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
	if (isMobile){
		var convos=document.getElementById('convos-col')
		convos.parentNode.removeChild(convos);
	}