# How to run
### Step1: Install requirements
```
pip install -r requirements.txt
```
### Step 2
```
python manage.py makemigrations rango
```
### Step 3
```
python manage.py migrate
```
### Step 4: Populate Data
```
python populate_rango.py
```
### Step 5: Crate Super User
```
python manage.py createsuperuser
```
### Step 6 Run project:
```
python manage.py runserver 127.0.0.1:8000
```
