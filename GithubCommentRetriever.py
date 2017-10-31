import requests
import json
import os
import yaml #pip install pyyaml

class GithubCommentRetriever():
    '''This class follows google doc string standards as well as pep8 styling
    NOTE: For more information about the github api visit: 
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
        self.data_dir        = os.path.dirname(os.path.realpath(__file__)) + '/Emilys_Data/'    #<string> the file path for a directory you use to save your data
        
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
        print "We hav ehit our rate limit for accessing the github api information."
        print "The rate limit should be reset in about in hour. For more information"
        print "visit: https://developer.github.com/v3/#rate-limiting"
        print "-------------------------------------"
        return True        
        
    def recover_comments(self):
        '''
        A recursive method that pulls a json dictionary of 100 comments per page.
        Github api has a rate limit of 60 pages per hour. 
        '''
        if self.next_page == '':
            self.next_page = self.basic_url.format(self.repo_owner,self.repo_name) + self.comment_type + '?per_page=100'
        r = requests.get(self.next_page)
        raw = r.json()
        links = r.links
        if r.status_code != 200:
            self.save_place()
            if r.status_code == 403:
                self.save_place()
                self.rate_limit_message() #optional
            return r.status_code
        else:
            try: 
                self.next_page = links['next']['url'] #[4]
                for comment in raw:
                    comment = comment['body']
                    # It is essential to encode our comment returns, 
                    # fails if not converted
                    comment = comment.encode('utf-8')  
                    self.comments.append(comment)
                self.recover_comments()
            except:
                return True
        
    def write_comments(self):
        '''
        This method writes all of the comments to an output file
        '''
        file_dir   = self.data_dir + self.dir_name        
        #Check to make sure directory exist
        dir_status = os.path.isdir(file_dir)
        if dir_status == False:
            os.mkdir(file_dir)
        #create filename & file path
        filename  = self.dir_name + '.txt'
        file_path = file_dir + '/' + filename
        #append comments to file
        f = open(file_path, "a+")
        for comment in self.comments:
            try: 
                line = comment + '\n'
                f.write(line)
            except Exception as e:
                print line
                print e
                pass
        f.close()
    
    def save_place(self):
        file_path = self.data_dir + 'save.yaml'
        data = {str(self.dir_name):{'next_page':self.next_page}}
        with open(file_path, 'a') as outfile:
            yaml.dump(data, outfile, default_flow_style=False)
        outfile.close()
        return True
        
    def read_save_file(self):
        file_path = self.data_dir + 'save.yaml'
        try:
            with open(file_path, 'r') as ymlfile:
                cfg = yaml.load(ymlfile)
                return cfg
        except Exception as e:
            print e
            return False
        
    
    def main(self):
        cfg = self.read_save_file()
        try: #Check to see if there is any save file data
            cfg[self.dir_name]
            self.next_page = cfg[self.dir_name]['next_page']
        except Exception as e:
            pass
        status = self.recover_comments()
        if self.comments != []:
            self.write_comments()
        
if __name__ == '__main__':
    ''' The github api[0] requires certain structures to recover comments from repos
        * commit comments structure [1]: GET /repos/:owner/:repo/comments 
        * issue comments structure [2]:  GET /repos/:owner/:repo/issues/comments 
        * pull request comments [3]:     GET /repos/:owner/:repo/pulls/comments
        Examples:
        * curl -i https://api.github.com/repos/devtools-html/debugger.html/issues/comments?page=1&per_page=100
        * curl -i https://api.github.com/repos/devtools-html/debugger.html/issues/comments?per_page=100
    '''
    github_tool = GithubCommentRetriever()
    #print "Mozilla"
    github_tool.set_github_info('mozilla','devtools-html','debugger.html','/issues/comments')    
    github_tool.main()    