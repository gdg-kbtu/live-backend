## TO RUN BACKEND SERVER YOU NEED:

1) You need to have python modules installed. If you don't have, install:

***in "live-backend" folder:***
```
python -m venv venv 
venv/Scripts/activate
python -m pip install Django
python -m pip install psycopg
```

If you use Linux:
```
python -m venv venv 
source venv/bin/activate
python -m pip install Django
python -m pip install psycopg
```


2) You need to have postgreSQL local server installed on your machine.  Install --> https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
   Open command line anywhere, then create database:
   ```
   psql -U [your username]
   [your password]
   CREATE DATABASE crm;
   ```



3) In settings.py,  in DATABASES section,  set USERNAME and PASSWORD to your username and password of postgresql server user

4) In "site" folder:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```


I hope at this point everything is set up

5) Run:
   ```
   python manage.py runserver
   ``` 

