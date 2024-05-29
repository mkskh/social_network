## How to use api:
  
### Install django restframework
- pip instal djangorestframework  
  
### Create a superuser with admin level permissions

- python manage.py createsuperuser
- name : adminapi (it recognize admin already been taken) 
- password : testapi1234
- email : admin@mail2.com

### Creating the database:

- sudo su postgres
- psql

- place the following :

    - CREATE DATABASE api_user_social_network;

    - CREATE USER api_user_sn_admin WITH PASSWORD 'testapi1234';

    - ALTER DATABASE api_user_social_network OWNER TO api_user_sn_admin;

    - GRANT ALL PRIVILEGES ON DATABASE api_user_social_network TO api_user_sn_admin;
  
Make sure the database has been created  
  

### Load the data (in the data_backup/ folder): 
  
- python manage.py loaddata db_backup.json
  
For using the API in social network project use - python manage.py runserver 9000 
  

### TO access the API endpoints :


- to be authorized to use the API endpoints, you will need to add the Authorization header like so :
Authorization: Token <your_token>

- you can create a token in the admin panel. select a Token model - select a user - generate Token.


## API User Actions (API UserProfile follow the exact same logic)
  
USER:
  
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
  
PROFILE:
  
- **Create Profile**
  - Endpoint: `/profile/create/`
  - Method: `POST`

- **Create Many Profiles**
  - Endpoint: `/profile/create_bulk/`
  - Method: `POST`
  
- **Get Profile**
  - Endpoint: `/profile/get/<id>/`
  - Method: `GET`

- **Update Profile**
  - Endpoint: `/profile/update/<id>/`
  - Method: `GET`
  
- **Delete Profile**
  - Endpoint: `/profile/delete/<id>/`
  - Method: `DELETE`
