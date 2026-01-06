# PetCare
### Desciprion
This project is designed for families to manage pets and shared responsibilities. It allows multiple family members to collaborate by creating, updating, and deleting users and pets, scheduling health events and activities, and tracking their statuses.

## Getting Started
### Dependencies
-   Python
-   pip 
-   Virtual environment tool 
-   SQLite or PostgresSql
### Installing

1.  Clone the repository
```
git clone https://github.com/illa-j/PetCare.git
```

2.  Create and activate virtual environment
```
python -m venv venv
source venv/bin/activate  
# On Windows: venv\Scripts\activate
```
3.  Install required packages
```
pip install -r requirements.txt
```

4.  Set up environment variables
```
cp .env.sample .env
# Edit .env with your configuration
```
5.  Run migrations
```
python manage.py migrate
```

6.  Create superuser (optional)
```
python manage.py createsuperuser
```

### Executing program

1.  Start the development server
```
python manage.py runserver
```
2.  Access the application at `http://127.0.0.1:8000/`
3.  Access admin panel at `http://127.0.0.1:8000/admin/`

## Help
Common issue and solution:
-   **Migration errors**: Make sure all migrations are applied
```
python manage.py makemigrations
python manage.py migrate
```
