# Import the main form class from Flask-WTF
from flask_wtf import FlaskForm

# Import various field types for forms
from wtforms.fields import StringField, PasswordField, SubmitField, SelectField, IntegerField, FileField, HiddenField
# Import validators to ensure form data meets requirements
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
# Import specific file upload validators
from flask_wtf.file import FileRequired, FileAllowed


class RegistrationForm(FlaskForm):
    # Registration fields with validators
    username = StringField('Username', validators=[DataRequired('You are silly, enter a username')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    level = SelectField('Level', choices=['None', 'Premium Tier', 'Cheap Tier'])
    height = IntegerField('Height', validators=[DataRequired()])
    submit = SubmitField('Submit')

    # Custom validators
    def validate_height(self, height):
        if height.data > 150:
            raise ValidationError('You are too tall')
        if height.data < 100:
            raise ValidationError('You are too short')

    def validate_level(self, level):
        if level.data == 'None':
            raise ValidationError('You must chose a level')

class CSVUploadForm(FlaskForm):
    # Form for uploading CSV files - requires a file and limits to CSV extension
    file = FileField('Upload', validators=[FileRequired(), FileAllowed(['csv'])])
    submit = SubmitField('Submit')

class ItemForm(FlaskForm):
    # Form with hidden field to track which fruit is selected
    fruit_choice = HiddenField('fruit_choice')

# Form specifically for file downloads
class DownloadForm(FlaskForm):
    # Simple form with just a submit button to trigger file download
    submit = SubmitField('Download')
