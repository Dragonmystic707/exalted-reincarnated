(function(document) {
  const content = document.querySelector('.page');
  var activeSidebarItem = document.querySelector('.sidebar-nav-chapter-item > a.active');

  // $('.page').scrollNav({
  //   sections: 'h1',
  //   subSections: 'h2',
  //   insertTarget: activeSidebarItem,
  //   insertLocation: 'insertAfter',
  //   headlineText: '',
  //   showTopLink: false,
  // })

  scrollnav.init(content, {
    insertTarget: activeSidebarItem,
    insertLocation: 'after'
  });

})(document);


