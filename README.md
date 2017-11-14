# Social API Implemented on Django

**Prerequisite**
* [pip-tools](https://pypi.python.org/pypi/pip-tools/)
* [conda](https://conda.io/docs/index.html)

**How-to**
1. Compile all dependencies `pip-compile -o requirements.txt requirements.in`
2. Install all dependencies `pip install -r requirements.txt`
3. Run migration `python manage.py migrate`
4. Test local server `python manage.py runserver`

---
Default database is using SQLite, but cause this using Django, change database is simple enough just change on settings with something like this:
```python
# MySQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'DB_NAME',
        'USER': 'DB_USER',
        'PASSWORD': 'DB_PASSWORD',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```
```python
# Postgres
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db_name',                      
        'USER': 'db_user',
        'PASSWORD': 'db_user_password',
        'HOST': '',
        'PORT': 'db_port_number',
    }
}
```

