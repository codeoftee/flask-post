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

products = []
name = 'Tola'
email = 'tola@pediforte.com'
users = [
    {
        'name': 'Carlos Denver',
        'age': 54,
        'nationality': 'Mexican',
        'email': 'carlos@pediforte.com',
        'id': 0
    },
    {
        'name': 'Messi Cross',
        'age': 24,
        'nationality': 'Spanish',
        'email': 'messi@pediforte.com',
        'id': 1
    }
]


@app.route('/test')
def test_page():
    email = 'tola@pediforte.com'
    fruits = ['Apple', 'Mango', 'Orange', 'Pineapple']
    show_users = 'yes'
    return render_template('test.html', em=email, friuts=fruits,
                           profiles=users, show_users=show_users)


@app.route('/')
def homepage():
    return render_template('home.html', name=name, email=email)


@app.route('/about')
def about_page():
    return "<h1>About Flask page 2</h1>"


@app.route('/products/')
def product_page():
    return render_template('all_products.html', products=products)


@app.route('/add-product', methods=['POST'])
def add_product():
    title = request.form['title']
    price = request.form['price']
    products.append(
        {'title': title, 'price': price,
         'image': 'https://picsum.photos/seed/' + title + '/200/200'}
    )
    return redirect(url_for('product_page'))


@app.route('/add-product-page')
def add_product_page():
    return render_template('add-product.html')


@app.route('/profile/<uid>')
def get_user(uid):
    uid = int(uid)
    profile = users[uid]
    return render_template('profile.html', profile=profile)


@app.route('/success')
def success():
    return render_template('success.html')


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
            resp.set_cookie('username', username, max_age=timedelta(hours=24))
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
                resp.set_cookie('username', username, max_age=timedelta(hours=24))
                resp.set_cookie('password', pw, max_age=timedelta(hours=24))
                return resp
        flash('Invalid username or password!')
        return render_template('login.html')
