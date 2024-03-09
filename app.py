from flask import Flask, render_template
from helpers.dictionary_dataset import dataset

import random

app = Flask(__name__)

# Applying configuration of flask    ---To be kept secret---
app.config['SECRET_KEY'] = 'Aaposi@234#*Joids9J89#&^Bvbiux/Biubc8*7'
app.config['RECAPTCHA_ENABLED'] = True
app.config['RECAPTCHA_PUBLIC_KEY'] = '5ids9J89#&^Bvbiux/BiubcvD3V5FfJGv4Z3YDp2YzK9wv'   
app.config['RECAPTCHA_PRIVATE_KEY'] = '6Ld5JZgUAAAAAExy5vD3V5FfJGv4Z3YDp2YzK9wv'
app.config['RECAPTCHA_TABINDEX'] = 1
app.config['RECAPTCHA_DATA_ATTRS'] = {'theme': 'dark', 'size': 'compact'}

@app.route('/')
def home():
    
    fe_items = get_data(1)
    new_items = get_data(1)
    return render_template("home.html", fe_items = fe_items, new_items = new_items)

def get_data(num = 10):
    dataset_men = get_random_data(filter_data(dataset['Men'], 'Innerwear'), num)
    dataset_women = get_random_data(filter_data(dataset['Women'], 'Innerwear'), num)
    dataset_boys = get_random_data(dataset['Boys'], num)
    dataset_girls = get_random_data(dataset['Girls'], num)
    dataset_unisex = get_random_data(dataset['Unisex'], num)
    dataset_final = dataset_men + dataset_women + dataset_boys + dataset_girls + dataset_unisex
    return dataset_final

def filter_data(list, remove_filter):
    return [d for d in list if d['subCategory'] != remove_filter]

def get_random_data(list, num = 10):
    return random.sample(list, num)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/store')
def store():
    fe_items = get_data(4)
    new_items = get_data(4)
    return render_template("store.html", fe_items = fe_items, new_items = new_items)

@app.route('/product/<gender>/<item_id>')
def product(gender, item_id):
    product_details = get_product_details(gender, item_id)
    fe_items = get_random_data(filter_data(dataset[gender]  , 'Innerwear'), 4)
    return render_template('product.html', product_details=product_details, fe_items=fe_items)


def get_product_details(gender, item_id):
    for d in dataset[gender]:
        if d['id'] == item_id:
            return d

@app.route('/cart')
def cart():
    return render_template("cart.html")

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/signin')
def signin():
    return render_template("signin.html")


if __name__ == '__main__':
    app.run(debug=True)
