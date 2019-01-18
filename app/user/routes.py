from app.user import bp
from flask import render_template, flash, redirect, url_for, request, g, current_app, json
from flask_login import login_user, logout_user, current_user, login_required
from flask_babel import _, get_locale
from app import db
from app.main.forms import EditProfileForm, PostForm, LocationForm, NetworkForm,JournalForm, \
CustomerForm, Post_r_Form, StatisticForm, DeleteForm, InfoForm,RemoveForm,ScriptForm,TemplateForm,GetNetworksForm
from app.models import User, Post, Location, Customer, Network, Post_r, \
Statistic, Category, Subcategory, Info, Hardware,Script,Template,Journal
import os
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER_ENV')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'xlsx','cfg'])
ALLOWED_EXTENSIONS_PANDAS = set(['xlsx'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def allowed_file_pandas(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_PANDAS
    return True  






@bp.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    folder=os.environ.get('UPLOAD_FOLDER')+current_user.username
    filelist=[]
    for x in os.listdir(folder):
        filelist.append(x)
    

    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user.user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('user.user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part!')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file!')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(folder, filename))
            flash(_('File uploaded!'))
            
                
        return redirect(url_for('user.user',username=user.username, user=user,
                            filename=filename,filelist=filelist ))

    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url, filelist=filelist)





@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash(_('You cannot follow yourself!'))
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(_('You are following %(username)s!', username=username))
    return redirect(url_for('user.user', username=username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash(_('You cannot unfollow yourself!'))
        return redirect(url_for('user.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(_('You are not following %(username)s.', username=username))
    return redirect(url_for('user.user', username=username))