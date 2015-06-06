document.addEventListener('DOMContentLoaded', function() {
  _.$('project-listing').addEventListener('click', function(e) {
    var el = getClosestParentWithId(e.target);

    if (el != null && el.id != 'project-listing') {
      var info = el.getElementsByClassName('info-box');
      var hideIcon = el.getElementsByClassName('fa-chevron-up');
      var showIcon = el.getElementsByClassName('fa-chevron-down');
      info[0].classList.toggle('hidden');
      hideIcon[0].classList.toggle('hidden');
      showIcon[0].classList.toggle('hidden');
    }
  }, false);

  _.$('project-all').addEventListener('click', function(e) {
    e.preventDefault();
    setActiveFilter(e.target);
    resetProjectFilters();
    return false;
  }, false);
  _.$('project-personal').addEventListener('click', function(e) {
    e.preventDefault();
    setActiveFilter(e.target);
    filterProjects('personal');
    return false;
  }, false);
  _.$('project-school').addEventListener('click', function(e) {
    e.preventDefault();
    setActiveFilter(e.target);
    filterProjects('school');
    return false;
  }, false);
_.$('project-work').addEventListener('click', function(e) {
    e.preventDefault();
    setActiveFilter(e.target);
    filterProjects('work');
    return false;
  }, false);


  function setActiveFilter(element) {
    var curActive = _.$('project-filter').getElementsByClassName('active');
    curActive[0].classList.remove('active');
    element.classList.add('active');
  }

  function resetProjectFilters() {
    var listings = _.$('project-listing').querySelectorAll('section.hidden');
    for (var i = 0; i < listings.length; i++) {
      listings[i].classList.remove('hidden');
    }
  }

  function filterProjects(category) {
    var listings = _.$('project-listing').getElementsByTagName('section');
    for (var i = 0; i < listings.length; i++) {
      var projectClass = listings[i].classList;
      if (projectClass.contains(category)) {
        projectClass.remove('hidden');
      } else {
        projectClass.add('hidden');
      }
    }
  }

  function getClosestParentWithId(element) {
    while (element.id == '') {
      element = element.parentNode;
      if (!element) {
        return null;
      } else if (element.classList.contains('nonclickable')) {
        return null;
      }
    }
    return element;
  }

}, false);
