document.addEventListener('DOMContentLoaded', function() {
  _.$('books-headline').addEventListener('click', function(e) {
    var menu = this.getElementsByClassName('menu')
    menu[0].classList.toggle('visible');
  }, false);

  _.$('bookshelf-about').addEventListener('click', function(e) {
    e.preventDefault();
    return false;
  }, false);

  /* Books filtering using AJAX
  _.$('books-filter').addEventListener('click', function(e) {
    if (e.target.tagName == 'A') {
      queryBooks(e.target.name);
    }
  }, false);

  function queryBooks(filter) {
    var httpRequest;
    makeRequest(filter);

    function makeRequest(filter) {
      if (window.XMLHttpRequest) {
        // IE7+, Firefox, Chrome, Safari, Opera
        httpRequest = new XMLHttpRequest();
      } else if (window.ActiveXObject) {
        // IE6 and older
        try {
          httpRequest = new ActiveXObject("Msxml2.XMLHTTP");
        } catch (e) {
          try {
            httpRequest = new ActiveXObject("Microsoft.XMLHTTP");
          } catch (e) {}
        }
      }
      if (!httpRequest) { return false; }
      httpRequest.onreadystatechange = processResponse;
      httpRequest.open('GET', $URL_ROOT + '/bookshelf/_query?filter=' + encodeURIComponent(filter));
      httpRequest.send();
    }

    function processResponse() {
      if (httpRequest.readyState === 4) {
        if (httpRequest.status === 200) {
          console.log(httpRequest.responseText);
          var response = JSON.parse(httpRequest.responseText);

          if (!response.error) {
            var selected = response.selected;
            var filters = response.filters;
            var books = response.books;
            var filterHTML = '';
            var bookHTML = '';

            _.$('filter-selected').innerHTML = selected;

            for (var i = 0; i < filters.length; i++) {
              filterHTML += '<li><a href="javascript:;" name="' + filters[i] +
                            '">' + filters[i] +' </a></li>\n';
            }
            _.$('books-filter').innerHTML = filterHTML;

            if (books.length > 0) {
              for (var j = 0; j < books.length; j++) {
                bookHTML += '<div class="book">\n<a href="' + books[j][2] +
                            '" rel="external" target="_blank">\n' +
                            '<img src="' + books[j][1] + '" alt="' + books[j][0] +
                            '" width="185" height="280"></a>\n</div>\n';
              }
            } else {
              bookHTML = '<div class="placeholder">\n' +
                         '<span class="fa fa-book fa-5x"></span>\n' +
                         '<p>No books have been added yet.</p>\n' +
                         '<p>(￣。￣)～ｚｚｚ&hellip;</p>\n</div>';
            }
            _.$('books-display').innerHTML = bookHTML;
          }
        } else {
          // Error
          _.$('books-display').innerHTML = '<div class="placeholder">\n' +
            '<span class="fa fa-book fa-5x"></span>\n' +
            '<p>My bookshelf is unavailable at the moment.</p>\n' +
            '<p>(◕﹏◕✿) &hellip;  (╯︵╰,) &hellip; (✖﹏✖) &hellip;</p>\n</div>';
        }
      }
    }
  }
  */

}, false);
