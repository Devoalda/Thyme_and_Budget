> [NOTE] Commands may differ depending on OS

# Cd to project
`cd Backend`

# (Optional) Create venv
`python -m venv venv`

## For Linux
`source venv/bin/activate`

## For Windows
`venv\Scripts\activate`

# Install libraries if not done so
`pip3 install -r requirements.txt`

# Run migrations
`python manage.py migrate`

# Make migrations
`python manage.py makemigrations`

`python manage.py migrate`

# Run server
`python manage.py runserver`

# Endpoints to test

Register:
`http://127.0.0.1:8000/account/register`

Login:
`http://127.0.0.1:8000/api/token/`