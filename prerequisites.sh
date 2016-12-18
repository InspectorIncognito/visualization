
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
# if scripts received a parameter, it is the linux user name where
# will be installed the project. Bower doesn't let you install with 
# sudo privileges
if [ -z "$1" ]; then
    LINUX_USER_NAME=$1
    sudo -u "$LINUX_USER_NAME" bower install
else
    bower install
fi
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



