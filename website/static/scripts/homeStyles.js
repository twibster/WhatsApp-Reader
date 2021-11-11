media=document.getElementById('media-btn')
no_media=document.getElementById('no-media-btn')
function show_media() {
	media.style.background='#434748'
	no_media.style.background='transparent'
	document.getElementsByClassName('show-no-media')[0].classList.remove('visible')
	document.getElementsByClassName('show-media')[0].classList.add('visible')
}
function show_no_media(){
	media.style.background='transparent'
	no_media.style.background='#434748'
	document.getElementsByClassName('show-media')[0].classList.remove('visible')
	document.getElementsByClassName('show-no-media')[0].classList.add('visible')	
}