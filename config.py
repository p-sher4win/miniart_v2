import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask app configs
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG')
    FLASK_ENV = os.environ.get('FLASK_ENV')
    FLASK_APP = os.environ.get('FLASK_APP')
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # Firebase init configs
    FIREBASE_CRED_PATH = os.environ.get('FIREBASE_CRED_PATH')
    FIREBASE_API_KEY = os.environ.get('FIREBASE_API_KEY')
    FIREBASE_AUTH_DOMAIN = os.environ.get('FIREBASE_AUTH_DOMAIN')

    # Mongo db congigs
    MONGO_URI = os.environ.get('MONGO_URI')     # dev use only (remove for prod)
    # MONGO_PASS = os.environ.get('MONGO_PASS')
    # MONGO_URI = f'mongodb+srv://bravestorm:{MONGO_PASS}@miniart-cluster.jb3svne.mongodb.net/?appName=miniart-cluster'
    ADMIN_EMAIL=os.environ.get('ADMIN_EMAIL')
    ADMIN_PASS=os.environ.get('ADMIN_PASS')
