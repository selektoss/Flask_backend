import flask
from medic.settings import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from medic import create_app
from medic.models import db

app = create_app()
Migrate(app, db, directory="migrations")