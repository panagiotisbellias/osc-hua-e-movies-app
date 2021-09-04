# e-movies-app
E-Movies App, a Django project in the context of HUA DIT course 'Basic DevOps Concepts and Tools'

## Clone and run project
```bash
git clone https://github.com/panagiotisbellias/e-movies-app 
python3 -m venv myvenv
source myvenv/bin/activate
pip install -r requirements.txt
cd movies_app
cp movies_app/.env.example movies_app/.env
```
edit movies_app/.env file to define
```vim
SECRET_KEY='test123'
DATABASE_URL=sqlite:///./db.sqlite3
ALLOWED_HOSTS=127.0.0.1,localhost
```
## database migration and superuser creation
```bash
python manage.py migrate
python manage.py createsuperuser # answer to the prompts to make your admin profile with a valid email address
```
## run development server
```bash
python manage.py runserver
```
## alternatively, run application server we have installed via pip
```bash
gunicorn --bind 0.0.0.0:8000 movies_app.wsgi:application
```