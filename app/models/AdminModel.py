from flask_wtf import FlaskForm
from wtforms import SubmitField

class AdminModel(FlaskForm):
    delete = SubmitField("Delete")