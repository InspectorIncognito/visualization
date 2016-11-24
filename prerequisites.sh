
#####################################################################
# CONFIGURATION
#####################################################################

install_packages=true
postgresql_configuration=true
project_configuration=true
apache_configuration=true
import_data=true

#####################################################################
# REQUIREMENTS
#####################################################################

if $install_packages; then
  sudo apt-get update
  #install django
  sudo apt-get install python-django
  #install postgres
  sudo apt-get install postgresql postgresql-contrib
  #install npm
  sudo apt-get install nodejs
  sudo apt-get install npm
  #install bower
  sudo npm install -g bower
  bower install
  #install postgis
  sudo apt-get install postgis
  #install gdal
  sudo apt-get install libgdal-dev
  sudo pip install gdal
fi



