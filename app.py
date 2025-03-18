from flask import Flask, render_template, request, flash, redirect, url_for, session # type: ignore
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash # type: ignore
from flask_migrate import Migrate # type: ignore

# Configure the app
app = Flask(__name__)
app.secret_key = "xyz"
app.permanent_session_lifetime = timedelta(minutes=5)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def get_password(self, password):
        return check_password_hash(self.password_hash, password)

# Item model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200), nullable=False)

# Cart model
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)  # Added quantity

# Routes
@app.route('/')
def home():
    items = Item.query.all()
    return render_template('index.html', items=items)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.get_password(password):
            session.permanent = True
            session['user'] = user.username
            session['user_id'] = user.id
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
        user = session["user"]
        return render_template("user.html", user=user)
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("user_id", None)
    flash("You have been logged out!", "info")
    return redirect(url_for("login"))

# ADD TO CART ROUTE
@app.route('/add_to_cart/<int:item_id>')
def add_to_cart(item_id):
    if 'user_id' not in session:
        flash('You need to login to add items to the cart.', 'warning')
        return redirect(url_for('login'))
    user_id = session['user_id']
    existing_cart_item = Cart.query.filter_by(user_id=user_id, item_id=item_id).first()
    if existing_cart_item:
        existing_cart_item.quantity += 1
    else:
        new_cart_item = Cart(user_id=user_id, item_id=item_id, quantity=1)
        db.session.add(new_cart_item)
    db.session.commit()
    # flash('Item added to cart successfully!', 'success')
    return redirect(url_for('view_cart'))

# REMOVE FROM CART ROUTE
@app.route('/remove_from_cart/<int:item_id>')
def remove_from_cart(item_id):
    if 'user_id' not in session:
        flash('You need to login to modify the cart.', 'warning')
        return redirect(url_for('login'))
    user_id = session['user_id']
    cart_item = Cart.query.filter_by(user_id=user_id, item_id=item_id).first()
    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            db.session.delete(cart_item)
        db.session.commit()
    # flash('Item removed from cart successfully!', 'info')
    return redirect(url_for('view_cart'))

@app.route('/cart')
def view_cart():
    if 'user_id' not in session:
        flash('Please log in to view your cart.', 'warning')
        return redirect(url_for('login'))
    user_id = session['user_id']
    cart_items = db.session.query(Item, Cart.quantity).join(Cart).filter(Cart.user_id == user_id).all()
    total_price = sum(item.price * quantity for item, quantity in cart_items)
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

@app.route('/beauty')
def beauty():
    return render_template('beauty.html')

@app.route('/panels')
def panels():
    return render_template('panels.html')

@app.route('/native')
def native():
    return render_template('native.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure database tables are created
        sample_items = [
            {'name': 'Pain relief', 'price': 199.0, 'image': "https://res.cloudinary.com/urbanclap/image/upload/t_high_res_template/w_231,dpr_2,fl_progressive:steep,q_auto:low,f_auto/c_limit/images/growth/luminosity/1700143543316-c5eb5c.jpeg"},
            {'name': 'Stress relief', 'price': 199.0, 'image': "https://res.cloudinary.com/urbanclap/image/upload/t_high_res_template/w_231,dpr_2,fl_progressive:steep,q_auto:low,f_auto/c_limit/images/growth/luminosity/1700143539186-26f4e5.jpeg"},
            {'name': 'Natural Skincare', 'price': 299.0, 'image': "https://res.cloudinary.com/urbanclap/image/upload/t_high_res_template/w_231,dpr_2,fl_progressive:steep,q_auto:low,f_auto/c_limit/images/growth/luminosity/1700143553928-f5f936.jpeg"}
        ]
        db.session.commit()
    app.run(debug=True)
