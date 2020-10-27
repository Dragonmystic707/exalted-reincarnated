(function(document) {
  const content = document.querySelector('.page');
  var activeSidebarItem = document.querySelector('.sidebar-bottom');

  scrollnav.init(content, { 
    debug: false,
    insertTarget: activeSidebarItem,
    sections: 'h1',
    subSections: 'h2'
  });
})(document);


