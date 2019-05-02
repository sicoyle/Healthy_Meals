from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import UserModel
from wtforms import StringField, TextField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms import SelectField
import wtforms
from flask_wtf.file import FileField, FileAllowed

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = UserModel.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('E-mail has already been used')


class EditProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address_line_1 = StringField('Address Line 1', validators=[DataRequired()])
    address_line_2 = StringField('Address Line 2', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])

    STATE_ABBREV = ('Select State', 'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 
                'HI', 'ID', 'IL', 'IN', 'IO', 'KS', 'KY', 'LA', 'ME', 'MD', 
                'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 
                'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 
                'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY')

    

    state = wtforms.SelectField(label='State', 
        choices=[(state, state) for state in STATE_ABBREV])    
    zip_code = StringField('Zip Code', validators=[DataRequired()])
    phone_number = StringField('Phone Number')
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'], 'Invalid file type. Input jpg or png.')])
    submit = SubmitField('Submit')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[DataRequired()])
    password = PasswordField('New password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm new password', validators=[DataRequired()])
    submit = SubmitField('Update Password')

class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    submit = SubmitField('Reset Password')

class PasswordResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('New Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown email address.')

class PostForm(FlaskForm):
    post = TextField('Add a ToDo item', validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Submit')

#test
#Length(min=1, max=140)]
