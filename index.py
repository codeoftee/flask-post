# flask project
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
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
