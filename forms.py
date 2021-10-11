from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, DateField, SelectField, IntegerField
from wtforms.validators import DataRequired,Length, EqualTo

#Forms
class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Length(min=6, max=100)])
    password = PasswordField('password', validators=[DataRequired()])
    
class SignUpForm(FlaskForm):
    firstname = StringField('first name', validators=[DataRequired(), Length(min=1, max=50)])
    lastname = StringField('last name', validators=[DataRequired(), Length(min=1, max=50)])
    email = StringField('email', validators=[DataRequired(), Length(min=6, max=100)])
    contact = StringField('Telephone number', [Length(min=10, max=10, message='must be valid phone number')])
    password = PasswordField('password', validators=[DataRequired(), EqualTo('confirm', message='passwords should match')])
    confirm = PasswordField('confirm password')
    dob = DateField('Date of Birth (dd-mm-yyyy)', validators=[DataRequired()], format='%d-%m-%Y')
    skills = TextAreaField('Any skills you would like to employers to see', [Length(max=500)])
    status = SelectField(
        'current employment status',
        choices=[('yes', 'On a Job'), ('no', 'Available'), ('none', "I'd rather not say")]
    )

class JobPostForm(FlaskForm):
    title = StringField('Job title', validators=[DataRequired(), Length(min=1, max=50)])
    description = TextAreaField('Detailed Description', [Length(min=1, max=1000)])
    duration = StringField('Duration (eg. 2 days)', validators=[DataRequired(), Length(min=1, max=50)])
    amount = StringField('How much are you paying for this Job?', validators=[DataRequired(), Length(min=1, max=50)])
    no_of_people = IntegerField('How many people for this Job?', validators=[DataRequired()])

class CommentForm(FlaskForm):
	text = TextAreaField('comment', [Length(min=1, max=50)])
