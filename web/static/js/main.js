// DOM utility function
var _ = {
  $: function (id) {
    return document.getElementById(id);
  }
};

document.addEventListener('DOMContentLoaded', function() {
  var menu = _.$('nav-menu-bar')
  var nav = _.$('site-nav');

  menu.addEventListener('click', function(e) {
    nav.classList.toggle('visible');
    menu.classList.toggle('color-menu-open');
  }, false);

}, false);
