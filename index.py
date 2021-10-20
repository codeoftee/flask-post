# flask project
import os
from datetime import timedelta

from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

from config import Config
import hashlib

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import User, Product
from app_functions import check_login


@app.route('/')
def homepage():
    user = check_login()
    if user is None:
        return redirect(url_for('login'))

    return render_template('home.html', user=user)


@app.route('/about')
def about_page():
    return "<h1>About Flask page 2</h1>"


@app.route('/products/')
def product_page():
    products = Product.query.all()
    user = check_login()
    return render_template('all_products.html', products=products, user=user)


@app.route('/add-product', methods=['POST'])
def add_product():
    user = check_login()
    if user is None:
        return redirect(url_for('login'))
    title = request.form['title']
    price = request.form['price']
    category = request.form['category']
    description = request.form['description']
    # upload image
    image = request.files['image']
    if image is None or image.filename is None:
        flash('Please select product image!')
        return render_template('add-product.html')
    print(image.filename)
    filename = secure_filename(image.filename)
    image.save(os.path.join(Config.UPLOADS_FOLDER, filename))
    image = filename
    product = Product(title=title, category=category,
                      price=price, description=description,
                      image=image)
    try:
        db.session.add(product)
        db.session.commit()
        flash('{} added successfully!'.format(title))
        return redirect(url_for('product_page'))
    except Exception as e:
        flash('Processing error! {}'.format(e))
        return render_template('add-product.html')


@app.route('/add-new-product')
def add_product_page():
    user = check_login()
    if user is None:
        return redirect(url_for('login'))
    return render_template('add-product.html')


@app.route('/success')
def success():
    user = check_login()
    return render_template('success.html', user=user)


@app.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'GET':
        return render_template('sign-up.html')
    else:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if username == '':
            flash('Please enter username!')
        elif password == '':
            flash('Please enter password')
        elif len(password) < 6:
            flash('Password must be more than 6 characters.')
        elif email == '':
            flash('Please enter email')
        else:
            exists = User.query.filter_by(email=email).first()
            if exists is not None:
                flash('Email address used for another account.')
                return render_template('sign-up.html')
            password_hash = hashlib.sha256(password.encode())
            # the hash string is in hexdigest()
            pw_hash = password_hash.hexdigest()
            user = User(username=username, email=email, password_hash=pw_hash)
            db.session.add(user)
            db.session.commit()
            # python sessions https://pythonbasics.org/flask-sessions/
            session['username'] = username
            session['email'] = email
            resp = redirect(url_for('success'))
            # python sessions https://pythonbasics.org/flask-cookies/
            resp.set_cookie('id', user.id, max_age=timedelta(hours=24))
            resp.set_cookie('password', pw_hash, max_age=timedelta(hours=24))
            return resp

        return render_template('sign-up.html')


@app.route('/logout')
def logout():
    # remove sessions
    session['username'] = None
    session['email'] = None
    # remove cookies
    resp = redirect(url_for('login_page'))
    resp.set_cookie('username', '', expires=0)
    resp.set_cookie('password', '', expires=0)
    return resp


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        pw = hashlib.sha256(password.encode()).hexdigest()
        user = User.query.filter_by(username=username).first()
        if user is not None:
            if user.password_hash == pw:
                # logged in successfully
                session['username'] = username
                session['email'] = user.email
                resp = redirect(url_for('homepage'))
                resp.set_cookie('id', str(user.id), max_age=timedelta(hours=24))
                resp.set_cookie('password', pw, max_age=timedelta(hours=24))
                return resp
        flash('Invalid username or password!')
        return render_template('login.html')


@app.route('/uploads/<filename>')
def view_file(filename):
    return send_from_directory('static/uploads', filename)


@app.route('/delete/<id>')
def delete_product(id):
    user = check_login()
    if user is None:
        return redirect(url_for('login'))
    product = Product.query.filter_by(id=id).first()
    if product is None:
        flash('Product not found')
        return redirect(url_for('product_page'))
    db.session.delete(product)
    db.session.commit()
    flash('{} has been deleted successfully'.format(product.title))
    return redirect(url_for('product_page'))


@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit_product(id):
    user = check_login()
    if user is None:
        return redirect(url_for('login'))
    product = Product.query.filter_by(id=id).first()
    if product is None:
        flash('Product not found')
        return redirect(url_for('product_page'))
    if request.method == 'GET':
        return render_template('edit.html', product=product)

    product.title = request.form['title']
    product.category = request.form['category']
    product.description = request.form['description']
    db.session.commit()
    flash('{} updated successfully'.format(product.title))
    return redirect(url_for('product_page'))