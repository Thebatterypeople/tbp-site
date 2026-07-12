// The Battery People — shared site JS
document.addEventListener('DOMContentLoaded', function () {
  var btn = document.querySelector('.menu-btn');
  var nav = document.querySelector('.mobilenav');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      nav.classList.toggle('open');
    });
  }
});
