from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config['SECRET_KEY']=os.urandom(16).hex()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

database_url=os.environ.get('DATABASE_URL')

if not database_url:
	database_url='sqlite:///conversations.db'
elif 'postgres://' in database_url:
	database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI']=database_url

db = SQLAlchemy(app)

from website import routes
