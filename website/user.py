from flask import Blueprint, render_template, flash, redirect, url_for, request
from models import User
from app import db

users = Blueprint('users', __name__)

@users.route('/users')
def user_list():
    # Retrieve all users from the database
    all_users = User.query.all()
    return render_template('user_list.html', users=all_users)

@users.route('/users/<int:user_id>')
def user_details(user_id):
    # Retrieve user details by user_id
    user = User.query.get_or_404(user_id)
    return render_template('user_details.html', user=user)

@users.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        # Update the user details based on the submitted form data
        user.username = request.form['username']
        # Handle other user fields if needed
        db.session.commit()

        flash('User details updated successfully.', 'success')
        return redirect(url_for('users.user_details', user_id=user.id))

    return render_template('edit_user.html', user=user)

@users.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    flash('User deleted successfully.', 'success')
    return redirect(url_for('users.user_list'))
