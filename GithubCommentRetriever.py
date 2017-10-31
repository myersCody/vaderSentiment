import requests
import json
import os
import yaml #pip install pyyaml

class GithubCommentRetriever():
    def __init__(self):
        self.basic_url       = 'https://api.github.com/repos/{0}/{1}'
        self.comment_type    = ''
        self.dir_name        = ''
        self.repo_owner      = ''
        self.repo_name       = ''
        self.next_page       = ''
        self.comments        = []
        self.data_dir        = os.path.dirname(os.path.realpath(__file__)) + '/Emilys_Data/'
        
    def set_github_info(self,dir_name,repo_owner,repo_name,comment_type):
        '''[dir_name]   - <string> Name of the directory to save the data under
           [repo_owner] - <string> Name of the repo owner on github
           [repo_name]  - <string> Name of the repo on github'''
        self.dir_name     = dir_name
        self.repo_owner   = repo_owner
        self.repo_name    = repo_name
        self.comment_type = comment_type
        return True    
        
    def recover_comments(self):        
        '''Future Work:
        (1) GitHub API currently only returns 30 items per request. There may
            be a work around through pagination. To summerize pagination we need
            to find the total number of page and loop through each page by adding
            `page={{page_number}}` to the end. 
            * curl -i https://api.github.com/repos/devtools-html/debugger.html/issues/comments?page=1&per_page=100
            * curl -i https://api.github.com/repos/devtools-html/debugger.html/issues/comments?per_page=100
        '''
        if self.next_page == '':
            self.next_page = self.basic_url.format(self.repo_owner,self.repo_name) + self.comment_type + '?per_page=100'
        r = requests.get(self.next_page)
        raw = r.json()
        links = r.links
        if r.status_code != 200:
            self.save_place()
            print r.status_code
            return r.status_code
        else:
            try: 
                self.next_page = links['next']['url'] #[4]
                for comment in raw:
                    comment = comment['body']
                    comment = comment.encode('utf-8')
                    self.comments.append(comment)
                self.recover_comments()
            except:
                return True
        
    def write_comments(self):
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
    
    def main(self):
        status = self.recover_comments()
        self.write_comments()
        
if __name__ == '__main__':
    ''' The github api[0] requires certain structures to recover comments from repos
        * commit comments structure [1]: GET /repos/:owner/:repo/comments 
        * issue comments structure [2]:  GET /repos/:owner/:repo/issues/comments 
        * pull request comments [3]:     GET /repos/:owner/:repo/pulls/comments
    '''
    github_tool = GithubCommentRetriever()
    #print "Mozilla"
    github_tool.set_github_info('mozilla','devtools-html','debugger.html','/issues/comments')    
    github_tool.main()    
        
'''
FOOTNOTES:
[0] - https://developer.github.com/v3/
[1] - https://developer.github.com/v3/repos/comments/#list-commit-comments-for-a-repository
[2] - https://developer.github.com/v3/issues/comments/#list-comments-in-a-repository
[3] - https://developer.github.com/v3/pulls/comments/#list-comments-in-a-repository
[4] - https://developer.github.com/v3/guides/traversing-with-pagination/
'''