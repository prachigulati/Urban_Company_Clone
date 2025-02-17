from flask import Flask, render_template, request  # type: ignore
from flask_sqlalchemy import SQLAlchemy
import bcrypt # type: ignore

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db= SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100),nullable=False)
    password = db.Column(db.String(100))

    def __init__(self,password):
        self.password=bcrypt.hashpw(password.encode(''))
        
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=="POST":
        pass
    return render_template('register.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=="POST":
        pass
    return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True)
