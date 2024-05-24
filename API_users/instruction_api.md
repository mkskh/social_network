## to 'install and use the api.

- step into the folder API_users/ when running the command in terminal


### first to create a superuser with admin level permissions

- python manage.py createsuperuser
- name : adminapi (it recognize admin already been taken) 
- password : testapi1234
- email : admin@mail2.com

### creating the database:

- enter your postgresql

- place the following :

    - CREATE DATABASE api_user_social_network;

    - CREATE USER api_user_sn_admin WITH PASSWORD 'testapi1234';

    - ALTER DATABASE api_user_social_network OWNER TO api_user_sn_admin;

    - GRANT ALL PRIVILEGES ON DATABASE api_user_social_network TO api_user_sn_admin;

-
-

check if the database id correctly existing in dbeaver
( I have had an issue with postgreSQL i realised, where this USER even though giving all the privileges, was not having Superuser and all the pri


### set database in the conf/settings.py (possibly already set up):

```
 DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'api_user_social_network',                      
        'USER': 'api_user_sn_admin',
        'PASSWORD': 'testapi1234',
        'HOST': 'localhost',
        'PORT': 5432,
    }
} 
```


### to hide the credential, in the file .env put :

```
    DB_NAME2='api_user_social_network'
    DB_USER2='api_user_sn_admin'
    DB_PASSWORD2='testapi1234'
    DB_HOST2='localhost'
    DB_PORT2=5432
```

#### and replace the database in settings.py with the one already provided in comments above or same here: 

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME2'),
        'USER': os.getenv('DB_USER2'),
        'PASSWORD': os.getenv('DB_PASSWORD2'),
        'HOST': os.getenv('DB_HOST2'),
        'PORT': os.getenv('DB_PORT2'),
    }
}
```



### then run the migrations to setup the database and models:

- python manage.py makemigrations
- python manage.py migrate

### now to load the datas, (they are in the data_backup/ director): 


- python manage.py loaddata apiuser_data.json

- python manage.py loaddata apiuserprofile_data.json
-
-



---
everything should function correctly now.

ps : we run this API user app on -> python manage.py runserver 8080 
 

if need to restart the tables from zero :
```
TRUNCATE TABLE users_api_apiuser  RESTART IDENTITY CASCADE;
TRUNCATE TABLE users_api_apiuserprofile  RESTART IDENTITY CASCADE;
```

### TO access the API endpoints :


- to be authorized to use the API endpoints, you will need to add the Authorization header like so :
Authorization: Token <your_token>

- you can create a token in the admin panel. select a user and save. will generate a token for that user.


## API User Actions (API UserProfile follow the exact same logic)

- **Create User**
  - Endpoint: `/user/create/`
  - Method: `POST`

- **Create Many Users**
  - Endpoint: `/user/create_bulk/`
  - Method: `POST`
  
- **Get User**
  - Endpoint: `/user/get/<id>/`
  - Method: `GET`

- **Update User**
  - Endpoint: `/user/update/<id>/`
  - Method: `GET`
  
- **Delete User**
  - Endpoint: `/user/delete/<id>/`
  - Method: `DELETE`
