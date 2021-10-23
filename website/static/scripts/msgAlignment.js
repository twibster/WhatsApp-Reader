var msgs =document.getElementsByClassName('msg');
function align_right(btn){
	if (btn.innerText=='Left align'){
		btn.innerText='Right align'
	}
	else{
		btn.innerText='Left align'
	}	
	var i;
	for (i = 0; i < msgs.length; i++) {
	  msgs[i].classList.toggle("right-align");
	}
}