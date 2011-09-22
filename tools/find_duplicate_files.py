#!/usr/bin/env python
import os 
import pprint
import hashlib
from collections import defaultdict
import logging
import logging.handlers


# inspiration
# http://www.endlesslycurious.com/2011/06/01/finding-duplicate-files-using-python/

class Main():
    def __init__(self,rootdir):
        self.log = self.create_log()
        sizes = self.get_sizes(rootdir)
        dups, all = self.check_hash(sizes)
        
        print('-------------------------------------')
        self.delete_files(dups)
        
        for item in dups:
            print(item)
        self.log.debug('Found %s duplicates ' % len(dups))
        #pprint.pprint(dups)
        
        

    def get_sizes(self, rootdir):
        '''Get files with same size'''
        sizes = defaultdict(list)

        i = 0
        for root, dirs, files in os.walk( rootdir ):
            for filename in files:
                filepath = os.path.join( root, filename )
                filesize = os.stat( filepath ).st_size
            
                i += 1
                sizes[filesize].append(filepath)
        self.log.debug('Found %d files ' % i)
        return sizes






    def check_hash(self,sizes):
        '''Return a list with duplicates.'''
        unique = []
        duplicates = []
        all = defaultdict(list)
    
        for key in sizes:
            if len(sizes[key]) > 1:
                for filepath in sizes[key]:
                    filehash = hashlib.md5(open(filepath).read()).digest()

                    if filehash not in unique:
                        unique.append( filehash )
                    else:
                        print('Scanning files with same size',sizes[key])
                        duplicates.append( filepath )
                        print('Found duplicate : ',filepath)
                    all[filehash].append(filepath)
                        
        return duplicates, all




    def delete_files(self,dups):
        for filepath in dups:
            try:
                os.remove(filepath)
                self.log.debug('Removing %s ' % filepath)
                print('Removed : ',filepath)
            except Exception as e:
                print ("Error executing. ",e.args)
        


    def create_log(self):
        curdir = os.path.dirname(__file__)
        LOG_FILENAME = os.path.join(curdir,'log.log')

        my_logger = logging.getLogger('MyLogger')
        my_logger.setLevel(logging.DEBUG)
        handler = logging.handlers.RotatingFileHandler(
              LOG_FILENAME, maxBytes=2000, backupCount=5)
        
        my_logger.addHandler(handler)
        return my_logger
        
        
if __name__ == "__main__":
    Main("/media/vault_small/Gallery/pics")
        
        
        
        
