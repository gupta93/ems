from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from app import db, login_manager

class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))


class User(UserMixin, db.Model):
    """
    Create an Employee table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship(Role, backref='user')
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())


    def is_admin(self):
        return self.role.name == 'admin'

    def is_super_admin(self):
        return self.role.name == 'super_admin'

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verifypassword(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.first_name)

class Company(db.Model):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(60))
    company_address = db.Column(db.String(300))
    users = db.relationship('Mapping', backref='company',cascade='delete', lazy=True)
    invites = db.relationship('Invites', backref='company',cascade='delete', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())


    def __repr__(self):
        return '<Company: {}>'.format(self.company_name)


class Mapping(db.Model):
    __tablename__ = 'mapping'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id',ondelete='CASCADE'))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))

class Invites(db.Model):
    __tablename__ = 'invites'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


