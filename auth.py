from flask import Blueprint
from flask import Flask, render_template, request, redirect, url_for, flash, session
from . import db
from website.user import user
from website.models import User, Product, Cart
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_bcrypt import Bcrypt


auth = Blueprint('auth', __name__)
bcrypt = Bcrypt()



@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if the password and confirm_password match
        if password != confirm_password:
            flash('Password and confirm password do not match.')
            return redirect(url_for('register'))

        # Check if the username or email already exist in the database
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        if existing_user:
            flash('Username or email already exists.')
            return redirect(url_for('register'))

        # Create a new user and hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. You can now log in.')
        return redirect(url_for('login'))

    return render_template('register.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Login successful.')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.')
            return redirect(url_for('login'))

    return render_template('login.html')


@auth.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully.')
    return redirect(url_for('index'))

@auth.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    quantity = int(request.form['quantity'])
    product = Product.query.get(product_id)
    if not product or quantity > product.quantity:
        flash('Product not available or insufficient quantity')
        return redirect(url_for('product_details', product_id=product_id))
    
    if 'user_id' in session:
        user_id = session['user_id']
        cart_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
            db.session.add(cart_item)
        db.session.commit()
        flash('Product added to cart')
    else:
        flash('Please log in to add products to your cart')
    
    return redirect(url_for('product_details', product_id=product_id))

@auth.route('/cart')
def view_cart():
    if 'user_id' in session:
        user_id = session['user_id']
        cart_items = Cart.query.filter_by(user_id=user_id).all()
        return render_template('cart.html', cart_items=cart_items)
    else:
        flash('Please log in to view your cart')
        return redirect(url_for('login'))
