from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from blog.models import User


#Register new users
class Registration_form(FlaskForm):
    __tablename__ = 'sign_up users'
    username = StringField('Username:', validators=[DataRequired(), Length(min=5, max=20)])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Password:', validators=[DataRequired(), Length(min=6, max=20)] )
    confirm_password = PasswordField('Confirm Password:', validators=[DataRequired(), EqualTo('password'), Length(min=6, max=20)] )
    submit = SubmitField('Sign Up')
    
    
    #Validate username to check already existing username
    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('Username Already Exist! Try Again')
   
   
    #Validate Email to check already existing email
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('email Already Exist! Try Again')
 
 
#Login users    
class Login_form(FlaskForm):
    __tablename__ = 'Login_users'
    email = StringField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Password:', validators=[DataRequired(), Length(min=6, max=20)] )
    remember = BooleanField('Remember Me:')
    submit = SubmitField('Login')


#Update your profile in the app
class Profile_update(FlaskForm):
    username = StringField('Username:', validators=[DataRequired(), Length(min=5, max=20)])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    profile_pics = FileField('Upload profile picture:', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')
    
    
    #Validate username 
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError('Username Already Exist! Try Again')
   
    #Validate Email
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError('email Already Exist! Try Again')


#Request for token

class Reset_request(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Reset Password')
    
    #Validate Email to check already existing email or Not
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is None:
            raise ValidationError('Email Not Found! Try Again')


#Reset password form

class Password_reset(FlaskForm):
    password = PasswordField('Password:', validators=[DataRequired(), Length(min=6, max=20)] )
    confirm_password = PasswordField('Confirm Password:', validators=[DataRequired(), EqualTo('password'), Length(min=6, max=20)] )
    submit = SubmitField('Reset Password')