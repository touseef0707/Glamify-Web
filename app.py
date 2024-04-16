# Import necessary modules
from flask import Flask, render_template, request, redirect, url_for
from helpers.dictionary_dataset import dataset
from auth_routes import auth_blueprint
import random
import firebase_admin
from firebase_admin import credentials, auth, db

# Initialize Flask app
app = Flask(__name__)
app.register_blueprint(auth_blueprint)

# Applying configuration of flask    ---To be kept secret---
app.config['SECRET_KEY'] = 'Aaposi@234#*Joids9J89#&^Bvbiux/Biubc8*7'
app.config['RECAPTCHA_ENABLED'] = True
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Lc24ZUpAAAAAMHqBwt9tGgzCiJClilX0WejJvZH'   
app.config['RECAPTCHA_PRIVATE_KEY'] = '6Lc24ZUpAAAAAGyH1juh5bLhxcnxLuuaF6EP70xx'
app.config['RECAPTCHA_TABINDEX'] = 1
app.config['RECAPTCHA_DATA_ATTRS'] = { 'size': 'normal'}

# Initialize Firebase
cred = credentials.Certificate("glamify-fbase-secret-key.json")
firebase_admin.initialize_app(cred, {'databaseURL': "https://glamify-0707-default-rtdb.asia-southeast1.firebasedatabase.app/"})


# Route for home page
@app.route('/')
def home():
    fe_items = get_data(1)
    new_items = get_data(1)
    return render_template("home.html", fe_items = fe_items, new_items = new_items)

# function to get data according to numbers specified
def get_data(num = 10):
    # filtered out innerwears :)
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

# function to get random data
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
    # Get the search query from the form submission
    search_query = request.args.get('search')
    
    # Get filter options from the form submission
    filters = {
        'gender': request.args.get('gender', '').lower(),
        'masterCategory': request.args.get('master_category', '').lower(),
        'subCategory': request.args.get('sub_category', '').lower(),
        'season': request.args.get('season', '').lower(),
        'usage': request.args.get('occasion', '').lower(),
        'baseColour': request.args.get('color', '').lower()
    }
    
    # Get all items
    items = get_data(100)
    
    # Apply search filter if search query is provided
    if search_query:
        items = [item for item in items if search_query.lower() in item['productDisplayName'].lower()]
    
    # Apply all other filters
    filtered_items = apply_all_filters(items, filters)
    
    return render_template("store.html", fe_items=filtered_items)

def apply_all_filters(products, filters):
    filtered_products = products
    
    # Apply each filter
    for key, value in filters.items():
        if value:
            filtered_products = [item for item in filtered_products if item[key].lower() == value]
    
    return filtered_products


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

# Route for order details page
@app.route('/order_details')
def order_details():
    return render_template("order_details.html")

# dummy user information and orders
user = {"display_name":"rainyjoke","firstname": "Touseef", "lastname": "Ahmed", 
        "email": "touseefahmed0707@gmail.com", "phone": "+971234567890",
        "address" : "ABCD 1234 Street"}

orders = [{"id": "1", "date": "2021-07-07", "total": "1000", "status": "Delivered"},
          {"id": "2", "date": "2021-07-07", "total": "2000", "status": "Delivered"},
          {"id": "3", "date": "2021-07-07", "total": "3000", "status": "Delivered"}]

# Route for profile page
@app.route('/profile')
def profile():
    return render_template("profile.html", user = user, orders = orders)

# Route for checkout page
@app.route('/checkout')
def checkout():
    return render_template("checkout.html")

# Route for wishlist page
@app.route('/wishlist')
def wishlist():
    wishlist = get_data(1)
    return render_template("wishlist.html", fe_items = wishlist)

# Function to delete user from Firebase Authentication and Realtime Database
def delete_user(user_id):
    try:
        # Get user object
        user = auth.get_user(user_id)
        # Delete user from Firebase Authentication
        auth.delete_user(user_id)
        # Delete user from Firebase Realtime Database
        db.reference("/users").child(user.display_name).delete()

    except Exception as e:
        print("User deletion failed:", e)

# delete_user("dX4uGhSITmRoqUosbRxUE1YY3Q13")

if __name__ == '__main__':
    app.run(debug=True)
