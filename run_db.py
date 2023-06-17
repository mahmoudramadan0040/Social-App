from flask_app import db,app
from flask_app.models import User, Post
import sys
#to create all tables
# Create Database
def create_db():
    with app.app_context():
        # you will have instance folder with site.db inside
        db.create_all()

#run this function to post dummy data
def post_user():
    with app.app_context():
        user1 = User(
            username = 'karim.Maged',
            email = 'karim@yahoo.com',
            password = '123456',
            photo = '/static/images/R.png'
            )
        db.session.add(user1)
        db.session.commit()

def post_post():
    with app.app_context():
        user1 = User.query.first()
        post1 = Post(
            title = 'This is the First test Post',
            content = 'This is a content for the first test post',
            user_id = user1.id
        )
        db.session.add(post1)
        db.session.commit()

def delete_db():
    with app.app_context():
        db.drop_all()

if __name__ == '__main__':
    globals()[sys.argv[1]]()
