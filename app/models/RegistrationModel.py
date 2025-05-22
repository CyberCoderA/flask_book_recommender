from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import Length, DataRequired, Email
from wtforms import widgets, SelectMultipleField
import email_validator

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(html_tag='ol', prefix_label=False)
    option_widget = widgets.CheckboxInput()

class RegistrationModel(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])

    genres = [(1, 'Romance'), (2, 'Action'), (3, 'Adventure'), (4, 'Thriller')] 
    preffered_genres = MultiCheckboxField('Preferred Genres', choices=genres, validators=[Length(min=1, max=3)])
    
    submit = SubmitField('Login')