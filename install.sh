#!/bin/bash
database="xmeme"
#password=""

#export PGPASSWORD=$password
#sudo apt install postgresql postgresql-contrib
sudo apt-get install -y postgresql postgresql-contrib.
sleep 1
sudo -u postgres createdb xmeme
sleep 1
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'patralekha';"
sleep 2

sudo apt-get install -y python3.6
sudo apt-get install -y python3-pip

sleep 5
pip3 install ural
python3 -m pip install Django
pip3 install -r requirements.txt

path=`which python3`
sudo ln -sfn $path /usr/bin/python

