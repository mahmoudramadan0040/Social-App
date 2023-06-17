from flask import render_template,redirect,request,url_for
from flask_app import bcrypt,login_manager,app,db
from flask_login import current_user,login_required,login_user,logout_user
from flask_app.models import User,Post
from PIL import Image
from io import BytesIO
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
@app.route('/profile',methods = ['GET','POST'])
def profile():
    test_user = User.query.first()
    test_post = Post.query.filter_by(user_id = test_user.id).all()
    context = {'user':test_user, 'posts':test_post}
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        with app.app_context():
            post = Post(
                title = title,
                content = content,
                user_id = test_user.id
            )
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('profile'))
    return render_template('profile.html', **context)



#friend requests endpoint
@app.route('/friendrequests')
def friend_requests():
    return "friend requests"


