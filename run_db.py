from flask_app import db,app
from flask_app.models import User
import sys
#to create all tables
# Create Database
def create_db():
    with app.app_context():
        # you will have instance folder with site.db inside
        db.create_all()

        
if __name__ == '__main__':
    globals()[sys.argv[1]]()

