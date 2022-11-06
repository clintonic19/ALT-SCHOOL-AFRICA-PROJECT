from flask import (render_template, redirect, flash, url_for, 
                   abort, request, Blueprint)
from flask_login import current_user, login_required
from blog import database
from blog.models import Post
from blog.posts.forms import Create_post, contact_form
posts = Blueprint('posts', __name__)


#Creating a new post in the  blog application

@posts.route('/post/new', methods=["POST", "GET"])
@login_required
def new_post():
    form = Create_post()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post created Successfully', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', legend='Create New Post',  form=form)


#Edit an existing post with the current user
@posts.route('/post/<int:post_id>')
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('edit_post.html', title=post.title, post=post)


#updating an existing post with the current user
@posts.route('/post/<int:post_id>/update', methods=["POST", "GET"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = Create_post()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        database.session.commit()
        flash('Post Updated Successfully!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', legend='Update Post', form=form)

#Delete a post
@posts.route('/post/<int:post_id>/delete', methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    database.session.delete(post)
    database.session.commit()
    flash('Post Deleted Successfully!', 'success')
    return redirect(url_for('main.home'))
