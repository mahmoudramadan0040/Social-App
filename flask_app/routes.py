from flask import render_template,redirect,request,url_for
from flask_app import bcrypt,login_manager,app,db
from flask_login import current_user,login_required,login_user,logout_user
from flask_app.models import User,Post
from flask_app.forms import PostFrom 
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


@app.route('/post/create',methods=['GET','POST'])
def create_post():
    form= PostFrom()
    if form.validate_on_submit():
        with app.app_context():
            new_post = Post(
                title=form.title.data,
                content =form.content.data,
                date_posted = form.date_posted.data,
                user_id=1
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
    
@app.route('/post/<int:id>')
def get_post(id):
    with app.app_content():
        post =Post.query.filter_by(id=id).first()
        if post:
            return render_template('',post=post)

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
        

