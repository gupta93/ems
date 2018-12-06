from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import login_required, current_user

from . import home
from .. import db

from ..admin.forms import UserEditForm, InviteEditForm
from ..models import User, Invites, Company, Mapping, Role

@home.route('/')
def homepage():

    return render_template('home/index.html', title='Welcome to Squad Master')


@home.route('/dashboard')
@login_required
def dashboard():
    return render_template('home/dashboard.html', title='Dashboard')


@home.route('/admin/companies')
@login_required
def admin_companies():
    if not current_user.is_super_admin:
        abort(403)
    return render_template('home/admin_companies.html', title='Admin Companies')


@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        abort(403)
    return render_template('home/admin_dashboard.html', title='Admin Dashboard')


@home.route('/profile', methods=['GET'])
@login_required
def profile():

    return render_template('home/profilepage.html', title='Employee Profile', edit_profile=False)

@home.route('/profile/edit', methods=['GET','POST'])
@login_required
def edit_profile():

    form = UserEditForm(obj=current_user)
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        try:
            db.session.add(current_user)
            db.session.commit()
            flash('You have successfully update your profile')
        except Exception, e:
            flash('Error in updating profile. ' + str(e))
        return redirect(url_for('home.profile'))

    return render_template('home/profilepage.html',form=form, title='Edit Profile', edit_profile=True)

@home.route('/invite', methods=['GET','POST'])
def add_invite():

    email = request.args.get('email')
    invite = Invites.query.filter_by(email=email)
    if not invite:
        abort(404)
    company = invite.first().company
    user = User(email=email)
    form = InviteEditForm(obj=user)
    emp_role = Role.query.filter_by(name='employee').first()
    if form.validate_on_submit():
        user.first_name = form.fname.data
        user.last_name = form.lname.data
        user.password =  form.password.data
        user.role_id = emp_role.id
        try:
            db.session.add(user)
            mapping = Mapping(user_id=user.id)
            company.users.append(mapping)
            db.session.add(mapping)
            db.session.add(company)
            db.session.commit()
            flash('You have successfully update your profile. Please login')
        except Exception, e:
            flash('Error in updating profile. ' + str(e))
        return redirect(url_for('auth.login'))

    return render_template('home/invitee.html',form=form, title='Edit Profile')
