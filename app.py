from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import *
from forms import *
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)

toolbar = DebugToolbarExtension(app)


@app.route('/')
def home_page():
    if "user_id" not in session:
        return redirect('/register')
    user = User.query.get_or_404(session['user_id'])
    return redirect(f'/users/{user.username}')


@app.route('/register', methods=["GET", "POST"])
def register():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(
            username, password, email, first_name, last_name)

        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken.  Please pick another')
            return render_template('register.html', form=form)
        session['user_id'] = new_user.id
        flash('Welcome! Successfully Created Your Account!', "success")
        return redirect(f'/users/{new_user.username}')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome Back, {user.username}!", "primary")
            session['user_id'] = user.id
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Invalid username/password.']

    return render_template('login.html', form=form)


@app.route('/users/<username>')
def user_page(username):
    if "user_id" not in session:
        flash("Please login first!", "danger")
        return redirect('/')
    user = User.query.get_or_404(session['user_id'])
    if user.username != username:
        flash("Not your Page Buster!", "danger")
        return redirect('/')

    all_feedback = Feedback.query.filter(
        Feedback.username == user.username).all()
    return render_template('user.html', user=user, feedback=all_feedback)


@app.route('/users/<username>/feedback/add', methods=["GET", "POST"])
def add_feedback(username):
    form = FeedbackForm()
    if "user_id" not in session:
        flash("Please login first!", "danger")
        return redirect('/')
    user = User.query.get_or_404(session['user_id'])
    if user.username != username:
        flash("Not your Page Buster!", "danger")
        return redirect('/')
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        username = user.username
        new_feedback = Feedback(
            title=title, content=content, username=username)
        db.session.add(new_feedback)
        db.session.commit()
        flash('Feedback Created!', 'success')
        return redirect(f'/users/{user.username}')

    return render_template('addFeedback.html', form=form, user=user)


@app.route('/logout')
def logout_user():
    session.pop('user_id')
    flash("Goodbye!", "info")
    return redirect('/')


@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    if "user_id" not in session:
        flash("Please login first!", "danger")
        return redirect('/')
    user = User.query.get_or_404(session['user_id'])
    if user.username != username:
        flash("Not your Page Buster!", "danger")
        return redirect('/')
    db.session.delete(user)
    db.session.commit()

    session.pop('user_id')
    flash("Goodbye Forever!!", "info")
    return redirect('/')


@app.route('/feedback/<int:id>/update', methods=['GET', 'POST'])
def edit_fb(id):
    if "user_id" not in session:
        flash("Please login first!", "danger")
        return redirect('/')
    user = User.query.get_or_404(session['user_id'])

    fb = Feedback.query.get_or_404(id)
    form = FeedbackForm(obj=fb)
    if user.username != fb.username:
        flash("Not your Page Buster!", "danger")
        return redirect('/')

    if form.validate_on_submit():
        fb.title = form.title.data
        fb.content = form.content.data
        db.session.commit()
        return redirect(f'/users/{user.username}')
    else:
        return render_template('editFeedback.html', form=form)


@app.route('/feedback/<int:id>/delete', methods=['POST'])
def delete_fb(id):
    if "user_id" not in session:
        flash("Please login first!", "danger")
        return redirect('/')
    user = User.query.get_or_404(session['user_id'])

    fb = Feedback.query.get_or_404(id)
    form = FeedbackForm(obj=fb)
    if user.username != fb.username:
        flash("Not your Page Buster!", "danger")
        return redirect('/')
    db.session.delete(fb)
    db.session.commit()

    flash("No more Feedback!!", "info")
    return redirect(f'/users/{user.username}')
