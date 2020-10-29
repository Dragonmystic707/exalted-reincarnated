(function(document) {
  const content = document.querySelector('.page');
  var activeSidebarItem = document.querySelector('.sidebar-sidebar-nav-item active');

  $('.page').scrollNav({
    sections: 'h1',
    subSections: 'h2',
    insertTarget: activeSidebarItem,
    insertLocation: 'insertAfter',
    headlineText: '',
    showTopLink: false,
  })

})(document);


