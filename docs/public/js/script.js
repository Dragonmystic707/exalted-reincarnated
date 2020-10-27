(function(document) {
  const content = document.querySelector('.page');

  scrollnav.init(content, { 
    debug: false,
    insertTarget: sidebar-nav-item.active
  });
})(document);


