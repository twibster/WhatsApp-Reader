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