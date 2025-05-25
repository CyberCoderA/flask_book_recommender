from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, DataRequired

class AccountSettingsModel(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=50)])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8, max=20)])
    old_password = StringField('Old Password', render_kw={'readonly': True})

    update = SubmitField('Update')