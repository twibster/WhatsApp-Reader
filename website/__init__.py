from flask import Flask,render_template
import os

app = Flask(__name__)
app.config['SECRET_KEY']=os.urandom(16).hex()

from website import routes
