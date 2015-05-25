document.addEventListener('DOMContentLoaded', function() {
 _.$('show-course').addEventListener('click', function(e) {
    _.$('course-list').classList.remove('hidden');
    _.$('hide-course').classList.remove('hidden');
    this.classList.add('hidden');
 }, false);

 _.$('hide-course').addEventListener('click', function(e) {
    _.$('course-list').classList.add('hidden');
    _.$('show-course').classList.remove('hidden');
    this.classList.add('hidden');
 }, false);

}, false);
