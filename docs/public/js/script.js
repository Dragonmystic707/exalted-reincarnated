(function(document) {
  const content = document.querySelector('.page');
  var activeSidebarItem = document.querySelector('.sidebar-split');

  $('.page').scrollNav({
    sections: 'h1',
    subSections: 'h2',
    insertTarget: activeSidebarItem,
    insertLocation: 'insertAfter'
  })

})(document);


