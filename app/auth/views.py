from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user, current_user

from . import auth
from .. import home
from forms import LoginForm, RegistrationForm
from .. import db
from ..models import User

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an employee in through the login form
    """

    form = LoginForm()
    if form.validate_on_submit():

        # check whether employee exists in the database and whether
        # the password entered matches the password in the database
        employee = User.query.filter_by(email=form.email.data).first()
        if employee is not None and employee.verifypassword(
                form.password.data):
            # log employee in
            login_user(employee)

            # redirect to the dashboard page after login
            if employee.role.name == "super_admin":
                return redirect(url_for('home.admin_companies'))
            elif employee.role.name == "admin":
                return redirect(url_for('home.admin_dashboard'))
            else:
                return redirect(url_for('home.dashboard'))


        # when login details are incorrect
        else:
            flash('Invalid email or password.')

    # load login template
    if current_user.is_authenticated:
        return redirect(url_for('home.profile'))
    else:
        return render_template('auth/login.html', form=form, title='Login')


@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('auth.login'))
