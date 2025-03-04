from flask import Flask, render_template, request, flash , redirect, url_for, session  # type: ignore
from datetime import timedelta #importing timedelta for session timeout
from flask_sqlalchemy import SQLAlchemy  #importing Flask-SQLAlchemy for database handeling
from werkzeug.security import generate_password_hash, check_password_hash  #for password hashing ans securing


#configure the app
app=Flask(__name__)   #created a flask application instance
app.secret_key= "xyz"    #secret key for session management and security
app.permanent_session_lifetime=timedelta(minutes=5)   #session timeout
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  #database URI for SQLite
db= SQLAlchemy(app)   #initialize SQLAlchemy with the app


#create a model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(150), nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)  #method to set a hashed password
    
    def get_password(self, password):
        return check_password_hash(self.password_hash, password)  #method to check the password
# The user class represents a table in the database with columns id, username, and password_hash.


#creating routes
@app.route('/')   #defines the url path for the home page
def home():
    return render_template('index.html')

@app.route('/panels')
def panels():
    return render_template('panels.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=="POST":
        username = request.form['username']   #gets username from the form
        password = request.form['password']   #gets password from the form
        user = User(username=username)   #User instance
        user.set_password(password)   #set hashed pass
        db.session.add(user)   #add the user to databse session
        db.session.commit()    #commit the session to save the user
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()   #Query the user from the database
        if user and user.get_password(password):   #validate the pass
            session.permanent = True   #this makes the session permanent
            session['user'] = user.username   #this stores the username in session
            flash("Login Successful!", "info")
            return redirect(url_for("user"))
        else:
            flash('Invalid credentials', 'danger')
    if "user" in session:
        flash("Already Logged In!", "info")
        return redirect(url_for("user"))
    return render_template('login.html')

@app.route("/user")
def user():
    if "user" in session:
        user=session["user"]  #get the username from session
        return render_template("user.html",user=user)  #rendering the user page with username
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash("You have been logged out!","info")
    session.pop("user",None)  #to remove the user from session
    return redirect(url_for("login"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  #create the database tables
    app.run(debug=True)
