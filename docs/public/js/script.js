(function(document) {
  const content = document.querySelector('.page');
  var activeSidebarItem = document.querySelector('.sidebar-split');

  scrollnav.init(content, { 
    debug: false,
    insertTarget: activeSidebarItem,
    sections: 'h2',
    subSections: 'h3',
    insertLocation: 'after'
  });
})(document);


