# INSTRUCTIONS:
#   DEPENDENCIES: This command has dependencies, all of the dependencies will be 
#     Downloaded into a virtual environment if you run the command:: source setup.sh
#   EXAMPLE USAGE: python RandomComments.py Linux 
#     (after RandomComments.py you will need to list the community 
#     you would like the random comments to come from)

from peewee import *
from db.models import *
from tqdm import tqdm
import sys, os
import random
import xlsxwriter

class Random_Comments():
    def __init__(self):
        self.args      = sys.argv
        self.community = self.community_exist()
        self.id_min    = self.find_min()
        self.id_max    = self.find_max()
        self.id_list   = []
        
    def community_exist(self):
        #mainDB.get_conn()
        print "Checking if community is in the database..."
        try:
            community = Community.get(Community.name == self.args[1].lower())
            print "Community exist... Continuing \n"
            return community.name
        except Exception as e:
            print "Error: The community ({0}) that you selected does not seem to exist".format(self.args[1].lower())
            print "Ensure that the database you are trying to access is located in db/data.sqlite"
            return "Error"
            
    def find_min(self):
        try: 
            query = "SELECT MIN(CID) as CID FROM comments WHERE comments.community_id == '{0}'".format(self.community)
            result = mainDB.execute_sql(query)
            return int(result.fetchone()[0])
        except Exception as e:
            return None
            
    def find_max(self):
        try: 
            query = "SELECT MAX(CID) as CID FROM comments WHERE comments.community_id == '{0}'".format(self.community)
            result = mainDB.execute_sql(query)
            return int(result.fetchone()[0])
        except Exception as e:
            return None

    def generate_ids(self,size=100):
        if len(self.id_list) == size:
            return True
        random_id = random.randint(self.id_min, self.id_max)
        if random_id not in self.id_list:
            self.id_list.append(random_id)
            self.generate_ids()
            return True
            
    def create_excel(self):
        #Create the file & setup the workbook
        filename = "{}_random_comments.xlsx".format(self.community)
        workbook = xlsxwriter.Workbook(filename)
        workbook.set_properties({
        'title': '100 Random Comments From {}'.format(self.community),
        'author': 'Cody Myers',
        'comments': 'Created with Pythn and XlsxWriter'})
        row_index = 2
        sheet = workbook.add_worksheet(self.community)
        sheet.write('A1', 'vader_compound')
        sheet.write('B1', 'comment')
        sheet.write('C1', 'emily_score')
        for cid in tqdm(self.id_list):
            comment_info = Comments.select().where(Comments.CID == cid).first()
            sheet.write('A{0}'.format(row_index),comment_info.compound)
            sheet.write('B{0}'.format(row_index),comment_info.sentence)
            row_index += 1
        workbook.close()        
            
    def main(self):
        print "Selecting random comments from the database...\n"
        self.generate_ids()
        print "Creating excel file..."
        self.create_excel()
                
if __name__ == "__main__":
    rand_helper = Random_Comments()
    rand_helper.main()
    