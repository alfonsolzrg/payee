# payee
Accounting app

## Installing and first run

Locally, you just need a sqlite db. Eventually, a PostgreSQL/MySQL server will be required.

- Install all requirements with ```pip install -r requirements```
- Copy the local.dist.py file to local.py ```cp settings/local.py.dist /settings.local.py```, change settings to reflect your local database installation
- Export local ENV variables: ```export DJANGO_SETTINGS_MODULE=payee.settings.local```
- Run migrations: ```python manage.py migrate```
- Start dev server: ```python manage.py runserver```

That's it!


## Deploying

You can use the provided Dockerfile to build an image and then run it using the container orchestration platform of your choice. 
Or, use plain old Docker ;)
