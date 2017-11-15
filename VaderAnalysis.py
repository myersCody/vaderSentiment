import glob
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

DATA_DIR = 'Emilys_Data'
class VaderAnalysis():
    '''The purpose of this class is to organize what files pertain to which
    community, and to loop through each comment raiting them based of serveral 
    different methods and store these scores to a database'''
    def __init__(self):
        self.communities = self.sort_communities()  #<dict: <list:string>> A dict where the keys are community names and the values are a list of strings. 
    
    def find_files(self):
        '''This method walks through the DATA_DIR directory collecting file
        paths of all .txt files.
        
        Returns:
            txt_files: a list of strings
        '''        
        txt_files = []
        for root, dirs, files in os.walk(DATA_DIR):
            for file in files:
                if file.endswith(".txt"):
                    txt_file = os.path.join(root, file)
                    txt_files.append(txt_file)
        #print txt_files
        return txt_files
                    
    def sort_communities(self):
        '''This method loops through the txt_files list organizing all of the 
        file_paths by which community the txt file is generated from. 
        e.g.
        Emilys_Data/mozilla/pulls/mozilla(pg.1-50) belongs to mozilla
        
        Returns:
            communities: dict where values are a list of file_paths
        '''
        txt_files = self.find_files()
        communities = {}
        for path in txt_files:
            #The second element in the file_path is the community name
            community = path.split('/')[1] 
            if community in communities.keys():
                data_list = communities[community] 
                data_list.append(path)
                communities[community] = data_list
            else:
                communities[community] = [path]
        #print communities
        return communities
    
    def read_files(self):
        '''This method loops through all of the communities in our dictionary,
        and strips the content of indentions and next_page characters. Then
        it calls the a method that runs the vader sentiment analysis.'''
        communities_keys = self.communities.keys()
        for key in communities_keys:
            data_list = self.communities[key]
            for file_path in data_list:
                with open(file_path) as f:
                    content = f.readlines()
                    content = [x.strip() for x in content]
                    self.analyze_content(content)
            
    def analyze_content(self,content):
        '''This method uses the vader SentimentIntensityAnalyzer to process 
        each comment in a text file.
        
        Args:
            content: <list: string> A list of file paths leading to community comment data.
        '''
        analyzer = SentimentIntensityAnalyzer()
        for sentence in content:
            vs = analyzer.polarity_scores(sentence)
            print (vs)
            #print("{:-<65} {}".format(sentence, str(vs)))
        
if __name__ == "__main__":
    vader_obj = VaderAnalysis()
    vader_obj.read_files()
    vader_obj.sort_communities()