from flask import Blueprint, render_template
from .models.LoginModel import LoginModel

main = Blueprint('__main__', __name__)

@main.route("/")
def index():
    return render_template('index.html')

@main.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginModel()

    if form.validate_on_submit():
        return "Successfully Logged In!"

    return render_template('login.html', form=form)