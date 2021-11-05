function handle_color(card){
	card.style.backgroundColor='#323739';
	var convo_cards =document.getElementsByClassName('convo-card')
	var i;
	for (i = 0; i < convo_cards.length; i++) {
		if (convo_cards[i] != card){
			convo_cards[i].style.backgroundColor='#131c21';
		}
	}
}

function hide_convos() {
	document.getElementById('convos-col').classList.toggle('visible')
	var header =document.getElementsByClassName('header-convo')[0]
	if (header.classList.contains('hide-header')){
		header.classList.toggle('hide-header')
	}

}
function alter_side() {
	document.getElementById('convos-col').classList.toggle('visible')
	document.getElementsByClassName('header-convo')[0].classList.toggle('hide-header')
	document.getElementsByClassName('convo-col')[0].classList.toggle('hide-body')
}