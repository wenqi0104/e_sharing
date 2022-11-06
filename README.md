# e_sharing
>git clone https://github.com/wenqi0104/e_sharing.git  

## Run in local environment

+ Create superuser for admin
```
py manage.py createsuperuser
```
+ Execute commands in terminal for migrations
```
py manage.py makemigrations
py manage.py migrate
```
+ Install dependencies in requirements.txt
```
pip install geocoder
```
+ Modify the database account and password in settings.py 
+ Run server
```
py manage.py runserver
```
