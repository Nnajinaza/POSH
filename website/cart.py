from flask import Blueprint, render_template, flash, redirect, url_for, session, request
from models import Product

cart = Blueprint('cart', __name__)

@cart.route('/cart')
def view_cart():
    cart_items = session.get('cart', [])
    products = []
    total_price = 0

    # Retrieve product details for each item in the cart
    for item in cart_items:
        product = Product.query.get(item['product_id'])
        if product:
            quantity = item['quantity']
            item_total = product.price * quantity
            total_price += item_total
            products.append({
                'product': product,
                'quantity': quantity,
                'item_total': item_total
            })

    return render_template('cart.html', products=products, total_price=total_price)

@cart.route('/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    quantity = int(request.form.get('quantity', 1))

    # Retrieve the product from the database
    product = Product.query.get_or_404(product_id)

    # Retrieve the cart from the session
    cart = session.get('cart', [])

    # Check if the product is already in the cart
    for item in cart:
        if item['product_id'] == product_id:
            # Increment the quantity if the product is already in the cart
            item['quantity'] += quantity
            flash('Product quantity updated in the cart.', 'info')
            break
    else:
        # Add the product to the cart if it's not already present
        cart.append({
            'product_id': product_id,
            'quantity': quantity
        })
        flash('Product added to the cart.', 'success')

    # Update the cart in the session
    session['cart'] = cart

    return redirect(url_for('cart.view_cart'))

@cart.route('/cart/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    # Retrieve the cart from the session
    cart = session.get('cart', [])

    # Remove the product from the cart
    cart = [item for item in cart if item['product_id'] != product_id]

    # Update the cart in the session
    session['cart'] = cart

    flash('Product removed from the cart.', 'success')
    return redirect(url_for('cart.view_cart'))

@cart.route('/cart/clear', methods=['POST'])
def clear_cart():
    # Clear the cart in the session
    session.pop('cart', None)

    flash('Cart cleared.', 'success')
    return redirect(url_for('cart.view_cart'))
