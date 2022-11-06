from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


#Form to Create a new Post

class Create_post(FlaskForm):
    title = StringField('Title:', validators=[DataRequired()])
    content = TextAreaField('Content:', validators=[DataRequired()])
    submit = SubmitField('Post') 
  
   
#contact us form

class contact_form(FlaskForm):
    first_name = StringField('First Name:', validators=[DataRequired(), Length(min=5, max=20)])
    last_name = StringField('Last Name:', validators=[DataRequired(), Length(min=5, max=20)])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    message = TextAreaField('Message:', validators=[DataRequired()])
    submit = SubmitField('Submit Form')