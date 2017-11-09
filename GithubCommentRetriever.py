import requests
import json
import os
import logging
import datetime
import time

#May require installs
import yaml              #sudo pip install pyyaml
from pathlib import Path #sudo pip install pathlib //install not needed for python3

#Global Variables
LOGFILENAME = 'GithubCommentRetriever.log'
SAVEFILE    = 'save.yaml'
DATADIRNAME = '/Emilys_Data/'


class GithubCommentRetriever():
    '''NOTE: For more information about the github api visit: 
    https://docs.google.com/document/d/1VTt7edWW2N5Wg8_H-Lbct5cYMohgnhgtzIzOSZbNtqs/edit?usp=sharing
    '''
    def __init__(self):
        self.basic_url       = 'https://api.github.com/repos/{0}/{1}'                           #<string> The core github api repo. {0} repo_owner, {1} repo_name
        self.comment_type    = ''                                                               #<string> One of the github comment types explained in __main__
        self.dir_name        = ''                                                               #<string> Name of the directory to save the data under
        self.repo_owner      = ''                                                               #<string> Name of the repo owner on github
        self.repo_name       = ''                                                               #<string> Name o fthe repo on github
        self.next_page       = ''                                                               #<string> url to the next github api page of comments
        self.comments        = []                                                               #<list: string> all of the commments collected
        self.data_dir        = os.path.dirname(os.path.realpath(__file__)) + DATADIRNAME        #<string> the file path for a directory you use to save your data
        
    def set_logging_info(self):
        '''Setups the log file for the logging library'''
        log_path = "".join([self.data_dir, LOGFILENAME]) #most efficent method for concatinating two strings
        Path(log_path).touch()                           #performs a linux touch command
        logging.basicConfig(format='%(asctime)s : %(message)s', filename=log_path, level=logging.DEBUG, datefmt='%m/%d/%Y %I:%M:%S %p')
        return True
    
    def set_github_info(self,dir_name,repo_owner,repo_name,comment_type):
        '''
        Sets instance variables that are used in multiple methods.
        
        Args:
            dir_name:     <string> Name of the directory to save the data under
            repo_owner:   <string> Name of the repo owner on github
            repo_name:    <string> Name o fthe repo on github
            comment_type: <string> One of the github comment types explained in __main__
        
        Returns: 
            True: Successful
        '''
        self.dir_name     = dir_name
        self.repo_owner   = repo_owner
        self.repo_name    = repo_name
        self.comment_type = comment_type
        return True
        
    def rate_limit_message(self):
        '''
        A warning messaging notifing the user that we hit the rate limit
        '''
        print "---------------WARNING---------------"
        print "We have reached our rate limit for accessing the github api information."
        print "The rate limit should be reset in about in hour. For more information"
        print "visit: https://developer.github.com/v3/#rate-limiting"
        print "-------------------------------------"
        return True
        
    def check_rate_limit(self):
        '''Prints infomation regarding the rate limit to the user'''
        rate_url  = 'https://api.github.com/rate_limit'
        r         = requests.get(rate_url)
        raw       = r.json()
        info_dict = raw['rate']
        print "Rate Limit Max: {}".format(info_dict['limit'])
        print "Request Remaining: {}".format(info_dict['remaining'])
        print "Reset time: {}".format(self.convert_unix_time(info_dict['reset']))
        return True
        
    def convert_unix_time(self, epoch_seconds):
        '''The reset time is returned as a UTC string, this method converts the
        string into your local time'''
        greenwich_time        = datetime.datetime.utcfromtimestamp(int(epoch_seconds))
        eastern_time          = greenwich_time - datetime.timedelta(hours=5)
        standard_eastern_time = datetime.datetime.strftime(eastern_time,"%m/%d/%Y %I:%M:%S %p")
        return standard_eastern_time
        
        
    def recover_comments(self):
        '''
        A recursive method that pulls a json dictionary of 100 comments per page.
        Github api has a rate limit of 60 pages per hour. 
        '''
        if self.next_page == '':
            self.next_page = ''.join([self.basic_url.format(self.repo_owner,self.repo_name),self.comment_type,'?per_page=100'])
        logging.info(self.next_page)
        r = requests.get(self.next_page)
        raw = r.json()
        links = r.links
        logging.debug(str(links))
        if r.status_code != 200:            
            if r.status_code == 403: #rate limit message is opptional                
                self.rate_limit_message()
                logging.warning("Error: {0} Github Api call was unsuccessful. The rate limit was likly met for github api calls.".format(r.status_code))
            else:
                logging.warning("Error: {0} Github Api call was unsuccessful".format(r.status_code))
            return r.status_code
        else:
            try:                                            
                for comment in raw:
                    comment = comment['body']
                    comment = comment.encode('utf-8') #Essential for elements outside of ascii range(128)
                    self.comments.append(comment)                
                try:
                    self.next_page = links['next']['url'] #[4]
                except Exception as e:
                    logging.info(e)
                    logging.info('End of recursive cycle.')
                    return True
                self.recover_comments()
                
            except Exception as e:                
                logging.warning(e)
                return True
        
    def write_comments(self):
        '''
        This method writes all of the comments to an output file.
        '''
        file_dir = "".join([self.data_dir,self.dir_name])
        dir_status = os.path.isdir(file_dir) #Make sure directory exist
        if dir_status == False:
            os.mkdir(file_dir)
        filename  = "".join([self.dir_name,'.txt']) #create Filename
        file_path = "".join([file_dir,'/',filename]) #create filepath
        f = open(file_path, "a+")
        for comment in self.comments: #add comments to file
            try: 
                line = "".join([comment,'\n'])
                f.write(line)
            except Exception as e:
                logging.debug('e')
                logging.debug('Failed to write line: ({}) to file.'.format(line)) 
                pass
        f.close()
        return True
    
    def save_place(self):
        '''This method allows us to save where we have stopped so that we can 
        continue after our rate limit timeout is up. '''
        logging.warning('A save place was triggered for url: {}'.format(self.next_page))
        #file_path = self.data_dir + 'save.yaml'
        file_path = "".join([self.data_dir,SAVEFILE])
        data = {str(self.dir_name):{'next_page':self.next_page}} #Sets up our config file format
        #used w to prevent duplicate keys
        #old save data is located in the logs
        with open(file_path, 'w') as outfile: 
            yaml.dump(data, outfile, default_flow_style=False)
        outfile.close()
        return True
        
    def read_save_file(self):
        '''This method coverts our save yaml file in to a dictionary so that we 
        can continued from our last stopping point.'''
        file_path = "".join([self.data_dir,SAVEFILE])
        try:
            with open(file_path, 'r') as ymlfile:
                cfg = yaml.load(ymlfile)
                return cfg
        except Exception as e:
            print e
            return False
    
    def main(self):
        '''You MUST run self.set_github_info before running main.'''
        self.set_logging_info()
        cfg = self.read_save_file()
        try: #Check to see if there is any save file data
            cfg[self.dir_name]
            self.next_page = cfg[self.dir_name]['next_page']
        except Exception as e:
            pass
        status = self.recover_comments()              
        self.save_place()
        if self.comments != []:
            self.write_comments()
        self.check_rate_limit()
        
if __name__ == '__main__':
    """Steps:
    1) run set_github_info in order for the class to work properly
    2) ensure that you want the data in your save point in save.yaml (if there is any)
    3) run python GithubCommentRetriever.py
    4) rename the file and place it in the correct directory.
    5) repeat
    """
    github_tool = GithubCommentRetriever()
    '''Mozilla Data'''    
    #github_tool.set_github_info('mozilla','devtools-html','debugger.html','/issues/comments') #Completed on 20171030
    #github_tool.set_github_info('mozilla','devtools-html','debugger.html','/pulls/comments')  #Completed on 20171101
    '''Linux Data'''
    #github_tool.set_github_info('linux','torvalds','linux','/issues/comments') #Completed on 20171107
    #github_tool.set_github_info('linux','torvalds','linux','/pulls/comments')  #Completed on 20171107 (I want to check this, we should have more than two pages)
    '''Racket Data'''
    #github_tool.set_github_info('racket','racket','racket','/issues/comments') #Completed on 20171107
    #github_tool.set_github_info('racket','racket','racket','/pulls/comments')  #Completed on 20171107
    '''Open MRS'''
    #github_tool.set_github_info('openmrs','openmrs','openmrs-core','/issues/comments')
    #github_tool.set_github_info('openmrs','openmrs','openmrs-core','/pulls/comments')
    '''Sahana Eden'''
    #github_tool.set_github_info('sahana','sahana','eden','/issues/comments')
    github_tool.set_github_info('sahana','sahana','eden','/pulls/comments')
    github_tool.main()