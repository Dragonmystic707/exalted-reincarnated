(function(document) {
  const content = document.querySelector('.page');
  var activeSidebarItem = document.querySelector('.sidebar-split');

  $('.page').scrollNav({
    debug: false,
    insertTarget: activeSidebarItem,
    sections: 'h1',
    subSections: 'h2',
    insertLocation: 'after'})

})(document);


