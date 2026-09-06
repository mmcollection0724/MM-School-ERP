# MM School ERP

Django backend starter for the existing MM School ERP UI.

## Included in this first backend version
- Secure Django login/logout
- Server-side SQLite database
- Students with admission fields
- Teachers / Staff with search
- Expenses
- Notices
- Dashboard counts
- Nursery, Prep, 1st through 10th classes
- Same black/classy visual direction as the uploaded prototype

## Run locally
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/

For production, use PostgreSQL, HTTPS, environment variables, backups, and a real deployment server. Do not put passwords or client secrets in JavaScript.
