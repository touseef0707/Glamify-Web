# Import necessary modules
from flask import Flask, render_template, request, redirect, url_for
from helpers.dictionary_dataset import dataset
from auth_routes import auth_blueprint
import random
import firebase_admin
from firebase_admin import credentials

app = Flask(__name__)
app.register_blueprint(auth_blueprint)

# Applying configuration of flask    ---To be kept secret---
app.config['SECRET_KEY'] = 'Aaposi@234#*Joids9J89#&^Bvbiux/Biubc8*7'
app.config['RECAPTCHA_ENABLED'] = True
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Lc24ZUpAAAAAMHqBwt9tGgzCiJClilX0WejJvZH'   
app.config['RECAPTCHA_PRIVATE_KEY'] = '6Lc24ZUpAAAAAGyH1juh5bLhxcnxLuuaF6EP70xx'
app.config['RECAPTCHA_TABINDEX'] = 1
app.config['RECAPTCHA_DATA_ATTRS'] = { 'size': 'normal'}

cred = credentials.Certificate("glamify-fbase-secret-key.json")
firebase_admin.initialize_app(cred, {'databaseURL': "https://glamify-0707-default-rtdb.asia-southeast1.firebasedatabase.app/"})


# Route for home page
@app.route('/')
def home():
    fe_items = get_data(1)
    new_items = get_data(1)
    return render_template("home.html", fe_items = fe_items, new_items = new_items)

# fetching random data from the dataset
def get_data(num = 10):
    dataset_men = get_random_data(filter_data(dataset['Men'], 'Innerwear'), num)
    dataset_women = get_random_data(filter_data(dataset['Women'], 'Innerwear'), num)
    dataset_boys = get_random_data(dataset['Boys'], num)
    dataset_girls = get_random_data(dataset['Girls'], num)
    dataset_unisex = get_random_data(dataset['Unisex'], num)
    dataset_final = dataset_men + dataset_women + dataset_boys + dataset_girls + dataset_unisex
    return dataset_final

# function to remove filtered data
def filter_data(list, remove_filter):
    return [d for d in list if d['subCategory'] != remove_filter and d['subCategory']!='Loungewear and Nightwear'] 

def get_random_data(list, num = 10):
    return random.sample(list, num)

# Route for about page
@app.route('/about')
def about():
    return render_template("about.html")

# Route for contact page
@app.route('/contact')
def contact():
    return render_template("contact.html")

# Route for store page
@app.route('/store')
def store():
    fe_items = get_data(4)
    new_items = get_data(4)
    return render_template("store.html", fe_items = fe_items, new_items = new_items)

# Route for product page
@app.route('/product/<gender>/<item_id>')
def product(gender, item_id):
    product_details = get_product_details(gender, item_id)
    fe_items = get_random_data(filter_data(dataset[gender]  , 'Innerwear'), 4)
    return render_template('product.html', product_details=product_details, fe_items=fe_items)

# function to get product details
def get_product_details(gender, item_id):
    for d in dataset[gender]:
        if d['id'] == item_id:
            return d
        

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    # Add code here to add item to the cart
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['POST'])
def buy():
    # Add code here to handle checkout process
    return redirect(url_for('checkout'))

# Route for cart page
@app.route('/cart')
def cart():
    return render_template("cart.html")

@app.route('/order_details')
def order_details():
    return render_template("order_details.html")

user = {"display_name":"rainyjoke","firstname": "Touseef", "lastname": "Ahmed", 
        "email": "touseefahmed0707@gmail.com", "phone": "+971234567890",
        "address" : "ABCD 1234 Street"}

orders = [{"id": "1", "date": "2021-07-07", "total": "1000", "status": "Delivered"},
          {"id": "2", "date": "2021-07-07", "total": "2000", "status": "Delivered"},
          {"id": "3", "date": "2021-07-07", "total": "3000", "status": "Delivered"}]

@app.route('/profile')
def profile():
    return render_template("profile.html", user = user, orders = orders)

@app.route('/checkout')
def checkout():
    return render_template("checkout.html")

@app.route('/wishlist')
def wishlist():
    wishlist = get_data(1)
    return render_template("wishlist.html", fe_items = wishlist)



if __name__ == '__main__':
    app.run(debug=True)
