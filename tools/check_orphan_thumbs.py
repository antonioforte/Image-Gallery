#!/usr/bin/env python
import os 
import pprint
import hashlib
from collections import defaultdict
import logging
import logging.handlers
from xml.etree import ElementTree as ET

# inspiration
# http://www.endlesslycurious.com/2011/06/01/finding-duplicate-files-using-python/

class Main():
    def __init__(self,rootdir):

        self.configxml = self.get_config_xml()
        self.exts = self.configxml.find('exts').text
        self.rootdir = self.configxml.find('location').text
        self.thumbsdir = os.path.join(self.rootdir,'thumbs')
        self.picsdir = os.path.join(self.rootdir,'pics')
        

        thumbs = self.walkDir(self.thumbsdir,self.exts)
        self.print_orphan_thumbs(thumbs, self.thumbsdir, self.picsdir)


    def print_orphan_thumbs(self,thumbs,thumbsdir, picsdir):
        o = 0
        for item in thumbs:
            fullurl = item[0]
            relpath = self.trim_first_slash(fullurl[len(thumbsdir):])
            bigpicpath = os.path.join(picsdir,relpath)

            if not os.path.exists(bigpicpath):
                self.delete_file(fullurl)
                o += 1
        print('Found orphan thumbs : ',str(o))


    def trim_first_slash(self,thestr):
        if thestr.startswith("/"):
            return thestr[1:]
        else:
            return thestr
        


    def walkDir(self,dir,exts):
        items = []
        try:
            for root,dirs,files in os.walk(unicode(dir)):
                for file in files:
                    full_url = os.path.join(dir,root,file)
                    url, ext = os.path.splitext(full_url)
                    if ext.lower() in exts:
                        items.append([full_url,ext,file])
        except Exception as e:
            print("Error walkDir : ", e)
        return items



    def delete_file(self,filepath):
        try:
            os.remove(filepath)
            print('Removing ',filepath)
        except Exception as e:
            print ("Error executing. ",e.args)
        


    def get_config_xml(self):
        script_path = os.path.abspath(os.path.dirname(__file__))
        parent = os.path.normpath(os.path.join(script_path, '..'))
        tree = ET.parse(os.path.join(parent, 'config.xml'))
        return tree
        
        
if __name__ == "__main__":
    Main("/media/vault_small/Gallery/pics")
        
        
        
        
