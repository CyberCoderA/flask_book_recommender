from flask import Blueprint, render_template, flash, redirect, url_for
from .models.LoginModel import LoginModel
from .models.RegistrationModel import RegistrationModel
from .models.UserModel import UserModel
from app import db
import pandas as pd

main = Blueprint('__main__', __name__)

@main.route("/")
def index():
    return render_template('index.html', data="")

@main.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginModel()

    if form.validate_on_submit():
        for account in account_list():
            reject_char = str.maketrans({",": None, "'": None, "(": None, ")": None})
            reformatted = str(retrieve_password(account[0].username)[0]).translate(reject_char)
            
            if(form.data["password"] == reformatted):
                flash(f" username: {account[0].username}\n")
                return redirect(url_for('__main__.index', data=form.data))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field}: {error}")

    return render_template('login.html', form=form)

@main.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationModel()

    if form.validate_on_submit():
        account = UserModel(
            username=form.data["username"],
            password="!2345",
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

def account_list():
    accounts = db.session.execute(db.select(UserModel).order_by(UserModel.username)).fetchall()
    return accounts

def retrieve_password(username):
    return db.session.execute(db.select(UserModel.password).filter(UserModel.username == username)).fetchall()

def process_recommendation(preffered_genre):
    book_data = pd.read_excel(r'\app\models\books.xlsx', sheet_name="book")
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
    
    return recommended_books if recommended_books else ["No books found with selected genres!"]