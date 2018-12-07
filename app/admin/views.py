from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from .. import db,HOST_IP
from ..models import User, Company, Mapping, Role, Invites
from forms import CompanyForm, UserForm, UserEditForm, InviteForm
from functions import send_mail

def check_super_admin():
    if not current_user.role.name == "super_admin":
        abort(403)


def check_admin():
    if not current_user.role.name == "admin":
        abort(403)

@admin.route('/companies')
@login_required
def list_companies():
    """
    List all employees
    """
    check_super_admin()

    companies = Company.query.all()

    return render_template('admin/companies/companies.html',
                           companies=companies, title='Companies')


@admin.route('/employees')
@login_required
def list_employees():
    """
    List all employees
    """
    check_admin()
    company = Mapping.query.filter_by(user_id=current_user.id).first().company
    mapping = company.users
    user_ids = []
    if len(mapping) > 1:
        for map in mapping:
            if map.user_id != current_user.id:
                user_ids.append(map.user_id)
        employees = User.query.filter(User.id.in_(user_ids))
    else:
        employees = []
    return render_template('admin/employees/employees.html',
                           employees=employees, title='Employees', company=company)


@admin.route('/companies/add', methods=['GET', 'POST'])
@login_required
def add_company():
    
    check_super_admin()

    add_company = True

    form = CompanyForm()
    if form.validate_on_submit():
        company = Company(company_name=form.name.data,
                      company_address=form.address.data)

        try:
            db.session.add(company)
            db.session.commit()
            flash('You have successfully added a new company')
        except Exception,e:
            flash('Error in adding company. ')

        # redirect to the pay grades page
        return redirect(url_for('admin.list_companies'))

    # load role template
    return render_template('admin/companies/company.html', add_company=add_company,
                           form=form, title='Add Company')


@admin.route('/employees/<int:id>/add', methods=['GET', 'POST'])
@login_required
def add_employee(id):
    check_admin()

    add_employee = True
    employee_role = Role.query.filter_by(name='employee').first()
    form = UserForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                      first_name=form.fname.data,
                      last_name=form.lname.data,
                      password=form.password.data,
                      role_id=employee_role.id)
        company = Company.query.get(id)
        try:
            db.session.add(user)
            db.session.commit()
            mapping = Mapping(user_id=user.id)
            company.users.append(mapping)
            db.session.add(mapping)
            db.session.add(company)
            db.session.commit()
            flash('You have successfully added a new employee')
        except Exception, e:
            flash('Error in adding employee. ')

        # redirect to the pay grades page
        return redirect(url_for('admin.list_employees'))

    # load role template
    return render_template('admin/employees/employee.html', add_employee=add_employee,
                           form=form, title='Add Employee')

@admin.route('/employees/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_employee(id):
    check_admin()

    add_employee = False
    user = User.query.get_or_404(id)
    form = UserEditForm(obj=user)
    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        try:
            db.session.add(user)
            db.session.commit()
            flash('You have successfully update the employee')
        except Exception, e:
            flash('Error in updating employee. ')

        # redirect to the employees list view
        return redirect(url_for('admin.list_employees'))

    # load template
    return render_template('admin/employees/employee.html', add_employee=add_employee,
                           form=form, title='Edit Employee')

@admin.route('/companies/<int:id>/admin', methods=['GET', 'POST'])
@login_required
def add_admin(id):
    
    check_super_admin()

    add_admin = True
    admin_role = Role.query.filter_by(name='admin').first()
    form = UserForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                      first_name=form.fname.data,
                      last_name=form.lname.data,
                      password=form.password.data,
                      role_id=admin_role.id)
        company = Company.query.get(int(id))
        try:
            db.session.add(user)
            db.session.commit()
            mapping = Mapping(user_id=user.id)
            company.users.append(mapping)
            db.session.add(mapping)
            db.session.add(company)
            db.session.commit()
            flash('You have successfully added a admin')
        except Exception,e:
            flash('Error in adding admin. '+ str(e))

        # redirect to companies list view
        return redirect(url_for('admin.list_companies'))

    # load add admin template
    return render_template('admin/companies/admin.html', add_admin=add_admin,
                           form=form, title='Add Admin')


@admin.route('/companies/delete/<int:id>', methods=['GET','POST'])
@login_required
def delete_company(id):
    """
    Deletes a company by super admin
    """
    check_super_admin()

    company = Company.query.get_or_404(id)

    db.session.delete(company)
    db.session.commit()
    flash('You have successfully deleted the account.')

    # redirect to list companies view
    return redirect(url_for('admin.list_companies'))

@admin.route('/employees/delete/<int:id>', methods=['GET','POST'])
@login_required
def delete_employee(id):

    check_admin()

    employee = User.query.get_or_404(id)


    db.session.delete(employee)
    db.session.commit()
    flash('You have successfully deleted the employee')

    # redirect to list employees view
    return redirect(url_for('admin.list_employees'))

@admin.route('/<int:id>/invite', methods=['GET','POST'])
@login_required
def invite_employee(id):
    check_admin()
    company = Company.query.get_or_404(id)
    form = InviteForm()
    if form.validate_on_submit():
       email = form.email.data
       link = 'http://{}/invite?email={}'.format(HOST_IP, email)
       text = 'You have been invited to join EMS by {}. Use link : {}'.format(company.company_name, link)
       invite = Invites(email=email, company_id = company.id)
       db.session.add(invite)
       db.session.commit()
       send_mail(sender=None, receiver=[email], name='EMS Team', subject='Invite Link', text=text)
       flash('Your invitation is sent to {}'.format(email))
       return redirect(url_for('admin.list_employees'))

    return render_template('admin/employees/invite.html',form=form, title='Invite Employee')