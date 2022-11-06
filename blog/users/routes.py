from flask import (render_template, redirect, flash, url_for, 
                   abort, request, Blueprint)
from flask_login import login_user, current_user, logout_user, login_required
from blog import database, bcrypt
from blog.models import User, Post
from blog.users.forms import (Registration_form, Login_form, Profile_update, Reset_request, Password_reset )
from blog.users.utils import save_profile_pics, reset_email

users = Blueprint('users', __name__)

#Register new users
@users.route("/register", methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = Registration_form()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password = hashed_password)
        database.session.add(user)
        database.session.commit()
        flash('Account Created Successfully, Please log in now!' ,'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


#Authenticate and log users in 
@users.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home')) 
    form = Login_form()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data )
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check Email and Password', 'danger')
    return render_template('login.html', title='Login', form=form)


#Log users out
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


#users profiles update     
@users.route('/profile', methods=["POST", "GET"])
@login_required
def profile():
    form = Profile_update()
    if form.validate_on_submit():
        if form.profile_pics.data:
            picture_file = save_profile_pics(form.profile_pics.data)
            current_user.image_file = picture_file        
        current_user.username = form.username.data
        current_user.email = form.username.data
        database.session.commit()
        flash('Profile Updated Successfully!', 'success')
        return redirect(url_for('users.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_images/' + current_user.image_file)
    return render_template('profile.html', title='Profile', image_file=image_file, form=form)


#Authentication to check numbers of post by a user and pagination
@users.route("/user/<string:username>")
def users_post(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('users_post.html', posts=posts, user=user)


#request token from users when they forget their passwords
@users.route('/reset_password', methods=["POST", "GET"])
def reset_request(): 
    if current_user.is_authenticated:
        return redirect(url_for('home')) 
    form = Reset_request()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        reset_email(user)
        flash('Authentication Email sent', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title ='Reset Password', form=form)

#reset users password
@users.route('/reset_password/<token>', methods=["POST", "GET"])
def reset_token(): 
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.reset_verified_token()
    if user is None:
        flash('Invalid or Expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = Password_reset()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        database.session.commit()
        flash('Password Changed Successfully, Please log in now!' ,'success')
        return redirect(url_for('users.login')) 
    return render_template('reset_token.html', title ='Reset Password', form=form)
    