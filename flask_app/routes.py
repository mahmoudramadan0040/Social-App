from flask import render_template,redirect,request,url_for,flash
from flask_app import bcrypt,login_manager,app,db
from flask_login import current_user,login_required,login_user,logout_user
from flask_app.models import User,Post
from flask_app.forms import PostFrom,Registration,LoginForm
from werkzeug.utils import secure_filename
import os


#home endpoint
@app.route('/home')
@app.route('/')
@login_required
def home():
    return "home"


#login endpoint
@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    context = {'form': form}
    if form.validate_on_submit():
        with app.app_context():
            user = User.query.filter_by(email = form.email.data).first()
            if user:
                    if user.check_password(form.password.data):
                        login_user(user)
                        flash("Login Successful!","success")
                        return redirect(url_for('profile'))
            else:
                flash("Login Unsuccessful!","danger")
                return redirect(url_for('login'))
    return render_template('login.html',**context)

# Register Endpoint
@app.route('/register',methods=['GET','POST'])
def register():
    form = Registration()
    context = {'form':form}
    if form.validate_on_submit():
        with app.app_context():
            photo = form.photo.data
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            photo_path = f"/static/images/{filename}"
            new_user = User(username = form.username.data,
                            password = form.password.data,
                            email = form.email.data,
                            photo = photo_path )
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash(f"Registration Successful for {form.username.data}!","success")
            return redirect(url_for('login'))
    return render_template('registration.html',**context)


#profile endpoint
@app.route('/profile',methods = ['GET','POST'])
@login_required
def profile():
    test_user = User.query.filter_by( email = current_user.email).first()
    test_post = Post.query.filter_by(user_id = test_user.id).all()
    context = {'user':test_user, 'posts':test_post}
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        privacy = request.form['privacy']
        with app.app_context():
            post = Post(
                title = title,
                content = content,
                user_id = test_user.id,
                privacy = privacy
            )
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('profile'))
    return render_template('profile.html', **context)



#friend requests endpoint
@app.route('/friendrequests')
def friend_requests():
    return "friend requests"


@app.route('/post/create',methods=['GET','POST'])
def create_post():
    form= PostFrom()
    if form.validate_on_submit():
        with app.app_context():
            new_post = Post(
                title=form.title.data,
                content =form.content.data,
                date_posted = form.date_posted.data,
                user_id=1,
            )
            db.session.add(new_post)
            db.session.commit()
        return redirect(url_for('home'))
    return render_template('posts/create.html',data={'form':form})
            
@app.route('/posts',methods=['GET'])
def list_post():
    with app.app_context():
        posts =Post.query.all()
        print(posts)
    return render_template('posts/list.html',posts=posts)
    
# @app.route('/post/<int:id>')
# def get_post(id):
#     with app.app_content():
#         post =Post.query.filter_by(id=id).first()
#         if post:
#             return render_template('',post=post)

@app.route('/post/<int:id>/update',methods=['GET','POST'])  
def update_post(id):
    post= Post.query.filter_by(id=id).first()
    if post:
        form= PostFrom(obj=post)
        if form.validate_on_submit():
            form.populate_obj(post)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('home'))
        return render_template('posts/create.html', data={'form':form})
    else:
        return "Post not exists to update !"

# @app.route('/post/<int:id>/delete',methods=['GET','POST'])
# def delete_post(id):
#     post =Post.filter_by(id=id).first()
#     if request.method == 'POST' :
        

