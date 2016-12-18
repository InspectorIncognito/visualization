
#####################################################################
# REQUIREMENTS
#####################################################################
# Install all necesary things
sudo apt-get update
# install python and pip
sudo apt-get --yes install python-pip python-dev libpq-dev
# install django
pip install -U Django
# install postgres
sudo apt-get --yes install postgresql postgresql-contrib
# install npm
sudo apt-get --yes install nodejs
sudo apt-get --yes install npm
sudo ln -s /usr/bin/nodejs /usr/bin/node
# install bower
sudo npm install -g bower
bower install --allow-root
# install postgis
sudo apt-get install postgis
# install gdal
sudo apt-get install --yes binutils libproj-dev gdal-bin
sudo apt-get install --yes openssh-server
pip install django-crontab
pip install psycopg2
pip install pytz
# install apache
sudo apt-get install --yes apache2 libapache2-mod-wsgi



