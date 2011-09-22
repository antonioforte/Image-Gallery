

var LibCommon = new Object();
LibCommon.init = function(){
    dom_addDocumentTitleDiv();
    
    /* Create navs*/
    var wrapper = document.getElementById('pageWrapper');
    if (wrapper != null){
        // Create letters nav
        if (wrapper.getAttribute('data-mode') == 'gallery_items') {
            navletters.init('pageWrapper',16);
        }
        // Create numbers nav
        if (wrapper.getAttribute('data-mode') == 'gallery_items_items') {
            navn.init('pageWrapper',17);
        }

    }
}


LibCommon.currentImage = 0;
LibCommon.urls;
LibCommon.duration = 2;
LibCommon.interval;
LibCommon.resizedInfo;

LibCommon.launchIndividualImage = function(chosenUrl){
	// this is the event launched by a click on thumb
	// get a list of big pics and filenames
	var wrapper = document.getElementById('pageWrapper');
	var goback = document.getElementById('goback');
	var docdiv = document.getElementById('docDiv');
        var buttonsdiv = document.getElementById('buttonsdiv');
	var gobackLink = document.getElementById('gobackLink').getAttribute('onClick');
	
	var urls = LibCommon.getPicsUrls(wrapper);
	LibCommon.urls = urls;
	LibCommon.currentImage = urls[0].indexOf(chosenUrl);
	
        if (buttonsdiv != null){
            document.body.removeChild(buttonsdiv);
        }
	document.body.removeChild(wrapper);
	document.body.removeChild(goback);
	document.body.removeChild(docdiv);
	
	LibCommon.createBigPicDiv();
	LibCommon.insertImage();
	LibCommon.addControlerEvents(chosenUrl,gobackLink);
}


LibCommon.insertImage = function (){
	var bigpicdiv = document.getElementById('bigpicdiv');
	dom_deleteAllChildNodes(bigpicdiv);

	var bigpic = document.createElement('img');
        bigpic.style.display = 'none';
	var curImageUrl = LibCommon.urls[0][LibCommon.currentImage];
	bigpic.onload = function() {
            LibCommon.resizeImage(bigpic);
            bigpic.style.display = 'inline';
            dom_addEventListener(bigpic,"mouseup",LibCommon.resizeImageOnClickEvt); 
            LibCommon.setText();
	}
	bigpicdiv.appendChild(bigpic);
	bigpic.setAttribute('src','file://'+curImageUrl);
}




LibCommon.play = function(e){
    var text = dom_getEventObj(e).textContent;
    switch (text) {
    case "play":
    	dom_getEventObj(e).textContent = 'stop';
    	LibCommon.interval = window.setInterval("LibCommon.playSanitize()",LibCommon.duration*1000);
        break;
    case "stop":
    	dom_getEventObj(e).textContent = 'play';
        clearInterval(LibCommon.interval);
        break;
    default:
        alert("Text is wierd");
    }
}

LibCommon.playSanitize = function (){
	if (LibCommon.currentImage == LibCommon.urls[0].length){
		LibCommon.currentImage = 0;
	}
	LibCommon.insertImage();
	LibCommon.currentImage++;
}


LibCommon.first = function (){
	LibCommon.currentImage = 0;
	LibCommon.insertImage();
}
LibCommon.previous = function (){
	LibCommon.currentImage--;
	if (LibCommon.currentImage < 0){
		LibCommon.currentImage = LibCommon.urls[0].length-1;
	}
	LibCommon.insertImage();
}
LibCommon.next = function (){
	LibCommon.currentImage++;
	if (LibCommon.currentImage == LibCommon.urls[0].length){
		LibCommon.currentImage = 0;
	}
	LibCommon.insertImage();
}
LibCommon.last = function (){
	LibCommon.currentImage = LibCommon.urls[0].length -1;
	LibCommon.insertImage();
}









LibCommon.resizeImageOnClickEvt = function (e){
	var pic = dom_getEventObj(e);
	var orW = pic.getAttribute('data-widthOr');
	var orH = pic.getAttribute('data-heightOr');
	
    var picWidth = pic.width;
    var picHeight = pic.height;

    // if pic is not displayed with original dimensions
    // resize image to original
    if (picWidth != orW && picHeight != orH) {
        pic.width = orW;
        pic.height = orH;    
    }
    // if pic is displayed with original dimensions
    // resize it to fit the screen
    if (picWidth == orW && picHeight == orH){
    	LibCommon.resizeImage(pic);
    }
}



LibCommon.setText = function (){
    var info = document.getElementById('info');
    dom_deleteAllChildNodes(info);
    
    var div = document.createElement("div");
    div.textContent = LibCommon.currentImage+' of '+LibCommon.urls[0].length; 
    info.appendChild(div);
    
    for ( var i = 0; i < LibCommon.resizedInfo.length; i++) {
        var div = document.createElement("div");
        div.textContent = LibCommon.resizedInfo[i];
        info.appendChild(div);
    }
}

LibCommon.createBigPicDiv = function(){
	var picdiv = document.createElement('div');
	picdiv.setAttribute('id','bigpicdiv'); 
	document.body.appendChild(picdiv);
}


LibCommon.resizeImage = function(img) {
    var browserDims = dom_getBrowserWindow();
    var hBorder = 150;
    var vBorder = 150;
    var browserW = Math.round(browserDims[0] - hBorder);
    var browserH = Math.round(browserDims[1] - vBorder);
    
    var picW = img.width;
    var picH = img.height;
    img.setAttribute('data-widthOr',picW);
    img.setAttribute('data-heightOr',picH);
    
    LibCommon.resizedInfo = [LibCommon.urls[1][LibCommon.currentImage]];
    LibCommon.resizedInfo.push('no - '+ img.width+' x '+img.height);
    LibCommon.resizedInfo.push('screen : '+(browserW+hBorder)+' x '+(browserH+vBorder));
    
    if (picW > browserW || picH > browserH){
        if (picW > picH) {
            var newWidth = browserW;
            var newHeight = picH * newWidth / picW;
            img.width = newWidth;
            img.height = Math.round(newHeight);
        } else if (picH > picW) {
            var newHeight = browserH;
            var newWidth = picW * newHeight / picH;
            img.width = Math.round(newWidth);
            img.height = newHeight;
        }
        LibCommon.resizedInfo = [LibCommon.urls[1][LibCommon.currentImage]];
        LibCommon.resizedInfo.push('yes - '+img.width+' x '+img.height+' - '+picW+' x '+picH);
        LibCommon.resizedInfo.push('screen : '+(browserW+hBorder)+' x '+(browserH+vBorder));
    }
}




LibCommon.addControlerEvents = function(chosenUrl,gobackLink){
	var controler = document.createElement("div"); 
	controler.setAttribute('id','controler');
	
    var first = document.createElement("button"); 
    first.textContent = 'first';
    var previous = document.createElement("button"); 
    previous.textContent = 'prev';
    var play = document.createElement("button"); 
    play.textContent = 'play';
    var next = document.createElement("button"); 
    next.textContent = 'next';
    var last = document.createElement("button"); 
    last.textContent = 'last';
    
    var exit = document.createElement("button"); 
    exit.setAttribute('onClick',gobackLink);
    exit.textContent = 'exit';
    
    var info = document.createElement("div"); 
    info.setAttribute('id','info');
    
	controler.appendChild(first);
	controler.appendChild(previous);
	controler.appendChild(play);
	controler.appendChild(next);
	controler.appendChild(last);
	controler.appendChild(exit);
	controler.appendChild(info);
    document.body.appendChild(controler);
	
	dom_addEventListener(first,"mouseup",LibCommon.first); 
	dom_addEventListener(previous,"mouseup",LibCommon.previous); 
	dom_addEventListener(play,"mouseup",LibCommon.play); 
	dom_addEventListener(next,"mouseup",LibCommon.next); 
	dom_addEventListener(last,"mouseup",LibCommon.last); 	
}



LibCommon.getPicsUrls = function (wrapper){
	var divs = wrapper.getElementsByTagName('div');
	var urls = [[],[]];
	
	for ( var i = 0; i < divs.length; i++) {
		var bigurl = divs[i].getAttribute('data-big_pic_url');
		var filename = divs[i].getAttribute('data-filename');
		urls[0].push(bigurl);
		urls[1].push(filename);
	}
	return urls;
}









//Let the games begin
dom_onDomReady(LibCommon.init);


//end