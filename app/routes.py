from flask import Blueprint, render_template, flash, redirect, url_for, session
from .models.LoginModel import LoginModel
from .models.RegistrationModel import RegistrationModel
from .models.AccountSettingsModel import AccountSettingsModel
from .models.UserModel import UserModel
from app import db
import pandas as pd

main = Blueprint('__main__', __name__)

@main.route("/")
def index():
    if('user' in session):
        formatted_text = format_text_for_list(UserModel.retrieve_preffered_genres(session['user']["username"])).strip()
        genre_list = formatted_text[:len(formatted_text)-1].split(',')

        return render_template('index.html', UserModel=UserModel, recommended_books=process_recommendation(genre_list))
    else:
        flash("Please login first!")
        return redirect(url_for('__main__.login'))
    
@main.route("/account_settings", methods=['POST', 'GET'])
def account_settings():
    form = AccountSettingsModel()

    if('user' in session):             
        form.username.data = session['user']["username"]                                                                                                                                                                                                                                                                                                                                                                                                                       
        form.old_password.data = session['user']["password"]

        if form.validate_on_submit():
            if form.data["new_password"] == form.data["confirm_password"]:
                flash(UserModel.update_password(session['user']["username"], form.data["new_password"]))

                session['user']["username"] = format_text(UserModel.retrieve_username(session['user']["id"]))
                session['user']["password"] = format_text(UserModel.retrieve_password(session['user']["username"]))

                return redirect(url_for('__main__.account_settings'))
            else:
                flash("Passwords do not match!")
                                                                                                                                                                                                                                                                                                                                                                                                                                
        return render_template('account_settings.html', form=form)
    else:
        flash("Please login first!")
        return redirect(url_for('__main__.login'))

@main.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginModel()

    if form.validate_on_submit():
        if(UserModel.user_exists(form.data["username"])):
            if(form.data["password"] == format_text(UserModel.retrieve_password(form.data["username"]))):
                user = UserModel.retrieve_user(form.data["username"])
                session['user'] = {
                    "id": format_text(UserModel.retrieve_user_id(form.data["username"])),
                    "username": form.data["username"],
                    "password": form.data["password"]
                }
                
                formatted_text = format_text_for_list(UserModel.retrieve_preffered_genres(session['user']["username"])).strip()
                genre_list = formatted_text[:len(formatted_text)-1].split(',')

                flash(f" Howdy, {form.data["username"]}")
                return redirect(url_for('__main__.index', UserModel=UserModel, recommended_books=process_recommendation(genre_list)))
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
        if(UserModel.user_exists(form.data["username"])):
            flash("Username already exists")
        else:
            account = UserModel(
                username=form.data["username"],
                password=form.data["password"],
                email=form.data["email"],
                prefferred_genres=str(form.data["preffered_genres"])
            )

            db.session.add(account)
            db.session.commit()
            return redirect(url_for('__main__.login'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field}: {error}")

    return render_template('register.html', form=form)

def format_text(s: str) -> str:
    reject_char = str.maketrans({",": None, "'": None, "(": None, ")": None})
    return str(s).translate(reject_char)

def format_text_for_list(s: str) -> str:
    reject_char = str.maketrans({"'": None, "(": None, ")": None, '"': None, "[": None, "]": None})
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
    