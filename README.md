# Flask_backend medic

Python 3.8.10

$ python3 -m venv .venv

$ source .venv/bin/activate

$ pip install -r requirements.txt

$ FLASK_APP="migrate" flask db init

$ FLASK_APP="migrate" flask db migrate

$ FLASK_APP="migrate" flask db upgrade

$ python3 run.py

# medic/settings.py

class Config:
    
    SECRET_KEY = 'your_key'
    CORS_ALLOWED_ORIGINS = ['http://localhost:8080']
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'mysql://username:password@HOST/DB_NAME'
    JSON_AS_ASCII = False