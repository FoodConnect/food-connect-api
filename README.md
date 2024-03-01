# food-connect-api

API Backend built with Django REST Framework

### Installation

Navigate to your desired directory and use the following command to clone down...

```
git clone https://github.com/FoodConnect/food-connect-api.git
```

change directories to the new clone...

```
cd food-connect-api
```

Install Python3 with HomeBrew

```
brew install python3
```

then create virtual environment.

```
python3.11 -m venv venv
```

Activate your virtual enviornment with

```
source venv/bin/activate
```

If you don't have Pip3 installed, install it with

```
brew install pip3
```

Otherwise upgrade with

```
pip install --upgrade pip
```

and install Django and Django REST Framework with

```
pip install django djangorestframework
```

as well as the django-cors-headers dependency with

```
pip install django-cors-headers
```

### Connecting to PostgreSQL Database

Install PostgreSQL with Homebrew with

```
brew install postgresql
```

then start the the PostgreSQL Service with

```
brew services start postgresql
```

Create a root user by logging into the PostgreSQL service with

```
psql postgres
```

and creating user credentials with

```
CREATE ROLE yourNewUsername WITH LOGIN PASSWORD ‘yourpassword’;
ALTER ROLE yourNewUsername CREATEDB;
```

Then, create your database with

```
CREATE DATABASE your_database_name;
```

and quit the session with

```
\q
```

To link your database to a postgresql database, first install 'psycopg2' module in your virtual environment to get Python to operate with Postgres:

```
pip install psycopg2
```

Create a database in your Postgres server. Then alter the following code in your settings.py file of your project:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'HOST': 'localhost',  # Or your database host
        'PORT': '',            # Leave it blank for default port
    }
}
```

Run the following commands to execute migrations:

```
python3.11 manage.py makemigrations
python3.11 manage.py migrate
```

### Usage

To start a local server, run the following command.

```
python3 manage.py runserver 8080
```

## Authors

<p>
<a href="https://github.com/perrileah">Leah Perri</a>
<br/>
<a href="https://github.com/kyle-pazdel">Kyle Pazdel</a>
</p>
