var msgs =document.getElementsByClassName('msg');
function align(){
	var i;
	for (i = 0; i < msgs.length; i++) {
	  msgs[i].classList.toggle("right-align");
	}
}