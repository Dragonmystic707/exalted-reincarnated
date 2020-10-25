(function(document) {
  var toggle = document.querySelector('.sidebar-toggle');
  var sidebar = document.querySelector('#sidebar');
  var checkbox = document.querySelector('#sidebar-checkbox');

  document.addEventListener('click', function(e) {
    var target = e.target;

    /* Just toggle the sidebar. Seriously */
    if(target === checkbox)
    {
      checkbox.checked = !checkbox.checked;
    }
    // if(!checkbox.checked ||
    //    sidebar.contains(target) ||
    //    (target === checkbox || target === toggle)) return;

    // checkbox.checked = false;
  }, false);
})(document);
