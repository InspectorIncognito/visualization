
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
  #install python and pip
  sudo apt-get install python-pip python-dev libpq-dev
  #install django
  pip install django psycopg2
  #install apache
  sudo apt-get install apache2
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
  sudo apt-get install binutils libproj-dev gdal-bin
fi



