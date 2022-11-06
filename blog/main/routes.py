from flask import render_template, redirect, flash, url_for, request, Blueprint
from blog.models import database, Post, User
from blog.posts.forms import contact_form
main = Blueprint('main', __name__)


 #Home page for the blog mainlication
@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts=Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template('home.html', posts=posts)

#About us

@main.route('/about')
def about():
    return render_template('about.html')

#contact us
@main.route('/contact')
def contact():
    form = contact_form()
    if form.validate_on_submit():
        message_sent = User(first_name=form.first_name.data, email=form.email.data,
                    last_name=form.last_name.data, message=form.message.data)
        database.session.add(message_sent)
        database.session.commit()
        flash('Form submitted successfully', 'successs')
        return redirect(url_for('home'))
    return render_template('contact.html', title='Contact', form=form)
