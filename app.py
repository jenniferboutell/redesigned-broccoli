import json
import urllib.request
from datetime import datetime
from urllib import parse
from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField, DateField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from yelp import find_coffee
from wiki import *
from flask_login import current_user, login_user, login_required, logout_user
from models import db, login, UserModel, Gif_history

class loginForm(FlaskForm):
    email=StringField(label="Enter email", validators=[DataRequired(),Email()])
    password=PasswordField(label="Enter password",validators=[DataRequired(), Length(min=6,max=16)])
    username=StringField(label="Enter username",validators=[DataRequired(), Length(min=6,max=255)])
    submit=SubmitField(label="Login")

class registerForm(FlaskForm):
    email=StringField(label="Enter email", validators=[DataRequired(),Email()])
    password=PasswordField(label="Enter password",validators=[DataRequired(), Length(min=6,max=16)])
    username=StringField(label="Enter usrname",validators=[DataRequired(), Length(min=6,max=255)])
    submit=SubmitField(label="Register")


DBUSER = 'jboutell'
DBPASS = 'arugula'
DBHOST = 'db'
DBPORT = '5432'
DBNAME = 'pglogindb'

class moodForm(FlaskForm):
    gif_url = StringField(validators=[Length(min=6, max=1000)])
    

#class BirthdayForm(FlaskForm):
 #   date=DateField(label="Enter Date", validators=[DataRequired()])
  #  number=IntegerField(label="Enter max number of records",validators=[DataRequired()])
   # submit=SubmitField(label="Find Birthdays")

#passwords={}
#passwords['lhhung@uw.edu']='qwerty'

app = Flask(__name__)
app.secret_key="a secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
        user=DBUSER,
        passwd=DBPASS,
        host=DBHOST,
        port=DBPORT,
        db=DBNAME)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login.init_app(app)

def addUser(email, password, username):
    #check if email or username exits
    user=UserModel()
    user.set_password(password)
    user.email=email
    user.username=username
    db.session.add(user)
    db.session.commit()

def addGif(gif_url, giftime, user_id):
    gifchoice = Gif_history()
    gifchoice.gif_url = gif_url
    gifchoice.giftime = giftime
    gifchoice.user_id = user_id
    db.session.add(gifchoice)
    db.session.commit()
    
@app.before_first_request
def create_table():
    db.create_all()
    user = UserModel.query.filter_by(email = "jenniferaboutell@gmail.com").first()
    if user is None:
        addUser("jenniferaboutell@gmail.com","arugula","jboutell")    

def gif(mood):
    gifs = []
    url = "http://api.giphy.com/v1/gifs/search"

    params = parse.urlencode({
        "q": mood,
        "api_key": "3m4gf6qKSc1vuLPwwPVyCGVk3K5su1nZ",
        "limit": "20"
  })

    with urllib.request.urlopen("".join((url, "?", params))) as response:
        data = json.loads(response.read())

    for gif in data['data']:
        gifs.append(gif['images']['fixed_height']['url'])

    return gifs


    
@app.route("/")
def redirectToLogin():
    return redirect("/login")

@app.route("/zones")
@login_required
def Zones():
    return render_template("zones.html")

@app.route("/login",methods=['GET','POST'])
def login():
    form=loginForm()
    if form.validate_on_submit():
        if request.method == "POST":
            email=request.form["email"]
            pw=request.form["password"]
            username=request.form["username"]
            user = UserModel.query.filter_by(email = email).first()
            if user is not None and user.check_password(pw) :
                login_user(user)
                return redirect('/zones')
    return render_template("register.html",form=form)

@app.route("/register",methods=['GET','POST'])
def register():
    form=registerForm()
    if form.validate_on_submit():
        if request.method == "POST":
            username = request.form["username"]
            email=request.form["email"]
            pw=request.form["password"]
            user = UserModel.query.filter_by(email = email).first()
            if user is not None :
                return redirect('/register')
            user = UserModel.query.filter_by(username = username).first()
            if user is not None :
                return redirect('/register')
            addUser(email, pw, username)
            return redirect('/login')
    return render_template("register.html",form=form)

@app.route("/mood", methods=["POST"])
def getmood():
    #form=moodForm()
    #if form.validate_on_submit():
    gif_url = request.form["gif_url"]
    giftime = datetime.now()
    user_id = current_user.id
    addGif(gif_url,giftime,user_id)
    return redirect('/moodhistory')

@app.route("/moodhistory")
def moodhistory():
    title = "Your Mood History"
    return render_template("moodhistory.html",user=current_user)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')

@app.route("/sad")
def sad():
  title = "Sad moods"
  gifs = gif("sad")
  return render_template('moods.html', title=title, gifs=gifs)

@app.route("/sick")
def sick():
  title = "Sick Moods"
  gifs = gif("sick")
  return render_template('moods.html', title=title, gifs=gifs)

@app.route("/tired")
def tired():
  title = "Tired Moods"
  gifs = gif("tired")
  return render_template('moods.html', title=title, gifs=gifs)

@app.route("/bored")
def bored():
  title = "Bored Moods"
  gifs = gif("bored")
  return render_template('moods.html', title=title, gifs=gifs)


@app.route("/happy")
def happy():
  title = "Happy moods"
  gifs = gif("happy")
  return render_template('moods.html', title=title, gifs=gifs)

@app.route("/calm")
def calm():
  title = "Calm Moods"
  gifs = gif("Calm")
  return render_template('moods.html', title=title, gifs=gifs)

@app.route("/focused")
def focused():
  title = "Focused Moods"
  gifs = gif("focused")
  return render_template('moods.html', title=title, gifs=gifs)

@app.route("/relaxed")
def relaxed():
  title = "Relaxed Moods"
  gifs = gif("relaxed")
  return render_template('moods.html', title=title, gifs=gifs)

@app.route("/frustrated")
def frustrated():
  title = "Frustrated Moods"
  gifs = gif("frustrated")
  return render_template('moods.html', title=title, gifs=gifs)

@app.route("/worried")
def worried():
  title = "Worried Moods"
  gifs = gif("worried")
  return render_template('moods.html', title=title, gifs=gifs)

@app.route("/silly")
def silly():
  title = "Silly Moods"
  gifs = gif("silly")
  return render_template('moods.html', title=title, gifs=gifs)

@app.route("/excited")
def excited():
  title = "Excited Moods"
  gifs = gif("excited")
  return render_template('moods.html', title=title, gifs=gifs)


@app.route("/angry")
def angry():
  title = "Angry moods"
  gifs = gif("angry")
  return render_template('moods.html', title=title, gifs=gifs)


@app.route("/terrified")
def terrified():
  title = "Terrified Moods"
  gifs = gif("terrified")
  return render_template('moods.html', title=title, gifs=gifs)

@app.route("/ecstatic")
def ecstatic():
  title = "Ecastatic Moods"
  gifs = gif("ecstatic")
  return render_template('moods.html', title=title, gifs=gifs)

@app.route("/devasted")
def devasted():
  title = "Devastated Moods"
  gifs = gif("devastated")
  return render_template('moods.html', title=title, gifs=gifs)




@app.route("/allmoods")
def allmoods():
   title="Choose Your Mood"
   return render_template('allmoods.html', title=title)



if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
