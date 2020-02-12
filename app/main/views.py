from flask import render_template,request, redirect, url_for,abort
from . import main
from flask_login import login_required, current_user
from ..models import Pitch, Comment, Types,User
from .forms import PitchForm, CommentsForm,UpdateProfile
from ..import db,photos


@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''

    types = Types.get_categories()

    title = 'Pitch up your Pitch'
    return render_template('index.html', types=types, title=title)


@main.route('/category/<int:id>')
def single_type(id):
    '''
    A view function that will return the pitches on a specific kind of view
    '''

    types = Types.query.get(id)
    title = f'{types.name} pitches'
    pitches = Pitch.get_pitches(types.id)

    return render_template('type.html', title=title, types=types, pitches=pitches)


@main.route('/category/pitch/new/<int:id>', methods=["GET", "POST"])
@login_required
def pitch_new(id):
    '''
    view function that helps renders theform to create a new pitch
    '''

    form = PitchForm()
    types = Types.query.filter_by(id=id).first()
    if form.validate_on_submit():
        pitch = form.pitch.data
        title = form.title.data

        new_pitch = Pitch(type_id=types.id, title=title, pitch=pitch, user=current_user)
        new_pitch.save_pitch()
        return redirect(url_for('.single_type', id=types.id))

    title = f'{types.name} pitches'
    return render_template('add_pitch.html', title=title, pitch_form=form, types=types)


@main.route('/comments/new/<int:id>', methods=["GET", "POST"])
@login_required
def comment(id):
    '''
    view function that return a form to comment on a given pitch
    '''

    form = CommentsForm()
    pitch = Pitch.query.filter_by(id=id).first()
    if form.validate_on_submit():
        comment = form.comment.data
        new_comment = Comment(
            pitch_id=pitch.id, comment_post=comment, user=current_user)
        new_comment.save_comments()

        return redirect(url_for('.comments', id=pitch.id))
    title = f'{pitch.title} comments'
    return render_template('new_comment.html', title=title, comment_form=form, pitch=pitch)


@main.route('/comments/<int:id>')
def comments(id):
    pitch = Pitch.query.get(id)
    comment = Comment.get_comments(pitch.id)
    title = f'{pitch.title} comments'
    print(comment)

    return render_template('comments.html', title=title, pitch=pitch, comment = comment)
 

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    types = Types.query.all()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user,types = types)


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

@main.route('/user/pitches/<int:id>')
def mypitches(id):
    
    users = User.query.get(id)
    title = f'{users.username} pitches'
    pitches = Pitch.get_pitches_user(users.id)
    
    return render_template('mypitches.html',title=title,pitches=pitches)
    
    