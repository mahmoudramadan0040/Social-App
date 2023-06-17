from flask_app import db,login_manager,bcrypt
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.Text, nullable = False)
    photo = db.Column(db.LargeBinary)
    friends = db.Column(ARRAY(db.Integer))
    posts = db.relationship('Post', backref='author', lazy=True, cascade='all,delete')
    
    def set_password(self,password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self,password):
        return bcrypt.check_password_hash(self.password,password)


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(50), nullable = False)
    content = db.Column(db.String(300))
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)