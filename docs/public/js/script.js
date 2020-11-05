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

  var coll = document.getElementsByClassName("collapsible");
  var i;

  const checkHeight = function(obj, expanded) {
    if (expanded){
      obj.style.maxHeight = obj.scrollHeight + "px";
    } else {
      obj.style.maxHeight = null;    
    }
  }
  /* Temporarily disable the transition duration */
  

  for (i = 0; i < coll.length; i++) {
    checkHeight(coll[i].nextElementSibling, coll[i].classList.contains("active"));
    
    coll[i].addEventListener("click", function() {
      this.classList.toggle("active");
      var content = this.nextElementSibling;
      checkHeight(content, this.classList.contains("active"));
    });
  }
})(document);



