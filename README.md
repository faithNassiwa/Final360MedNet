# 360MedNet
360MedNet is a networking platform for health professionals in Uganda.


## Installation
```
#clone the project.
git clone (project-link)

#Install requirements.
pip install requirements.pip

#Create postgres database

#Create .env file in the project's root directory
This file should contain all variables provided in settings.py. Refer to the env.sample file in the project root
directory to aid you create the .env file.

#Migrate migrations
python manage.py migrate

#Run django server in one terminal
python manage.py runserver



