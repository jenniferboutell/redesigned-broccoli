from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField, DateField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from yelp import find_coffee
from wiki import *
from flask_login import current_user, login_user, login_required, logout_user
from models import db, login, UserModel

class loginForm(FlaskForm):
    email=StringField(label="Enter email", validators=[DataRequired(),Email()])
    password=PasswordField(label="Enter password",validators=[DataRequired(), Length(min=6,max=16)])
    submit=SubmitField(label="Login")

class BirthdayForm(FlaskForm):
    date=DateField(label="Enter Date", validators=[DataRequired()])
    number=IntegerField(label="Enter max number of records",validators=[DataRequired()])
    submit=SubmitField(label="Find Birthdays")

#passwords={}
#passwords['lhhung@uw.edu']='qwerty'

app = Flask(__name__)
app.secret_key="a secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/login.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login.init_app(app)

def addUser(email, password):
    #check if email or username exits
    user=UserModel()
    user.set_password(password)
    user.email=email
    db.session.add(user)
    db.session.commit()

@app.before_first_request
def init_app():
    logout_user()
def create_table():
    db.create_all()
    user = UserModel.query.filter_by(email = "jenniferaboutell@gmail.com").first()
    if user is None:
        addUser("jenniferaboutell@gmail.com","arugula")    
    

@app.route("/")
def redirectToLogin():
    return redirect("/login")

@app.route("/birthdays",methods=['GET','POST'])
@login_required
def Birthdays():
    form=BirthdayForm()
    number = 0
    if form.validate_on_submit():
        if request.method == "POST":
            date=request.form["date"]
            print(date)
            mdy = date.split("-")
            month_day = mdy[1] +  "/" + mdy[2]
            year = mdy[0]
            number=request.form["number"]
            data=findBirths(month_day,year,number)
            return render_template("birthdays.html",form=form, number=int(number), sortedbyClosestYear=data)
    return render_template("birthdays.html",form=form, number = 0)

@app.route("/login",methods=['GET','POST'])
def login():
    form=loginForm()
    if form.validate_on_submit():
        if request.method == "POST":
            email=request.form["email"]
            pw=request.form["password"]
            user = UserModel.query.filter_by(email = email).first()
            if user is not None and user.check_password(pw) :
                login_user(user)
                return redirect('/birthdays')
    return render_template("login.html",form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
