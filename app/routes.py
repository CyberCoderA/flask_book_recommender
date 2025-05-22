from flask import Blueprint, render_template, flash
from .models.LoginModel import LoginModel
from .models.RegistrationModel import RegistrationModel

main = Blueprint('__main__', __name__)

@main.route("/")
def index():
    return render_template('index.html', data="")

@main.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginModel()

    if form.validate_on_submit():
        return "Successfully Logged In!"

    return render_template('login.html', form=form)

@main.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationModel()

    if form.validate_on_submit():
        flash("Registration Successful!")
        return render_template('index.html', data=form.data)
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Registration Failed: {error}")

    return render_template('register.html', form=form)

