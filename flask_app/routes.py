from flask import render_template,redirect
from flask_app import bcrypt,login_manager,app
from flask_login import current_user,login_required,login_user,logout_user
#home endpoint
@app.route('/home')
@app.route('/')
def home():
    return "home"


#login endpoint
@app.route('/login')
def login():
    return "login"

# Register Endpoint
@app.route('/register')
def register():
    return "register"


#profile endpoint
@app.route('/profile')
def profile():
    return render_template('profile.html')



#friend requests endpoint
@app.route('/friendrequests')
def friend_requests():
    return "friend requests"