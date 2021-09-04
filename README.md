# e-movies-app
E-Movies App, a Django project in the context of HUA DIT course 'Basic DevOps Concepts and Tools'

## Clone and run project locally
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
ALLOWED_HOSTS=localhost
```
## Database migration
```bash
python manage.py makemigrations && python manage.py migrate
```
## Run development server
```bash
python manage.py runserver
```
## Alternatively, run gunicorn application server
```bash
gunicorn --bind 0.0.0.0:8000 movies_app.wsgi:application
```