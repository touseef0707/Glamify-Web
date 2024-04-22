# Import necessary modules
from flask import Flask, jsonify, render_template, request, redirect, url_for
from helpers.dictionary_dataset import dataset
from helpers.helper_functions import filter_data, get_random_data, apply_all_filters, get_product_data
from auth_routes import auth_blueprint
import random
import firebase_admin
from firebase_admin import credentials, auth, db
from flask import session

# Initialize Flask app
app = Flask(__name__)
@app.template_filter()
def to_int(value):
    return int(value)

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


# get all items into one list
dm = filter_data(dataset['Men'], 'Innerwear')
dw = filter_data(dataset['Women'], 'Innerwear')
all_items =  dm + dw + dataset['Boys'] + dataset['Girls'] + dataset['Unisex']

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
    items = get_data(10)
     
    # Apply search filter if search query is provided
    if search_query:
        items = [item for item in all_items if search_query.lower() in item['productDisplayName'].lower()]
    
    # Apply all other filters
    filtered_items = apply_all_filters(items, filters)
    
    return render_template("store.html", fe_items=filtered_items)

# Route to handle adding items to cart
@app.route('/add_to_wishlist', methods=['POST'])
def add_to_wishlist():
    data = request.get_json()
    item_id = data['itemId']
    data = get_product_data(all_items, item_id)
    print(data)
    try:
        # Add item to the cart collection in Firebase
        db.reference("/wishlist").child(item_id).set(data)
        return jsonify({'success': True, 'message': 'Item added to cart successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    
# Inside your Flask app
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():

    # Get the user object from Firebase Authentication and login session
    user = auth.get_user(session.get("user_id"))
    username = user.display_name

    # Get the item ID and quantity from the request data
    data = request.get_json()

    # Get the product data for the item ID and update quantity field for cart
    product_data = get_product_data(all_items, data['itemId'])
    product_data['quantity'] = data['quantity']

    # try to add the item to the cart in the database
    try:
        db.reference(f"/users/{username}/cart").child(data['itemId']).set(product_data)
        return jsonify({'success': True, 'message': 'Item added to cart successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Route for product page
@app.route('/product/<gender>/<item_id>')
def product(gender, item_id):
    product_details = get_product_data(all_items, item_id)
    fe_items = get_random_data(filter_data(dataset[gender]  , 'Innerwear'), 4)
    return render_template('product.html', product_details=product_details, fe_items=fe_items, item_id=item_id)

# Route for cart page
@app.route('/cart')
def cart():
    return render_template("cart.html")

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    # Get the source of the request
    source = request.args.get('source')

    # Get the user object from Firebase Authentication and login session
    user = auth.get_user(session.get("user_id"))
    username = user.display_name

    # If the source is product page and the request method is POST
    if source == 'product' and request.method == 'POST':

        # Get the product ID and quantity from the form data
        product_id = request.form['product_id']
        quantity = request.form['quantity']

        # Get the product data for the product ID
        product_data = get_product_data(all_items, product_id)
        product_data['quantity'] = quantity

        # Render the checkout page template with the product data and quantity
        return render_template('checkout.html', product_data_list=[product_data], quantities=[quantity])
    
    elif source == 'cart' and request.method == 'POST':

        # Get the cart items from the database
        cart_items = db.reference(f"/users/{username}/cart").get()

        # Initialize empty lists for product data's and quantities
        product_data_list = []
        quantities = []

        # If cart items exist
        if cart_items:

            # Loop through the cart items and append the product data and quantity to the lists
            for item_id, item_data in cart_items.items():
                item_data['price'] = float(item_data['price'])
                product_data_list.append(item_data)
                quantities.append(int(item_data['quantity']))

            # Render the checkout page template with the product data and quantities
            return render_template('checkout.html', product_data_list=product_data_list, quantities=quantities)
        
# Route for order details page
@app.route('/order_details')
def order_details():
    return render_template("order_details.html")

# Sample order data
orders = [{"id": "1", "date": "2021-07-07", "total": "1000", "status": "Delivered"},
          {"id": "2", "date": "2021-07-07", "total": "2000", "status": "Delivered"},
          {"id": "3", "date": "2021-07-07", "total": "3000", "status": "Delivered"}]

# Route for profile page
@app.route('/profile')
def profile():
    # Get the user object from Firebase Authentication and login session
    user = auth.get_user(session.get("user_id"))
    display_name = user.display_name

    # update the user object with the data from the database
    user = db.reference("/users").child(user.display_name).get()

    return render_template("profile.html", user = user, orders = orders, display_name = display_name)

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

if __name__ == '__main__':
    app.run(debug=True)