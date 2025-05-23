from flask import Blueprint, render_template, flash
from .models.LoginModel import LoginModel
from .models.RegistrationModel import RegistrationModel
import pandas as pd

main = Blueprint('__main__', __name__)

@main.route("/")
def index():
    return render_template('index.html', data="")

# @main.route("/login", methods=['GET', 'POST'])
# def login():
#     form = LoginModel()

#     if form.validate_on_submit():
#         return "Successfully Logged In!"

    # return render_template('login.html', form=form)

@main.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationModel()

    if form.validate_on_submit():
        flash(f"Books in {form.data['preffered_genres']}: {process_recommendation(form.data['preffered_genres'])}")
        return render_template('index.html', data=form.data)
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field}: {error}")

    return render_template('register.html', form=form)

def process_recommendation(preffered_genre):
    recommended_books = ""

    data = {
        'Title': ['A Game of Thrones', 'Lucifer', 'Rain in España', 'Outlander', 'Replay'],
        'Genre': ['Fantasy', 'Fiction', 'Romance', 'Historical', 'Fiction']
    }

    for genre in preffered_genre:
        df = pd.DataFrame(data)
        recommended_books += str(df[df['Genre'] == genre]['Title'].tolist())
    
    return recommended_books if recommended_books else ["No books found with selected genres!"]