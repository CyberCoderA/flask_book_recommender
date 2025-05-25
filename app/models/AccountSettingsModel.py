from flask_wtf import FlaskForm
from wtforms import SubmitField

class AccountSettingsModel(FlaskForm):
    delete = SubmitField('Delete')