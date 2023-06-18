# importing flask,bcrypt
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


#create an instance of flask
app = Flask(__name__)
# the secret key
app.config['SECRET_KEY'] = 'W9MZ9FbVYKXHPDVqpvtkl1i16dnU3MWr'

#setting up the bcrypt
bcrypt = Bcrypt(app)

#setting an upload folder
UPLOAD_FOLDER = '/home/karim/ITI/18-Flask/Flask_social_media/flask_app/static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#setting up the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:18501900@localhost:5432/flask_db'
db = SQLAlchemy(app)

# setting up LoginManager
login_manager = LoginManager(app)
# importing the routes
from flask_app import routes,models