import sqlite3
import os, sys
import importlib
import time
import datetime
from db.models import *

DB_FILE = 'db/data.sqlite'
ARCHIVE = 'db/archive/'

class Database_Helper():
    def __init__(self):
        self.create_db()
        
    def create_db(self):
        if os.path.isfile(DB_FILE):
            time_stamp   = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H:%M:%S')
            new_filename = "".join([ARCHIVE,time_stamp,'.sqlite'])
            os.rename(DB_FILE, new_filename)
            print ("creating empty database file")
            open(DB_FILE, 'a').close()
        self.create_tables()
    
    def create_tables(self):
        #We need to change the cwd so that the db file will be saved in the right place
        current_path = os.getcwd()
        tmp_path     = os.path.join(current_path,DB_FILE).split('data.sqlite')[0]
        os.chdir(tmp_path) 
        classes=[]
        conf = ['Community','Comments']
        for str in conf:
            classes.append(getattr(sys.modules[__name__],str))
        mainDB.create_tables(classes)
        os.chdir(current_path)
    
    def insert_community(self,community_name):
        try:
            community = Community(name=community_name).save(force_insert=True)
            return True
        except Exception as e:
            return False    
    
    def insert_comment(self,comment_dict):
        self.insert_community(comment_dict['community'])
        comment = Comments(  community = comment_dict['community'],
                             sentence  = comment_dict['sentence'],
                             neg       = comment_dict['neg'],
                             neu       = comment_dict['neu'],
                             pos       = comment_dict['pos'],
                             compound  = comment_dict['compound']
                  ).save()
        return True
        
    
if __name__ == "__main__":
    db_helper = Database_Helper()
    comment_dict = {'sentence': 'funny :)', 'neg': 0.0, 'compound': 0.7096, 'pos': 1.0, 'community': 'linux', 'neu': 0.0}
    db_helper.insert_community(comment_dict['community'])
    db_helper.insert_comment(comment_dict)