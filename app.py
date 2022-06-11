mport json
from urllib import parse, request
from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from flask_login import current_user, login_user, login_required, logout_user
from models import db, login, UserModel, StudentModel
app = Flask(__name__)

class loginForm(FlaskForm):
        username=StringField(label="Enter username",validators=[DataRequired(), Length(min=4,max=25)])
        email = StringField(label = "Enter Email", validators = [DataRequired(), Email()])
        password = PasswordField(label = "Enter Password", validators = [DataRequired(), Length(min=4, max=550)])
        submit = SubmitField(label = "Login")

class registerForm(FlaskForm):
        email=StringField(label="Enter email", validators=[DataRequired(),Email()])
        password=PasswordField(label="Enter password",validators=[DataRequired(), Length(min=6,max=255)])
        username=StringField(label="Enter username",validators=[DataRequired(), Length(min=4,max=25)])
        submit=SubmitField(label="Register")

class loginForm_Student(FlaskForm):
        username=StringField(label="Enter username",validators=[DataRequired(), Length(min=4,max=25)])
        password = PasswordField(label = "Enter Password", validators = [DataRequired(), Length(min=4, max=255)])
        submit = SubmitField(label = "Login")

class registerForm_Student(FlaskForm):
        password=PasswordField(label="Enter password",validators=[DataRequired(), Length(min=4,max=255)])
        username=StringField(label="Enter username",validators=[DataRequired(), Length(min=4,max=25)])
        submit=SubmitField(label="Register")

app = Flask(__name__)
app.secret_key = "RC5594"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/login.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login.init_app(app)


def addTeacher(username, email, password):
        user = UserModel()
        user.set_password(password)
        user.username = username
        user.email = email
        db.session.add(user)
        db.session.commit()

def addStudent(username, password):
        user = StudentModel()
        user.set_password(password)
        user.username = username
        db.session.add(user)
        db.session.commit()

@app.before_first_request
def create_table():
        db.create_all()


def gif(mood):
        gifs = []
        url = "http://api.giphy.com/v1/gifs/search"

        params = parse.urlencode({
                "q": mood,
                "api_key": "3m4gf6qKSc1vuLPwwPVyCGVk3K5su1nZ",
                "limit": "20"
        })

        with request.urlopen("".join((url, "?", params))) as response:
                data = json.loads(response.read())

        for gif in data['data']:
                gifs.append(gif['images']['fixed_height']['url'])

        return gifs

@app.route("/home/teacher", methods=['GET','POST'])
@login_required
def homeTeacher():
        return render_template("home.html")

@app.route("/home/student", methods=['GET','POST'])
@login_required
def homeStudent():
        return render_template("home_student.html")

@app.route("/students")
def queryStudents():
        st = StudentModel.query.all()
        return render_template("student.html", st = st)

@app.route("/")
def redirecttoLogin():
        return redirect("/login")

@app.route("/login")
def login():
        return render_template("login.html")

@app.route("/login/teacher", methods=['GET', 'POST'])
def loginTeacher():
        form = loginForm()
        if form.validate_on_submit():
                if request.method == 'POST':
                        username = request.form["username"]
                        email = request.form["email"]
                        pw = request.form["password"]
                        user = UserModel.query.filter_by(email = email).first()
                        if email is not None and user.check_password(pw):
                                login_user(user)
                                return redirect('/home/teacher')
        return render_template("login_teacher.html", form = form)

      @app.route("/login/student", methods=['GET', 'POST'])
def loginStudent():
        form = loginForm_Student()
        if form.validate_on_submit():
                if request.method == 'POST':
                        username = request.form["username"]
                        pw = request.form["password"]
                        user = StudentModel.query.filter_by(username = username).first()
                        if username is not None and user.check_password(pw):
                                login_user(user)
                                return redirect('/home/student')
        return render_template("login_student.html", form = form)

@app.route("/register/teacher",methods=['GET','POST'])
def registerTeacher():
        form=registerForm()
        if form.validate_on_submit():
                if request.method == "POST":
                        username = request.form["username"]
                        email=request.form["email"]
                        pw=request.form["password"]
                        user = UserModel.query.filter_by(email = email).first()
                        if user is not None :
                                return redirect('/register/teacher')
                        user = UserModel.query.filter_by(username = username).first()
                        if user is not None :
                                return redirect('/register/teacher')
                        addTeacher(username, email, pw)
                        return redirect('/login')
        return render_template("register_teacher.html",form=form)

@app.route("/register/student",methods=['GET','POST'])
def registerStudent():
        form=registerForm_Student()
        if form.validate_on_submit():
                if request.method == "POST":
                        username = request.form["username"]
                        pw=request.form["password"]
                        user = StudentModel.query.filter_by(username = username).first()
                        if user is not None :
                                return redirect('/register/student')
                        addStudent(username, pw)
                        return redirect('/home/teacher')
        return render_template("register_student.html",form=form)

@app.route("/logout")
def logout():
        logout_user()
        return redirect("/login")

@app.route("/sad")
def sad():
        title = "Sad moods"
        gifs = gif("sad")
        return render_template('moods.html', title=title, gifs=gifs)

@app.route("/happy")
def happy():
        title = "Happy moods"
        gifs = gif("happy")
        return render_template('moods.html', title=title, gifs=gifs)

@app.route("/anxious")
def anxious():
        title = "Anxious moods"
        gifs = gif("anxious")
        return render_template('moods.html', title=title, gifs=gifs)

@app.route("/angry")
def angry():
        title = "Angry moods"
        gifs = gif("angry")
        return render_template('moods.html', title=title, gifs=gifs)

if __name__ == "__main__":
        app.run(host = '0.0.0.0',debug=True)


