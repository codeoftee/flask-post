# flask project
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
products = []
name = 'Tola'
email = 'tola@pediforte.com'

@app.route('/')
def homepage():
    return render_template('home.html', name=name, email=email)


@app.route('/about')
def about_page():
    return "<h1>About Flask page 2</h1>"


@app.route('/products/')
def product_page():
    return render_template('products.html', products=products)


@app.route('/add-product', methods=['POST'])
def add_product():
    title = request.form['title']
    price = request.form['price']
    products.append(
        {'title': title, 'price': price,
         'image': 'https://picsum.photos/seed/'+title+'/200/200'}
    )
    return redirect(url_for('product_page'))


@app.route('/add-product-page')
def add_product_page():
    return render_template('add-product.html')
