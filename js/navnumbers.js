

/*
<html>
<head>
<script type="text/javascript" src="js/navnumbers.js"></script>

<script>
    document.addEventListener("DOMContentLoaded", function(){
        navn.init('pageWrapper',4);
     }, false);
</script>
</head>
<body>

<div id="pageWrapper" class="wrapper" data-mode="gallery_items_items">
    <div>1</div>
    <div>2</div>
    <div>3</div>
    <div>4</div>
    <div>5</div>
    <div>6</div>
</div>

</body>
</html>
*/



var navn = new Object();
navn.wrapper = '';
navn.all = [];
navn.spaces = null;
navn.perpage = null;

navn.init = function(id,num){
    navn.wrapper = wrapper;
    navn.perpage = num;
    var wrapper = document.getElementById(id);
    var childs = wrapper.childNodes;
    
    for(var e = 0; e < childs.length; e++){
        navn.all.push(childs[e]);
    }
    
    if (navn.all.length > num){
        navn.spaces = Math.ceil(navn.all.length / num);
        navn.createButtons();
    }
}


navn.createButtons = function(){
    var num = navn.perpage;
    var buttonsdiv = document.createElement('div');
    buttonsdiv.id = 'buttonsdiv';
    
    var buttonall = document.createElement('button');
    buttonall.textContent = 'all';
    buttonall.addEventListener('mouseup',navn.sort,false);
    buttonsdiv.appendChild(buttonall);

    for(var e = 0; e < navn.spaces; e++){
        var button = document.createElement('button');
        var spacedivs = navn.all.slice(e*num,e*num+num);

        if (e == 0){
            button.textContent = e*num+' - '+num;
        }else if (e == navn.spaces-1){
            button.textContent = e*num+' - '+(e*num+spacedivs.length);
        }else{
            button.textContent = e*num+' - '+(spacedivs.length * e + num);
        }
        
        button.addEventListener('mouseup',navn.sort,false);
        buttonsdiv.appendChild(button);
    }
    document.body.insertBefore(buttonsdiv,navn.wrapper);
}


navn.sort = function(evt){
    var query = evt.srcElement.textContent;

    if (query != 'all'){
        var start = query.split(' - ')[0];
        var end = query.split(' - ')[1];
        var spacedivs = navn.all.slice(start,end);
        
        for(var e = 0; e < navn.all.length; e++){
            if (e >= start && e <= end){
                navn.all[e].style.display = 'block';
            }else{
                navn.all[e].style.display = 'none';
            }
        }
    }else{
        for(var i = 0; i < navn.all.length; i++){
            navn.all[i].style.display = 'block';
        }
    }  
}





/* end */