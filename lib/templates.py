

class templates:
    
    def Page(self,curdir,title):
        string = '''<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<link href="file://'''+curdir+'''/style.css" rel="stylesheet" type="text/css" />
<script type="text/javascript" src="file://''' + curdir + '''/js/dom_helper.js"></script>
<script type="text/javascript" src="file://''' + curdir + '''/js/navletters.js"></script>
<script type="text/javascript" src="file://''' + curdir + '''/js/common.js"></script>
<title>'''+title+'''</title>
</head>
<body>

<div id="goback">
    <a href="file://'''+curdir+'''/index.html">Home</a>
</div>

<div id="pageWrapper" class="wrapper" data-mode="gallery_items">_contents_</div>

</body>
</html>'''

        return string
    
    def PageFiles(self,curdir,title):
        string = '''<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<link href="file://'''+curdir+'''/style.css" rel="stylesheet" type="text/css" />
<script type="text/javascript" src="file://''' + curdir + '''/js/dom_helper.js"></script>
<script type="text/javascript" src="file://''' + curdir + '''/js/navnumbers.js"></script>
<script type="text/javascript" src="file://''' + curdir + '''/js/common.js"></script>
<title>'''+title+'''</title>
</head>
<body>

<div id="goback">
    <a href="file://'''+curdir+'''/index.html">Home</a>
    _back_
</div>

<div id="pageWrapper" class="wrapper" data-mode="gallery_items_items">_contents_</div>

</body>
</html>'''

        return string
    
    
    def PageLoading(self,curdir,title,text):
        string = '''<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<link href="file://'''+curdir+'''/style.css" rel="stylesheet" type="text/css" />
<script type="text/javascript" src="file://''' + curdir + '''/js/dom_helper.js"></script>
<script type="text/javascript" src="file://''' + curdir + '''/js/common.js"></script>
<title>Gallery Page Loading</title>
</head>
<body>

<div id="goback">
    <a href="file://'''+curdir+'''/index.html">Home</a>
</div>

<div id="pageLoading">'''+text+'''</div>

</body>
</html>'''

        return string
    