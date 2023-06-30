from flask import Blueprint, render_template, flash, redirect, url_for, request
from models import Product
from app import db

products = Blueprint('products', __name__)

@products.route('/products')
def product_list():
    # Retrieve all products from the database
    all_products = Product.query.all()
    return render_template('product_list.html', products=all_products)

@products.route('/products/<int:product_id>')
def product_details(product_id):
    # Retrieve product details by product_id
    product = Product.query.get_or_404(product_id)
    return render_template('product_details.html', product=product)

@products.route('/products/<int:product_id>/edit', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        # Update the product details based on the submitted form data
        product.name = request.form['name']
        # Handle other product fields if needed
        db.session.commit()

        flash('Product details updated successfully.', 'success')
        return redirect(url_for('products.product_details', product_id=product.id))

    return render_template('edit_product.html', product=product)

@products.route('/products/<int:product_id>/delete', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()

    flash('Product deleted successfully.', 'success')
    return redirect(url_for('products.product_list'))
