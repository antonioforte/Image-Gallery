#!/usr/bin/env python
from xml.etree import ElementTree as ET
import threading
import sqlite3
import sys
import os
import time

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import QtWebKit
from PyQt4 import QtNetwork

import lib.common
import lib.templates
import lib.gallery_image
import lib.myconfig



class thread_EditDB(QtCore.QThread):
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.exiting = False
        self.start()

    def __del__(self):
        self.exiting = True

    def setValues(self,str):
        self.lib = lib.common.common()
        self.curdir = os.path.dirname(sys.argv[0])
        self.configXml = self.lib.getXml(os.path.join(self.curdir,'config.xml'))
        self.operation = str
        
    def run(self):
        if self.operation == 'createDB':
            self.buildDBs()




    def buildDBs(self):
        db2create = os.path.join(self.curdir,'res','data.db')
        rootDir = self.configXml.find('location').text
        avoid = self.configXml.find('avoid').text.split(',')
        thumbsSize = self.configXml.find('thumbs').text.split(',')
        exts = self.configXml.find('exts').text.split(',')
              
        self.lib.deleteFile(db2create)
        conn = sqlite3.connect(db2create)
        c = conn.cursor()
        
        c.execute('''CREATE TABLE all_pics 
        (full_url text,
        gallery text,
        galleryItem text,
        dimW text,
        dimH text, 
        hasExif text, 
        fileSize text, 
        fileDate text,
        hasDesc text,
        filename text,
        filename_head int
        ) ''')

        picsFolder = os.path.join(rootDir,'pics')
        if os.path.exists(picsFolder):
            # check how many files there are
            lenFiles = str(len(self.lib.walkDir(picsFolder,exts)))
            filesFound = 0
            
            # /media/vault_big/Gallery/pics
            for gal in os.listdir(unicode(picsFolder)):
                if gal not in avoid:
                    
                    # /media/vault_big/Gallery/pics/Gallery_Animals
                    galDir = os.path.join(picsFolder,gal)
                    for galItem in os.listdir(unicode(galDir)):
                        
                        # /media/vault_big/Gallery/pics/Gallery_Animals/lion
                        galItemDir = os.path.join(picsFolder,gal,galItem)
                        for file in os.listdir(unicode(galItemDir)):
                            full_url = os.path.join(galItemDir,file)
                            url, ext = os.path.splitext(full_url)
                            dest = os.path.join(rootDir,'thumbs',gal,galItem,file)
                            hasDesc = 'no'

                            if file == 'desc.txt':
                                hasDesc = 'yes'
                                
                            # if it is an image
                            if ext in exts:
                                # get info from image
                                info = self.lib.getPicDetails(full_url)
                                dimW = info[0]
                                dimH = info[1]
                                hasExif = info[2] 
                                fileSize = self.lib.getFileSize(full_url)
                                fileDate = self.lib.getFileDate(full_url)
                                filename_head = file.split('.')[0]
                                print('Reading file : ',full_url)
                                
                                # insert in db
                                t = [full_url,gal,galItem,dimW,dimH,hasExif,fileSize,fileDate,hasDesc,file,filename_head]
                                c.execute('insert into all_pics values (?,?,?,?,?,?,?,?,?,?,?)', t)
                                
                                # create thumb
                                if not os.path.exists(dest):
                                    self.lib.createImgThumbFit(full_url,dest,thumbsSize)
                                    print('Creating thumb : ',dest)
                                    
                            # if it is an image
                            if ext in exts:
                                # send string message to Main , about progress made
                                filesFound += 1
                                self.emit(QtCore.SIGNAL("postResultsThread_EditDB(QString,QString)"),lenFiles,str(filesFound))
                                
        conn.commit()
        print ('Done building database')
        

        
        


class EditDBClass(QtCore.QObject):
    
    @QtCore.pyqtSlot(str)
    def go(self,str):
        print ('EditDBClass.go')
        self.thread = thread_EditDB()
        self.thread.setValues(str)
        self.connect(self.thread, QtCore.SIGNAL("postResultsThread_EditDB(QString,QString)"), self.update)
        
    def update(self,nAll,nCur):
        self.emit(QtCore.SIGNAL("postResultsThread_EditDB_caller(QString,QString)"),nAll,nCur)
        
        

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.lib = lib.common.common() 
        self.templates = lib.templates.templates()
        self.curdir = self.getMainDir()
        self.configXml = self.lib.getXml(os.path.join(self.curdir, 'config.xml'))
        
        self.Image_Gallery = lib.gallery_image.Image_Gallery()
        self.MyConfig = lib.myconfig.MyConfig()
        
        self.EditDB = EditDBClass()
        self.theinit()


    def getStartingHtml(self):
        db2create = os.path.join(self.curdir,'res','data.db')
        rootDir = os.path.join(self.configXml.find('location').text,'pics')
        thumbsDir =os.path.join(self.configXml.find('location').text,'thumbs')
        
        conn = sqlite3.connect(db2create)
        c = conn.cursor()
        c.execute('select * FROM all_pics')
 
        frame = self.web.page().mainFrame()
        document = frame.documentElement()
        indexWrapper = document.findFirst("div#indexWrapper")
        
        labels = []    
        for row in c:
            label = row[1]
            if label not in labels:
                labels.append(label)
                src = row[0].replace(rootDir,thumbsDir)
                
                div = ET.Element('div')
                div.attrib['onClick'] = self.lib.getEventClickString(self.curdir,label,'none','front')

                img = ET.SubElement(div,'img', {'src':src})
                span = ET.SubElement(div,'span')
                span.text = label.replace('Gallery_','')

                indexWrapper.appendInside(ET.tostring(div))  
        
        c.close()

        

    def theinit(self):
        self.resize(1200, 700)
        self.setWindowTitle('Image Gallery')
        self.setWindowIcon(QtGui.QIcon(os.path.join(self.curdir,'res','app_icon.png')))
        
#        self.status = self.statusBar()
#        self.status.setSizeGripEnabled(True)
#        self.status.showMessage("Welcome")
#        self.status.hide()

        start_page = os.path.join(self.curdir,'index.html')
        self.web = QtWebKit.QWebView(self)
        self.web.load(QtCore.QUrl(start_page))
        #self.web.page().setLinkDelegationPolicy(2)

        # dom inspector, plugins and javascript 
        self.web.page().settings().setAttribute(QtWebKit.QWebSettings.DeveloperExtrasEnabled, 7)
        self.web.settings().setAttribute(QtWebKit.QWebSettings.PluginsEnabled, False)

        self.setCentralWidget(self.web)
        self.web.show()
        self.center()

        QtCore.QObject.connect(self.web, QtCore.SIGNAL("loadFinished (bool)"), self.wbLoadEnd)
        QtCore.QObject.connect(self.web.page().mainFrame(), QtCore.SIGNAL("javaScriptWindowObjectCleared ()"), self.jsCleared)
        self.connect(self, QtCore.SIGNAL('keyPressEvent()'), self.keyPressEvent)

        self.connect(self.EditDB, QtCore.SIGNAL("postResultsThread_EditDB_caller(QString,QString)"), self.update)
        self.connect(self.Image_Gallery, QtCore.SIGNAL("postResultsThread_Query(QString)"), self.wbInsertHtml)
        self.connect(self.Image_Gallery, QtCore.SIGNAL("postResultsThread_QueryStart(QList)"), self.Thread_QueryStart)


    def wbInsertHtml(self, html):
        self.web.setHtml(html) 

    def Thread_QueryStart(self,queryInfo):
        # this function is called when the query thread
        # has started. It serves as a loading message.
        html = ''
        div = ET.Element('div')
        for item in queryInfo:
            span = ET.SubElement(div,'span')
            span.text = unicode(item)
        html += ET.tostring(div)
            
        Template = self.templates.PageLoading(self.curdir,'Page Loading',html)
        self.web.setHtml(Template) 
        

    def update(self,nAll,nCur):
        # this shows the update messages from
        # the EditDBClass thread.
        frame = self.web.page().mainFrame()
        document = frame.documentElement()
        results = document.findFirst("div#results")
        results.setStyleProperty('display','block')
        txt = 'Found : '+nCur+' of : '+nAll
        results.setPlainText(txt)


    def jsCleared(self):
        frame = self.web.page().mainFrame()
        frame.addToJavaScriptWindowObject("EditDB",self.EditDB)
        frame.addToJavaScriptWindowObject("Image_Gallery",self.Image_Gallery)
  

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
        
        
    def keyPressEvent(self, event):
        #print ("keyPressEvent : ",event.key())
        if event.key() == QtCore.Qt.Key_X:
            self.showFullScreen()
            # self.status.hide()
        if event.key() == QtCore.Qt.Key_C:
            self.showNormal()
            # self.status.show()
        if event.key() == QtCore.Qt.Key_U:
               self.web.setZoomFactor(1.5)
        if event.key() == QtCore.Qt.Key_I:
               self.web.setZoomFactor(1)
        if event.key() == QtCore.Qt.Key_O:
               self.web.setZoomFactor(0.8)
               
               
    def about(self):
        info = "theBrowser"
        QtGui.QMessageBox.information(self, "Information", info)

        
    def wbLoadEnd(self):
        #print ('wbLoadEnd')
        title = self.web.title()
        if title == 'Hall':
            self.getStartingHtml()
            

        
        
    def getMainDir(self):
        '''Get script or exe directory.'''
        if hasattr(sys, 'frozen'): #py2exe, cx_freeze
            app_path = os.path.dirname(sys.executable)
            print ('Executing exe', app_path)
        elif __file__: #source file
            app_path = os.path.dirname(sys.argv[0])
            print ('Executing source file', app_path)
        return app_path 
       
       

       
       
       
if __name__ == "__main__":
    '''Get script or exe directory.'''
    app_path = ''
    if hasattr(sys, 'frozen'): #py2exe, cx_freeze
        app_path = os.path.dirname(sys.executable)
        print ('Executing exe', app_path)
    elif __file__: #source file
        app_path = os.path.dirname(sys.argv[0])
    
    print ('apppath : ',app_path)
    app = QtGui.QApplication(sys.argv)

    splash_pix = QtGui.QPixmap(os.path.join(app_path,'res','splash.png'))
    splash = QtGui.QSplashScreen(splash_pix)
    splash.setMask(splash_pix.mask())
    splash.show()

    time.sleep(2)

    main = MainWindow()
    splash.finish(main)
    main.show()

    sys.exit(app.exec_())




        




