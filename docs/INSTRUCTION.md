# Python Django Starter Bundle Instructions
## Description
This is readme and instructions how start using Django backend bundle from Akveo. Backend bundle is integrated solution of Django micro-framework and Angular Frontend code. Backend code plays mostly API role, giving data to the client side as REST API.
Backend part of Django Starter Bundle is based on modern python framework [Django](https://www.djangoproject.com/) framework.
[Django Documentation](https://docs.djangoproject.com/en/2.2/) helps with understanding of Django principles.

# Running Instructions
Application requires a database to correctly run. In development by default Sqlite database is used, which is stored at `db.sqlite3`. If you would like to use other database in development mode, change DATABASES section in the setting.py file e.g.:
    'default': {
        'NAME': 'user_data',
        'ENGINE': 'django.db.backends.postgresql',
        'USER': 'postgres_user',
        'PASSWORD': 'password'
    }


### Running the backend
0) Install python 3. You can find [here](https://realpython.com/installing-python/) instructions for your operation system.
1) Change directory to the *backend* folder `cd backend/bundle_django`
2) Create virtualenv `virtualenv -p python3 bundle_env`
3) Activate virtualenv `source bundle_env/bin/activate`
4) Install required python modules `pip install -r requirements.txt`
5) Only during the initial launch create database schema for your application `python manage.py makemigrations api` and `python manage.py migrate`
6) Set your project secret key to `DJANGO_SECRET_KEY` environment variable
7) Run the application `python manage.py runserver 0.0.0.0:3001`

That's it! Now your application is running at port 3001 and you can access it by typing `http://localhost:3001/` in your browser.

### Running Angular front end
Before running Angular you need to have node installed 
0) Install nodejs. You can download it using you operating system package manager or from [here](https://nodejs.org/en/download/).
1) Go to the *front end* folder `cd frontend`
2) Run commands `npm install` and `npm start`
3) Open `http://localhost:4200` in your browser
4) create new user using interface and start working with app

## Issue tracking
You can post issues and see sample materials at [GitHub Support Repository](https://github.com/akveo/ngx-admin-bundle-support/issues)

### Other Commands
```bash
# development
$ npm run start
# development with watch mode - code will be rebuild after each change. it runs `nodemon` module to watch over changes and re-run node api automatically. 
$ npm run start:dev
# build dist for prod deployment
$ npm run build
# production mode
$ npm run start:prod
```

## Test
```bash
# unit tests
$ npm run test
# e2e tests
$ npm run test:e2e
# test coverage
$ npm run test:cov
```

## Style Check
```bash
# lint
$ npm run lint
```

## Features
 - Django framework, feature based modules
 - Compatible with ngx-admin out of the box
 - JWT authentication using rest_framework module
 - PostgreSQL, MySQL, Oracle, Microsoft SQL Server, and SQLite can be used as databases
 - SQLite is used as database toolkit for data CRUD operations
 - Compression setup for API
 - Logging to console
 - 6 months free updates
 
## Basic Code Structure
Code is organized in following structure
 - Main Folder
    - frontend // Contains all UI code
    - backend // Contains server side Django code
        - api // This is where all project files located
            - apps.py // Contains a registry of installed applications
            - migrations // Contains created DB schemas
            - auth // Auth module and code there
                - views.py // Contains view for auth pages
            - user // User module and code there
                - controller.py // Contains handlers for user commands
                - views.py // Contains view for user pages
            - common.py // Contains common functions
            - email.py // Contains code that sends emails
            - models.py // Contains table and rows for DB
            - urls.py // Url manager for API application
        - bundle_django // Main django application settings
            - settings.py // Django configuration file
            - urls.py // Url manager
            - wsgi.py // Web Server Gateway Interface
        - configs // Folder with configuration files
            - base_config.json // Configuration file
        - manage.py // application runner     
    - docs // documentation and licenses

## Support
Please post issues in [Bundle Support Issue Tracker](https://github.com/akveo/ngx-admin-bundle-support/issues)

## License
Django bundle is provided under Single Application or Multi Application license. Please find details in License files.
