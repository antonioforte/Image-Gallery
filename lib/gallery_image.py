import os
from xml.etree import ElementTree as ET
import templates
import common
import sqlite3
from PyQt4 import QtCore



class Worker(QtCore.QThread):
    def __init__(self, parent = None):
        QtCore.QThread.__init__(self, parent)
        self.exiting = False
        self.lib = common.common() 
        self.templates = templates.templates()

    def __del__(self):
        self.exiting = True

    def setValues2Search(self,curdir,gallery,galItem,mode):
        self.curdir = str(curdir)
        self.mode = mode
        self.gallery = gallery
        self.galItem = galItem
        self.configXml = self.lib.getXml(os.path.join(self.curdir,'config.xml'))
        self.dbPath = os.path.join(self.curdir,'res','data.db')
        self.rootDir = os.path.join(self.configXml.find('location').text,'pics')
        self.thumbsDir =os.path.join(self.configXml.find('location').text,'thumbs')
        
    def run(self):
        if self.mode == 'front':
            self.getGalleryItems()
        if self.mode == 'galItems':
            self.getGalleryItemsFiles()




    def getGalleryItems(self):
        pageTitle = unicode(self.gallery).replace('Gallery_','')
        Template = self.templates.Page(self.curdir,pageTitle)
        
        conn = sqlite3.connect(self.dbPath)
        c = conn.cursor()
        t = unicode(self.gallery)
        c.execute('select * FROM all_pics WHERE gallery=? ORDER BY galleryItem', (t,))
     
        html = ''
        galItems = []
        for row in c:
            galItem = row[2]
            if galItem not in galItems:
                galItems.append(galItem)
                src = row[0].replace(self.rootDir,self.thumbsDir)
                
                div = ET.Element('div')
                div.attrib['onClick'] = self.lib.getEventClickString(self.curdir,self.gallery,galItem,'galItems')
                div.attrib['data-gallery_item_label'] = galItem
                img = ET.SubElement(div,'img', {'src':'file://'+src})
                span = ET.SubElement(div,'span')
                span.text = self.lib.getShortString(25,galItem)

                html += ET.tostring(div)
        
        c.close()
        outHtml = Template.replace('_contents_',html)
        self.emit(QtCore.SIGNAL("postResultsThread(QString)"),outHtml)




    def getGalleryItemsFiles(self):
        pageTitle = unicode(self.gallery).replace('Gallery_','') +' - '+unicode(self.galItem)
        Template = self.templates.PageFiles(self.curdir,pageTitle)
        
        conn = sqlite3.connect(self.dbPath)
        c = conn.cursor()
        t = (unicode(self.gallery),unicode(self.galItem))
        c.execute('select * FROM all_pics WHERE gallery=? AND galleryItem=? ORDER BY filename_head', (t))

        html = ''
        for row in c:
            src = row[0].replace(self.rootDir,self.thumbsDir)
            
            div = ET.Element('div')
            div.attrib['onClick'] = 'LibCommon.launchIndividualImage("'+row[0]+'")'
            div.attrib['data-big_pic_url'] = row[0]
            div.attrib['data-filename'] = row[9]
            div.attrib['class'] = 'individual_pic'
            img = ET.SubElement(div,'img', {'src':'file://'+src})

            html += ET.tostring(div)

        c.close()
        
        span = ET.Element('span')
        span.text = 'back'
        span.attrib['id'] = 'gobackLink' 
        span.attrib['onClick'] = self.lib.getEventClickString(self.curdir,unicode(self.gallery),'none','front')
        outHtml = Template.replace('_back_',ET.tostring(span))
        outHtml = outHtml.replace('_contents_',html)
        self.emit(QtCore.SIGNAL("postResultsThread(QString)"),outHtml)



class Image_Gallery(QtCore.QObject):

    @QtCore.pyqtSlot(str,str,str,str)
    def go(self,curdir,gallery,galItem,mode):
        self.queryInfo = [gallery,galItem,mode]
        self.thread = Worker()
        self.thread.setValues2Search(curdir,gallery,galItem,mode)
        self.connect(self.thread, QtCore.SIGNAL("started()"), self.sayStart)
        self.connect(self.thread, QtCore.SIGNAL("finished()"), self.sayEnd)
        self.connect(self.thread, QtCore.SIGNAL("terminated()"), self.sayEnd)
        self.connect(self.thread, QtCore.SIGNAL("postResultsThread(QString)"), self.postHtml)
        self.thread.start()


    def sayEnd(self):
        print ('Thread query has ended')
        
    def sayStart(self):
        print ('Thread query has started')
        self.emit(QtCore.SIGNAL("postResultsThread_QueryStart(QList)"),self.queryInfo)
        
    def postHtml(self,html):
        print ('Thread query : postResultsThread_Query')
        self.emit(QtCore.SIGNAL("postResultsThread_Query(QString)"),html)
        
        

        
        
        
        
        
        
