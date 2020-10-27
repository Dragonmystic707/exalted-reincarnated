(function(document) {
  const content = document.querySelector('.page');

  scrollnav.init(content, { 
    debug: false,
    easingStyle: 'linear',
    sections: ($('.post-content > h1').length>0) ? 'h1' : 'h2',
    subSections: ($('.post-content > h1').length>0) ? 'h2' : 'h3'
  });
})(document);


