====================================================
Installation
====================================================

This repository mantains the code for deploying the TranSapp visualization server on a linux machine

For install this server first get the source of the project

```(bash)
# Run on the target machine
$ git clone https://github.com/InspectorIncognito/visualization.git
```
Place the project in the principal user folder

Next, you need install the server prerequisites, for that execute the bash file prerequisites.bash

```(bash)
# Run on the target machine in the visualization folder
$ bash prerequisites.bash
```

For the database of the server, first you need to create a empty database in postgres. Also you need a dump 
from transapp database app (AndroidRequest) for a initial work and migrations. Using psql clone the dump in your empty database

```(bash)
# Run on the target machine in the visualization folder
$ psql <your database> < <dump from database>
```

After that you need make the migrations

```(bash)
$ python manage.py migrate
$ python manage.py collectstatic
```

Also you need add your database configuration, for that create a file called database.py in visualization/visualization/ whit the next info

```(python)

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql_psycopg2',
       'NAME': <your database name>,
       'USER': <your user from the database>
       'PASSWORD': <your user password>,
       'HOST': 'localhost',
       'PORT': '',
   }
}

```

Also you need to generate a secret key for the django app, for that get a key (http://www.miniwebtool.com/django-secret-key-generator/) and write in
visualization/visualization/keys/secret_key.txt

You need to add the public-key from the server that will send you the data.

For apache configuration, first go to the folder /etc/apache2/sites-available and open the file 000-default.conf
Copy the next configuration

```(xml)
<VirtualHost *:80>
    . . .

    Alias /static /home/<your user>/visualization/static
    <Directory /home/<your user>/visualization/static>
        Require all granted
    </Directory>

    <Directory /home/<your user>/visualization/visualization>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>

    WSGIDaemonProcess visualization python-path=/home/<your user>/visualization:/home/<your user>/visualization/visualizationenv/lib/python2.7/site-packages
    WSGIProcessGroup visualization
    WSGIScriptAlias / /home/<your user>/visualization/visualization/wsgi.py

</VirtualHost>
```

