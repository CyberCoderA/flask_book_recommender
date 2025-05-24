from flask import Blueprint, render_template, flash, redirect, url_for, session
from .models.LoginModel import LoginModel
from .models.RegistrationModel import RegistrationModel
from .models.UserModel import UserModel
from app import db
import pandas as pd

main = Blueprint('__main__', __name__)

@main.route("/")
def index():
    if('user' in session):
        return render_template('index.html')
    else:
        flash("Please login first!")
        return redirect(url_for('__main__.login'))

@main.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginModel()

    if form.validate_on_submit():
        if(UserModel.user_exists(form.data["username"])):
            if(form.data["password"] == format_text(UserModel.retrieve_password(form.data["username"]))):
                session['user'] = form.data

                flash(f" Howdy, {form.data["username"]}")
                return redirect(url_for('__main__.index'))
            else:
                flash("Incorrect password")
        else:
            flash("User does not exist")
            
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field}: {error}")

    return render_template('login.html', form=form)


@main.route("/logout")
def logout():
    session.pop('user', default=None)
    return redirect(url_for('__main__.login'))

@main.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationModel()

    if form.validate_on_submit():
        account = UserModel(
            username=form.data["username"],
            password=form.data["password"],
            email=form.data["email"],
        )

        db.session.add(account)
        db.session.commit()
        flash(f"Books in {form.data['preffered_genres']}: {process_recommendation(form.data['preffered_genres'])}")
        return redirect(url_for('__main__.index', data=form.data))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field}: {error}")

    return render_template('register.html', form=form)

def format_text(s: str) -> str:
    reject_char = str.maketrans({",": None, "'": None, "(": None, ")": None})
    return str(s).translate(reject_char)

def process_recommendation(preffered_genre):
    book_data = pd.read_excel(r'app\models\books.xlsx', sheet_name="book")
    df = pd.DataFrame(book_data)
    recommended_books = []
    num_rows = df.shape[0]

    for i in range(0, num_rows):
        temp_genre = (df['Genre'].loc[i]).split(",")

        for genre in temp_genre:
            for selected_genre in preffered_genre:
                if(selected_genre == genre.strip()):
                    if(recommended_books.__contains__({df['Title'].loc[i]})):
                        pass
                    else:
                        recommended_books.append({df['Title'].loc[i]})

    return recommended_books if recommended_books else ["No books found with selected genres!"]

    # multi-genre books
    # for i in range(0, num_rows):
    #     for j in df['Genre'].loc[i]:
    #         for genre in preffered_genre:
    #             if(j == genre):
    #                 if(recommended_books.__contains__({df['Title'].loc[i]})):
    #                     pass
    #                 else:
    #                     recommended_books.append({df['Title'].loc[i]})

    # single genre books
    # for genre in preffered_genre:
    #     recommended_books += str(df[df['Genre'] == genre]['Title'].tolist())
    