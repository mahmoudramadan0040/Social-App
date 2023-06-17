from flask import render_template,redirect
from flask_app import bcrypt,login_manager,app
from flask_login import current_user,login_required,login_user,logout_user
#home endpoint
@app.route('/home')
@app.route('/')
def home():
    return "hello world"


#login endpoint
@app.route('/login')
def login():
    pass

# Register Endpoint
@app.route('/register')
def register():
    pass


#profile endpoint
@app.route('/profile')
def profile():
    pass



#friend requests endpoint
@app.route('/friendrequests')
def friend_requests():
    pass