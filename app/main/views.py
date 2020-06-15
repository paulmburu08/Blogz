from flask_login import login_required
from flask import render_template,request,redirect,url_for,abort
from . import main
from ..models import User,Blog
from .forms import UpdateProfile,AddBlog
from .. import db,photos

@main.route('/')
@login_required
def index():

    title = 'BLOGZ'
    blogs = Blog.query.order_by(Blog.date.desc())

    return render_template('index.html', title = title, blogs = blogs)

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
        return redirect(url_for('main.index'))
        
    title = 'New Blog'
    return render_template('pitch_form.html', title= title,form = form)

@main.route('/category/<string:cat>')
@login_required
def category(cat):
    blogs = Blog.query.filter_by(category = cat).order_by(Blog.date.desc())
    return render_template('category.html', blogs = blogs)

@main.route('/blog/<int:id>/comments',methods = ['GET','POST'])
@login_required
def comments(id):
    blog = Blog.query.filter_by(id = id).first()
    pitch.upvote = 0
    pitch.downvote = 0
    form = AddComment()
    upvote = UpVote()
    downvote = DownVote()
    if form.validate_on_submit():
        comment = form.comment.data

        new_comment = Comments(comment = comment,pitch_id = pitch.id, user = current_user)

        new_comment.save_comment()
        return redirect(url_for('main.comments',id = pitch.id))

    if upvote.validate_on_submit() and upvote.upvote.data:
        pitch.upvote+=1
        db.session.commit()
        return redirect(url_for('main.comments',id = pitch.id))

    elif downvote.validate_on_submit() and downvote.downvote.data:
        pitch.downvote+=1
        db.session.commit()
        return redirect(url_for('main.comments',id = pitch.id))

    comments = Comments.query.filter_by(pitch_id = id).order_by(Comments.date.desc())
    title = 'Comments'
    return render_template('comments.html',pitch = pitch, title= title,form = form, comments = comments, upvote = upvote, downvote = downvote)

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