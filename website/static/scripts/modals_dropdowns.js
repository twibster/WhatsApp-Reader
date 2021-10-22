var modal=document.getElementById('addModal')
var drop =document.getElementById('three-dot')
var pov_modal=document.getElementById('povModal')
var dropdown_div =document.getElementById('dropdown-div')
var p =document.getElementById('content')
// var sticky_elements =document.getElementsByClassName('sticky-msg')

function show_modal(){
  // var i;
  // for (i = 0; i < sticky_elements.length; i++) {
  //   sticky_elements[i].classList.remove("sticky-msg");
  // }
  p.innerHTML='This Feature is yet to come, stay tuned.'
  modal.classList.add('show');
}
function close_modal(){
  // var i;
  // for (i = 0; i < sticky_elements.length; i++) {
  //   sticky_elements[i].classList.add("sticky-msg");
  // }
  modal.classList.remove('show');
}
function show_dropdown(){
  drop.classList.add('show-drop')
}
function hide_dropdown(){
  drop.classList.remove('show-drop')
}
function show_pov(){
  pov_modal.classList.add('show')
}
function hide_pov(){
  pov_modal.classList.remove('show')
}
  
document.addEventListener("click", function(evt) {
  var opacity = window.getComputedStyle(drop).getPropertyValue("opacity");
  var targetElement = evt.target;
  do {
      if (targetElement == dropdown_div && opacity=='0') {
        show_dropdown();
        return;
       }  
      targetElement = targetElement.parentNode;
  } while (targetElement);
    hide_dropdown();
});
