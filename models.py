from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager

db = SQLAlchemy()
login = LoginManager()

class UserModel (UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255),nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    gifs = relationship("Gif_history")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)   

class Gif_history(db.Model):
    __tablename__ = 'gifhistory'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("users.id"))
    gif_url = db.Column(db.String, nullable=False)
    giftime = db.Column(db.DateTime, nullable=False)





@login.user_loader
def load_user(id):
    return UserModel.query.get(int(id))
