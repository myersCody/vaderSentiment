import glob
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

DATA_DIR = 'Emilys_Data'
class VaderAnalysis():
    def __init__(self):
        self.communities = self.sort_communities()
    
    def find_files(self):
        txt_files = []
        for root, dirs, files in os.walk(DATA_DIR):
            for file in files:
                if file.endswith(".txt"):
                    txt_file = os.path.join(root, file)
                    txt_files.append(txt_file)
        return txt_files
                    
    def sort_communities(self):
        txt_files = self.find_files()
        communities = {}
        for path in txt_files:
            community = path.split('/')[1]
            if community in communities.keys():
                data_list = communities[community] 
                data_list.append(path)
                communities[community] = data_list
            else:
                communities[community] = [path]
        return communities
    
    def read_file(self):
        communities_keys = self.communities.keys()
        for key in communities_keys:
            data_list = self.communities[key]
            for file_path in data_list:
                with open(file_path) as f:
                    content = f.readlines()
                    content = [x.strip() for x in content]
                    self.sort_content(content)
            
    def sort_content(self,content):
        #for line in content:
        analyzer = SentimentIntensityAnalyzer()
        for sentence in content:
            vs = analyzer.polarity_scores(sentence)
            print (vs)
            #print("{:-<65} {}".format(sentence, str(vs)))
        
if __name__ == "__main__":
    vader_obj = VaderAnalysis()
    vader_obj.read_file()
    vader_obj.sort_communities()
    #vader_obj.read_file('I\'m Piiiiiiiickle Rick')
    