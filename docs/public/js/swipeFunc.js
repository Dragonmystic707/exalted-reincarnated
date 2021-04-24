var swipeFunc = {
	touches : {
		"touchstart": {"x":-1, "y":-1}, 
		"touchmove" : {"x":-1, "y":-1}, 
		"touchend"  : false,
		"direction" : "undetermined"
	},
	touchHandler: function(event) {
		var touch;
		var box = document.getElementsByClassName("sidebar-checkbox")
		if (typeof event !== 'undefined'){	
			event.preventDefault(); 
			if (typeof event.touches !== 'undefined') {
				touch = event.touches[0];
				switch (event.type) {
					case 'touchstart':
					case 'touchmove':
						swipeFunc.touches[event.type].x = touch.pageX;
						swipeFunc.touches[event.type].y = touch.pageY;
						break;
					case 'touchend':
						touches[event.type] = true;
						if (swipeFunc.touches.touchstart.x > -1 && swipeFunc.touches.touchmove.x > -1) {
							box.checked = swipeFunc.touches.touchstart.x > swipeFunc.touches.touchmove.x;
						}
					default:
						break;
				}
			}
		}
	},
	init: function() {
		document.addEventListener('touchstart', swipeFunc.touchHandler, false);	
		document.addEventListener('touchmove', swipeFunc.touchHandler, false);	
		document.addEventListener('touchend', swipeFunc.touchHandler, false);
	}
};
swipeFunc.init();