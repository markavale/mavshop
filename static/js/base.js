// navbar effects
var prevScrollpos = window.pageYOffset;
window.onscroll = function() {
var currentScrollPos = window.pageYOffset;
  if (prevScrollpos > currentScrollPos) {
    document.getElementById("navbar").style.top = "0";
  } else {
    document.getElementById("navbar").style.top = "-75px";
  }
  prevScrollpos = currentScrollPos;
}

// shopping cart hover effects
// (function(){
  
//   $('.shopping-cart').each(function() {
//     var delay = $(this).index() * 50 + 'ms';
//     $(this).css({
//         '-webkit-transition-delay': delay,
//         '-moz-transition-delay': delay,
//         '-o-transition-delay': delay,
//         'transition-delay': delay
//     });
//   });
//   $('#cart, .shopping-cart').hover(function(e) {
//     $(".shopping-cart").stop(true, true).addClass("active");
//   }, function() {
//     $(".shopping-cart").stop(true, true).removeClass("active");
//   });  
// })();