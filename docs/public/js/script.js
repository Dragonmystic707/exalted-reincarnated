(function(document) {
  const content = document.querySelector('.page');
  var activeSidebarItem = document.querySelector('.sidebar-nav-item active');

  scrollnav.init(content, { 
    debug: false,
    insertTarget: activeSidebarItem
  });
})(document);


