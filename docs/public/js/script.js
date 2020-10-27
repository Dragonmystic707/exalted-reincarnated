(function(document) {
  const content = document.querySelector('.page');
  var activeSidebarItem = document.querySelector('a.sidebar-nav-item' > 'a.active');

  scrollnav.init(content, { 
    debug: false,
    insertTarget: activeSidebarItem
  });
})(document);


