
# This file will create a virtualenv that will handle all of the dependencies for
# our scripts. So that the scripts will work in both python3 & python2

'''
Helpful Commands:
   1) Source Setup.sh
   2) deactivate
   3) . venv/bin/activate
'''


mkdir -p data

if [ ! -d venv ]
then
  virtualenv venv
fi

. venv/bin/activate

sudo pip3 install peewee --upgrade

pip install peewee  --upgrade
pip install pyyaml  --upgrade
pip install pathlib
pip install nltk 
pip install requests
pip install tqdm
sudo pip3 install tqdm