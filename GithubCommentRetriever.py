import requests
import json
import os

class GithubCommentRetriever():
    def __init__(self):
        self.basic_url       = 'https://api.github.com/repos/{0}/{1}'
        self.comment_type    = ''
        self.dir_name        = ''
        self.repo_owner      = ''
        self.repo_name       = ''
        self.next_page       = ''
        self.comments        = ['testing']
        
    def set_github_info(self,dir_name,repo_owner,repo_name,comment_type):
        '''[dir_name]   - <string> Name of the directory to save the data under
           [repo_owner] - <string> Name of the repo owner on github
           [repo_name]  - <string> Name of the repo on github'''
        self.dir_name     = dir_name
        self.repo_owner   = repo_owner
        self.repo_name    = repo_name
        self.comment_type = comment_type
        return True    
        
    def set_next_page(self, next_page):
        self.next_page = next_page
        
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
            self.next_page = basic_url.format(self.repo_owner,self.repo_name) + self.comment_type + '?per_page=100'
        r = requests.get(self.next_page)
        raw = r.json()
        links = r.links
        if r.status_code != 200:
            #TODO: Save the current data
            # Save the current page
            # Most likly the rate limit was reached and we needed to continue
            # this work later
            print response.status_code
            return response.status_code
        else:
            self.next_page = links['next'] #[4]
            for comment in raw:
                comment = comment['body']
                self.comments.append(comment)
        
    def write_comments(self):
        
    

                
        
        
            
        
if __name__ == '__main__':
    ''' The github api[0] requires certain structures to pull comments from repos
        * commit comments structure [1]: GET /repos/:owner/:repo/comments 
        * issue comments structure [2]:  GET /repos/:owner/:repo/issues/comments 
        * pull request comments [3]:     GET /repos/:owner/:repo/pulls/comments
    '''
    github_tool = GithubCommentRetriever()
    #print "Mozilla"
    #github_tool.set_github_info('mozilla','devtools-html','debugger.html','/issues/comments')    
    #github_tool.recover_comments()
    github_tool.write_comments()
    
        
'''
FOOTNOTES:
[0] - https://developer.github.com/v3/
[1] - https://developer.github.com/v3/repos/comments/#list-commit-comments-for-a-repository
[2] - https://developer.github.com/v3/issues/comments/#list-comments-in-a-repository
[3] - https://developer.github.com/v3/pulls/comments/#list-comments-in-a-repository
[4] - https://developer.github.com/v3/guides/traversing-with-pagination/
'''