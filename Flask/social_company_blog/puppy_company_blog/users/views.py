from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, login_required, current_user, logout_user

from puppy_company_blog import db
from puppy_company_blog.users.forms import LoginForm, RegistrationForm, UpdateUserForm
from puppy_company_blog.models import User, BlogPost
from puppy_company_blog.users.picture_handler import add_profile_pic

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    form = LoginForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        
        flash("Thanks for Registration!")

        return render_template(url_for('user.login'))

    return render_template('register.html', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data)
        if User.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Login Success')

            next = request.args.get('next')

            if next == None or not next[0] =='/':
                next = url_for('core.index')
            return redirect(next)

    return render_template('login.html', form=form)


# Accound update form
@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateUserForm()

    if form.validate_on_submit:

        # Picture upload.
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data, username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        
        db.session.commit()
        flash('User account Updated')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static', filename='profile_pics/'+current_user.profile_image)
    return render_template('acccount.html', profile_image=profile_image, form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect( url_for('core.index'))

