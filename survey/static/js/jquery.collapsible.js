/**
 * Collapsible, jQuery Plugin
 * 
 * This plugin enables the management of 
 * collapsibles on the page with cookie support.
 * 
 * Copyright (c) 2010 John Snyder (snyderplace.com)
 * @license http://www.snyderplace.com/collapsible/license.txt New BSD
 * @version 1.1
 */
(function($) {
	$.fn.collapsible = function (cmd, arg) {
		//firewalling
		if (!this || this.length < 1) {
			return this;
		}

		//address command requests
		if (typeof cmd == 'string') {
			return $.fn.collapsible.dispatcher[cmd](this, arg);
		}
		
		//return the command dispatcher
		return $.fn.collapsible.dispatcher['_create'](this, cmd);
	};

	//create the command dispatcher
	$.fn.collapsible.dispatcher = {		
		//initialized with options
		_create : function(obj, arg) {
			createCollapsible(obj, arg);
		},
		//toggle the element's display
		toggle: function(obj) {
			toggle(obj, loadOpts(obj));
			return obj;
		},
		//show the element
		open: function(obj) {
			open(obj, loadOpts(obj));
			return obj;
		},
		//hide the element
		close: function(obj) {
			close(obj, loadOpts(obj));
			return obj;
		},
		//check if the element is closed
		collapsed: function(obj) {
			return collapsed(obj, loadOpts(obj));
		}
	};

	//create the initial collapsible
	function createCollapsible(obj, options) {
		//build main options before element iteration
		var opts = $.extend({}, $.fn.collapsible.defaults, options);
		
		//store any opened default values to set cookie later
		var opened = new Array();
		
		//iterate each matched object, bind, and open/close
		obj.each(function() {
			var $this = $(this);
			saveOpts($this, opts);
			
			//bind it to the event
			if (opts.bind == 'mouseenter') {
				$this.bind('mouseenter', function(e) {
					e.preventDefault(); 
					toggle($this, opts);
				});
			}
			
			//bind it to the event
			if (opts.bind == 'mouseover') {
				$this.bind('mouseover',function(e) {
					e.preventDefault(); 
					toggle($this, opts); 
				});
			}
			
			//bind it to the event
			if (opts.bind == 'click') {
				$this.bind('click', function(e) {
					e.preventDefault();
					toggle($this, opts);
				});
			}
			
			//bind it to the event
			if (opts.bind == 'dblclick') {
				$this.bind('dblclick', function(e) {
					e.preventDefault();
					toggle($this, opts);
				});
			}
			
			//initialize the collapsibles
			//get the id for this element
			id = $this.attr('id');
			
			//if not using cookies, open defauls
			if (!useCookies(opts)) {
				//is this collapsible in the default open array?
				dOpenIndex = inDefaultOpen(id, opts);
				
				//close it if not defaulted to open
				if (dOpenIndex === false) {
					$this.addClass(opts.cssClose);
					$this.next().hide(); 
				} else { //its a default open, open it
					$this.addClass(opts.cssOpen);
					$this.next().show();
					opened.push(id);
				}
			} else { //can use cookies, use them now
				//has a cookie been set, this overrides default open
				if (issetCookie(opts)) {
					cookieIndex = inCookie(id, opts);
					if (cookieIndex === false) { 
						$this.addClass(opts.cssClose);
						$this.next().hide();
					} else {
						$this.addClass(opts.cssOpen);
						$this.next().show();
						opened.push(id);
					}
				} else { //a cookie hasn't been set open defaults, add them to opened array
					dOpenIndex = inDefaultOpen(id, opts);
					if (dOpenIndex === false) {
						$this.addClass(opts.cssClose);
						$this.next().hide();
					} else {
						$this.addClass(opts.cssOpen);
						$this.next().show();
						opened.push(id);
					}
				}
			}
		});
		
		//now that the loop is done, set the cookie
		if (opened.length > 0 && useCookies(opts)) {
			setCookie(opened.toString(), opts);
		} else { //there are none open, set cookie
			setCookie('', opts);
		}
		
		return obj;
	};
	
	//load opts from object
	function loadOpts($this) {
		return $this.data('collapsible-opts');
	}
	
	//save opts into object
	function saveOpts($this, opts) {
		return $this.data('collapsible-opts', opts);
	}
	
	//returns true if object is opened
	function collapsed($this, opts) {
		return $this.hasClass(opts.cssClose);
	}
	
	//hides a collapsible
	function close($this, opts) {
		//give the proper class to the linked element
		$this.addClass(opts.cssClose).removeClass(opts.cssOpen);
		
		//close the element
		opts.animateOpen($this, opts);
		
		//do cookies if plugin available
		if (useCookies(opts)) {
			// split the cookieOpen string by ","
			id = $this.attr('id');
			unsetCookieId(id, opts);
		}
	}
	
	//opens a collapsible
	function open($this, opts) {
		//give the proper class to the linked element
		$this.removeClass(opts.cssClose).addClass(opts.cssOpen);
		
		//open the element
		opts.animateClose($this, opts);
		
		//do cookies if plugin available
		if (useCookies(opts)) {
			// split the cookieOpen string by ","
			id = $this.attr('id');
			appendCookie(id, opts);
		}
	}
	
	//toggle a collapsible on an event
	function toggle($this, opts) {
		if (collapsed($this, opts)) {
			//open a closed element
			open($this, opts);
		} else {
			//close an open element
			close($this, opts);
		}
		
		return false;
	}
	
	//use cookies?
	function useCookies(opts) {
		//return false if cookie plugin not present or if a cookie name is not provided
		if (!$.cookie || opts.cookieName == '') {
			return false;
		}
		
		//we can use cookies
		return true;
	}
	
	//append a collapsible to the cookie
	function appendCookie(value, opts) {
		//check if cookie plugin available and cookiename is set
		if (!useCookies(opts)) {
			return false;
		}
		
		//does a cookie already exist
		if (!issetCookie(opts)) { 
			//no lets set one
			setCookie(value, opts);
			return true;
		}
		
		//cookie already exists, is this collapsible already set?
		if (inCookie(value, opts)) { //yes, quit here
			return true;
		}
		
		//get the cookie
		cookie = $.cookie(opts.cookieName);
		
		//unescape it
		cookie = unescape(cookie);
		
		//turn it into an array
		cookieArray = cookie.split(',');
		
		//add it to list
		cookieArray.push(value);
		
		//save it
		setCookie(cookieArray.toString(), opts);
		
		return true;	
	}
	
	//unset a collapsible from the cookie
	function unsetCookieId(value, opts)
	{
		//check if cookie plugin available and cookiename is set
		if (!useCookies(opts)) {
			return false;
		}
		
		//if its not there we don't need to remove from it
		if (!issetCookie(opts)) { //quit here, don't have a cookie 
			return true;
		}
		
		//we have a cookie, is this collapsible in it
		cookieIndex = inCookie(value, opts);
		if (cookieIndex === false) { //not in the cookie quit here
			return true;
		}
		
		//still here get the cookie
		cookie = $.cookie(opts.cookieName);
		
		//unescape it
		cookie = unescape(cookie);
		
		//turn it into an array
		cookieArray = cookie.split(',');
		
		//lets pop it out of the array
		cookieArray.splice(cookieIndex, 1);
		
		setCookie(cookieArray.toString(), opts);
	}
	
	//set a cookie
	function setCookie(value, opts)
	{
		//can use the cookie plugin
		if (!useCookies(opts)) { //no, quit here
			return false;
		}
		
		//cookie plugin is available, lets set the cookie
		$.cookie(opts.cookieName, value, opts.cookieOptions);
	}
	
	//check if a collapsible is in the cookie
	function inCookie(value, opts)
	{
		//can use the cookie plugin
		if (!useCookies(opts)) {
			return false;
		}
		
		//if its not there we don't need to remove from it
		if (!issetCookie(opts)) { //quit here, don't have a cookie 
			return false;
		}
		
		//unescape it
		cookie = unescape($.cookie(opts.cookieName));
		
		//turn it into an array
		cookieArray = cookie.split(',');
		
		//get the index of the collapsible if in the cookie array
		cookieIndex = $.inArray(value, cookieArray);
		
		//is this value in the cookie arrray
		if (cookieIndex == -1) { //no, quit here
			return false;
		}
		
		return cookieIndex;
	}
	
	//check if a cookie is set
	function issetCookie(opts)
	{
		//can we use the cookie plugin
		if (!useCookies(opts)) { //no, quit here
			return false;
		}
		
		//is the cookie set
		if ($.cookie(opts.cookieName) == null) { //no, quit here
			return false;
		}
		
		return true;
	}
	
	//check if a collapsible is in the list of collapsibles to be opened by default
	function inDefaultOpen(id, opts)
	{
		//get the array of open collapsibles
		defaultOpen = getDefaultOpen(opts);
		
		//is it in the default open array
		index = $.inArray(id, defaultOpen);
		if (index == -1) { //nope, quit here
			return false;
		}
		
		return index;
	}
	
	//get the default open collapsibles and return array
	function getDefaultOpen(opts)
	{
		//initialize an empty array
		defaultOpen = new Array();
		
		//if there is a list, lets split it into an array
		if (opts.defaultOpen != '') {
			defaultOpen = opts.defaultOpen.split(',');
		}
		
		return defaultOpen;
	}
	
	// settings
	$.fn.collapsible.defaults = {
		cssClose: 'collapse-close', //class you want to assign to a closed collapsible header
		cssOpen: 'collapse-open', //class you want to assign an opened collapsible header
		cookieName: 'collapsible', //name of the cookie you want to set for this collapsible
		cookieOptions: { //cookie options, see cookie plugin for details
			path: '/',
			expires: 7,
			domain: '',
			secure: ''
		},
		defaultOpen: '', //comma seperated list of header ids that you want opened by default
		speed: 'slow', //speed of the slide effect
		bind: 'click', //event to bind to, supports click, dblclick, mouseover and mouseenter
		animateOpen: function (elem, opts) { //replace the standard slideUp with custom function
			elem.next().slideUp(opts.speed);
		},
		animateClose: function (elem, opts) { //replace the standard slideDown with custom function
			elem.next().slideDown(opts.speed);
		}
	};
})(jQuery);