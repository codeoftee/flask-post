# flask project
from datetime import timedelta

from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

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
    return render_template('all_products.html')


@app.route('/add-product', methods=['POST'])
def add_product():
    title = request.form['title']
    price = request.form['price']

    return redirect(url_for('product_page'))


@app.route('/add-product-page')
def add_product_page():
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
                resp.set_cookie('id', user.id, max_age=timedelta(hours=24))
                resp.set_cookie('password', pw, max_age=timedelta(hours=24))
                return resp
        flash('Invalid username or password!')
        return render_template('login.html')
