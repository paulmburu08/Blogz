from flask_login import login_required,current_user
from flask import render_template,request,redirect,url_for,abort,flash
from . import main
from ..models import User,Blog,Comments,Subscribe
from .forms import UpdateProfile,AddBlog,AddComment,AddSubscribers
from .. import db,photos
from ..email import mail_message
from ..requests import get_quotes

@main.route('/')
@login_required
def index():

    quotes = get_quotes()
    title = 'BLOGZ'
    blogs = Blog.query.order_by(Blog.date.desc())

    return render_template('index.html',quotes = quotes, title = title, blogs = blogs)

@main.route('/newblog',methods = ['GET','POST'])
@login_required
def new_blog():

    form = AddBlog()
    if form.validate_on_submit():
        title = form.title.data
        blog = form.blog.data
        category = form.category.data

        new_blog = Blog(title = title, blog = blog,category = category, user = current_user)

        new_blog.save_blog()

        mail_list = []
        subscribers = Subscribe.query.order_by(Subscribe.id.desc())
        for subscriber in subscribers:
            mail_list.append(subscriber.email)

        for mail in mail_list:
             mail_message("NEW POST!","email/new_post",mail,mail =mail)

        return redirect(url_for('main.index'))
        
    title = 'New Blog'
    return render_template('new_post.html', title= title,form = form)

@main.route('/category/<string:category>')
@login_required
def category(category):
    blogs = Blog.query.filter_by(category = category).order_by(Blog.date.desc())
    return render_template('category.html', blogs = blogs)

@main.route('/category/<string:category>/category/<int:id>/comments',methods = ['GET','POST'])
@login_required
def cat_comments(id,category):
    blog = Blog.query.filter_by(id = id).first()
    form = AddComment()
    if form.validate_on_submit():
        comment = form.comment.data

        new_comment = Comments(comment = comment,blog_id = blog.id, user = current_user)

        new_comment.save_comment()
        return redirect(url_for('main.cat_comments',id = blog.id,category= blog.category))

    comments = Comments.query.filter_by(blog_id = id).order_by(Comments.date.desc())
    title = 'Comments'
    return render_template('comments.html',blog = blog, title= title,form = form, comments = comments)

@main.route('/category/<string:category>/category/<int:id>/comments/update',methods = ['GET','POST'])
@login_required
def update_cat_post(id,category):
    title = 'Update post'
    blog = Blog.query.filter_by(id = id).first()
    if blog.user != current_user:
        abort(403)
    form = AddBlog()
    if form.validate_on_submit():
        blog.blog = form.blog.data
        blog.title = form.title.data
        db.session.commit()
        return redirect(url_for('main.category',id = blog.id,category= blog.category))

    elif request.method =='GET': 
        form.title.data = blog.title
        form.blog.data = blog.blog
    return render_template('new_post.html', title=title ,form = form)

@main.route('/blog/<int:id>/comments',methods = ['GET','POST'])
@login_required
def comments(id):
    blog = Blog.query.filter_by(id = id).first()
    form = AddComment()
    if form.validate_on_submit():
        comment = form.comment.data

        new_comment = Comments(comment = comment,blog_id = blog.id, user = current_user)

        new_comment.save_comment()
        return redirect(url_for('main.comments',id = blog.id))

    comments = Comments.query.filter_by(blog_id = id).order_by(Comments.date.desc())
    title = 'Comments'
    return render_template('comments.html',blog = blog, title= title,form = form, comments = comments)

@main.route('/blog/<int:id>/comments/update',methods = ['GET','POST'])
@login_required
def update_post(id):
    title = 'Update post'
    blog = Blog.query.filter_by(id = id).first()
    if blog.user != current_user:
        abort(403)
    form = AddBlog()
    if form.validate_on_submit():
        blog.blog = form.blog.data
        blog.title = form.title.data
        db.session.commit()
        return redirect(url_for('main.index',id = blog.id))

    elif request.method =='GET': 
        form.title.data = blog.title
        form.blog.data = blog.blog
    return render_template('new_post.html', title=title ,form = form)

@main.route('/blog/<int:id>/comments/delete',methods = ['POST'])
@login_required
def delete_post(id):
    blog = Blog.query.filter_by(id = id).first()
    if blog.user != current_user:
        abort(403)
    db.session.delete(blog)
    db.session.commit()
    return redirect(url_for('main.index',id = blog.id))

@main.route('/category/<string:category>/category/<int:id>/comments/delete',methods = ['POST'])
@login_required
def delete_cat_post(id,category):
    blog = Blog.query.filter_by(id = id).first()
    if blog.user != current_user:
        abort(403)
    db.session.delete(blog)
    db.session.commit()
    return redirect(url_for('main.category',id = blog.id, category = blog.category))

@main.route('/blog/<int:id>/comments/deletecomment/<int:comment_id>',methods = ['POST'])
@login_required
def delete_comment(comment_id,id):
    blog = Blog.query.filter_by(id = id).first()
    comment = Comments.query.filter_by(id = comment_id).first()
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('main.comments',id = blog.id))

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/subscribe',methods = ['GET','POST'])
def subscribe():
    form = AddSubscribers()

    if form.validate_on_submit():
        subscriber = form.email.data

        new_subscriber = Subscribe(email = subscriber)

        new_subscriber.save_subscriber()

        mail_list = []
        mail_list.append(new_subscriber.email)

        for mail in mail_list:
            mail_message('Subscription to Blogz.','email/new_subscriber',mail,subscribe=subscribe)

        return redirect(url_for('main.index'))

    return render_template('subscribe.html',form = form)