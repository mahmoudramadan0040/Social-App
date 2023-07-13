from flask import render_template,redirect,request,url_for,flash
from sqlalchemy import and_
from flask_app import bcrypt,login_manager,app,db
from flask_login import current_user,login_required,login_user,logout_user
from flask_app.models import User,Post,FriendRequests
from flask_app.forms import PostFrom,Registration,LoginForm,EditUserForm
from werkzeug.utils import secure_filename
import os


#home endpoint
@app.route('/home')
@app.route('/')
# @login_required
def home():
    with app.app_context():
        if current_user.is_authenticated: 
            if current_user.friends:
                posts = db.session.query(User, Post)\
                    .outerjoin(User, User.id == Post.user_id)\
                    .filter(and_(Post.user_id.in_(current_user.friends), Post.privacy.in_(["1","0"]))).all()
                friends = User.query.filter(User.id.in_(current_user.friends) ).all()
                print(friends)
            else:
                posts = []
                friends=[]

        else :
            posts = db.session.query(
            Post,
            User
            )\
            .join(User, Post.user_id == User.id and Post.privacy=='0')\
            .all();
            friends=[]
            print(posts)
            
        
    return render_template('home.html' ,posts=posts,friends=friends)


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
    requests = FriendRequests.query.filter_by(reciever = current_user.id).all()
    senders = User.query.join(FriendRequests, User.id.in_([req.sender for req in requests])).all()
    return render_template('friendrequests.html',requests = senders)


@app.route('/post/create',methods=['GET','POST'])
def create_post():
    form= PostFrom()
    if form.validate_on_submit():
        with app.app_context():
            new_post = Post(
                title=form.title.data,
                content =form.content.data,
                date_posted = form.date_posted.data,
                user_id=current_user.id,
                privacy = form.privacy.data
            )
            db.session.add(new_post)
            db.session.commit()
        return redirect(url_for('home'))
    return render_template('posts/create.html',data={'form':form})
            
@app.route('/posts',methods=['GET'])
@login_required
def list_post():
    with app.app_context():
        posts = db.session.query(
            Post,
            User
            )\
            .join(User, Post.user_id == User.id and Post.privacy=='0')\
            .all();
    return render_template('home.html',posts=posts)
    
# @app.route('/post/<int:id>')
# def get_post(id):
#     with app.app_content():
#         post =Post.query.filter_by(id=id).first()
#         if post:
#             return render_template('',post=post)

@app.route('/post/update/<int:id>', methods=['GET','POST'])  
def update_post(id):
    post= Post.query.filter_by(id=id).first()
    if post:
        form= PostFrom(obj=post)
        if form.validate_on_submit():
            form.populate_obj(post)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('profile'))
        return render_template('/posts/create.html', data={'form':form})
    else:
        return "Post does not exists to update !"

# @app.route('/post/<int:id>/delete',methods=['GET','POST'])
# def delete_post(id):
#     post =Post.filter_by(id=id).first()
#     if request.method == 'POST' :
        

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/delete/post/<int:id>', methods=['GET','POST'])
def delete(id):
    if request.method == 'POST':
        post = Post.query.filter_by(id = id).first()
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('profile'))
    return render_template('delete.html')


@app.route('/explore')
@login_required
def explore():
    if current_user.friends:
        users = User.query.filter(User.id != current_user.id)\
        .filter(User.id.not_in(current_user.friends)).all()
    else:
         users = User.query.filter(User.id != current_user.id).all()
    return render_template('explore.html',users = users)

@app.route('/add/friend/<int:id>')
@login_required
def addFriend(id):
    exist = FriendRequests.query.get((current_user.id, id))

    if exist:
        flash(f"You already sent friend request","danger")
        return redirect(url_for('explore'))
    else:
       with app.app_context():
            request = FriendRequests(sender = current_user.id,reciever = id)
            db.session.add(request)
            db.session.commit()
            flash("firent request was send successfully","success")
            return redirect(url_for('explore'))               
    
@app.route('/accept/<int:id>')
@login_required
def accept(id):
    with app.app_context():
        sender = FriendRequests.query.get((id,current_user.id))
        print(sender);
        print(id);
        print(current_user.id);
        if not current_user.friends:
           current_user.friends = [] 
           current_user.friends.append(id)
        else:
           current_user.add_friend(id)
           db.session.add(current_user)
           db.session.commit()
        db.session.delete(sender)
        db.session.commit()
        return redirect(url_for('friend_requests'))
    
@app.route('/ignore/<int:id>')
@login_required
def ignore(id):
    with app.app_context():
        sender = FriendRequests.query.get((id,current_user.id))
        db.session.delete(sender)
        db.session.commit()
        return redirect(url_for('friend_requests'))
    
@app.route('/edit',methods = ['GET','POST'])
@login_required
def edit():
    form = EditUserForm(obj = current_user)
    if form.validate_on_submit():
        with app.app_context():
            photo = form.photo.data
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            photo_path = f"/static/images/{filename}"
            current_user.username = form.username.data
            current_user.photo = photo_path
            db.session.add(current_user)
            db.session.commit()
            return redirect(url_for('profile'))
    return render_template('edit.html',form = form)