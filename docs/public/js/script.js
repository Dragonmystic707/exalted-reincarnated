(function(document) {
  var toggle = document.querySelector('.sidebar-toggle');
  var sidebar = document.querySelector('#sidebar');
  var checkbox = document.querySelector('#sidebar-checkbox');
  var container = document.querySelector('.container');

  document.addEventListener('click', function(e) {
    var target = e.target;

    // /* There's got to be a better way of doing this */
    // if(target === checkbox || target === toggle)
    // {
    //   if(checkbox.checked)
    //   {
    //     container.padding.right = '15rem';
    //   }
    //   else
    //   {
    //     container.padding.right = '1rem'; 
    //   }
      
    // }
  }, false);
})(document);
