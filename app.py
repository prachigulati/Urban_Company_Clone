from flask import Flask, render_template, request, flash , redirect, url_for, session , flash # type: ignore
from datetime import timedelta
# from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.secret_key= "xyz"
app.permanent_session_lifetime=timedelta(minutes=5)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# db= SQLAlchemy(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(100),nullable=False)
#     password = db.Column(db.String(100))

#     def __init__(self,password):
#         self.password=bcrypt.hashpw(password.encode(''))
        
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=="POST":
        pass
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=="POST":
        session.permanent = True
        user=request.form["nm"]
        session["user"]=user
        flash("Login Successful!","info")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already Logged In!","info")
            return redirect(url_for("user"))
        return render_template('login.html')
@app.route("/user")
def user():
    if "user" in session:
        user=session["user"]
        return render_template("user.html",user=user)
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash("You have been logged out!","info")
    session.pop("user",None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
