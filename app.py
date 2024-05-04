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
    
    # Get ten random items from the dataset 
    items = get_data(10)
     
    # Apply search filter if search query is provided
    if search_query:
        items = [item for item in all_items if search_query.lower() in item['productDisplayName'].lower()]
    
    # Apply all other filters
    filtered_items = apply_all_filters(items, filters)
    
    return render_template("store.html", fe_items=filtered_items)

# Route to handle adding items to wishlist
@app.route('/add_to_wishlist', methods=['POST'])
def add_to_wishlist():

    # Get the item ID from the request data
    data = request.get_json()
    item_id = data['itemId']
    data = get_product_data(all_items, item_id)

    # try to add the item to the wishlist in the database
    try:
        db.reference("/wishlist").child(item_id).set(data)
        return jsonify({'success': True, 'message': 'Item added to cart successfully'}), 200
    
    # If an error occurs, return the error message
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    
# Route to handle adding items to cart
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

    # Get the product details for the item ID
    product_details = get_product_data(all_items, item_id)

    # Get 4 related random products
    fe_items = get_random_data(filter_data(dataset[gender]  , 'Innerwear'), 4)

    return render_template('product.html', product_details=product_details, fe_items=fe_items, item_id=item_id)

# Route for cart page
@app.route('/cart')
def cart():

    # Get the user ID from the session
    user_id = session.get("user_id")

    # If user is not logged in, redirect to login page
    if not user_id:
        return redirect(url_for('auth.auth_login'))
    
    # Get the user object from Firebase Authentication
    user = auth.get_user(user_id)

    # Get the cart items from the database and update the neccessary lists and values to render the cart page
    product_data_list = []
    username = user.display_name
    ref = db.reference(f"/users/{username}/cart")
    cart_items = ref.get()
    total_sum, tax, grand_total, shipping = 0, 0, 0, 0

    if cart_items:
        for product_id, product_data in cart_items.items():
            product_data['price'] = float(product_data['price'])
            product_data['quantity'] = int(product_data['quantity'])
            product_data_list.append(product_data)
            total_sum += product_data['price'] * product_data['quantity']

        tax = round(0.05 * total_sum, 2)
        shipping = 15
        grand_total = total_sum + tax + shipping

    return render_template("cart.html", product_data_list=product_data_list, total_sum=total_sum, tax=tax, shipping=shipping, grand_total=grand_total)
      
# function to check if cart is not empty
def check_cart_empty(username):
    cart_items = db.reference(f"/users/{username}/cart").get()
    if not cart_items:
        return True
    return False

# Route to checkout page
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():

    # Get the source of the request
    source = request.args.get('source')

    # Get the user ID from the session if present else send to login page
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for('auth.auth_login'))

    # Get the user object from Firebase Authentication and login session
    user = auth.get_user(user_id)
    username = user.display_name

    # If the source is product page and the request method is POST
    if source == 'product' and request.method == 'POST':

        # Get the product ID and quantity from the form data
        product_id = request.form['product_id']
        quantity = int(request.form['quantity'])

        # Get the product data for the product ID
        product_data = get_product_data(all_items, product_id)
        product_data['price'] = float(product_data['price'])
        product_data['quantity'] = quantity

        # update neccessary values to render the checkout page
        total_sum = product_data['price'] * quantity
        tax = round(0.05 * total_sum, 2)
        shipping = 15
        grand_total = total_sum + tax + shipping

        return render_template('checkout.html', product_data_list=[product_data], quantities=[quantity], total_sum=total_sum, tax=tax, shipping=shipping, grand_total=grand_total)
    
    # If the source is cart page and the request method is POST and the cart is not empty
    elif source == 'cart' and request.method == 'POST' and not check_cart_empty(username):

        # Get the cart items from the database
        cart_items = db.reference(f"/users/{username}/cart").get()

        # Initialize empty lists for product data's and quantities
        product_data_list = []
        quantities = []

        # If cart items exist
        if cart_items:
            total_sum = 0
            # Loop through the cart items and append the product data and quantity to the lists
            for product_id, product_data in cart_items.items():
                product_data['price'] = float(product_data['price'])
                product_data_list.append(product_data)
                quantities.append(int(product_data['quantity']))
                total_sum += product_data['price'] * int(product_data['quantity'])
            tax = round(0.05 * total_sum, 2)
            shipping = 15
            grand_total = total_sum + tax + shipping
            # Render the checkout page template with the product data and quantities
            return render_template('checkout.html', product_data_list=product_data_list, quantities=quantities, total_sum=total_sum, tax=tax, shipping=shipping, grand_total=grand_total)
    
    else:
        return redirect(url_for('cart'))

# function to calculate the total sum, tax, shipping and grand total
def calculate_cart_total(cart_items):

    total_sum = 0
    if cart_items:
        for product_id, product_data in cart_items.items():
            product_data['price'] = float(product_data['price'])
            product_data['quantity'] = int(product_data['quantity'])
            total_sum += product_data['price'] * product_data['quantity']

    tax = round(0.05 * total_sum, 2)
    shipping = 15
    grand_total = total_sum + tax + shipping

    return total_sum, tax, shipping, grand_total

# function to get the orders from the database
def get_orders(username):
    orders = db.reference(f"/users/{username}/orders").get()
    return orders

# function to get the number of orders from the database
def len_orders(username):
    orders = db.reference(f"/users/{username}/orders").get()
    if orders:
        return len(orders)
    return 0

# Route to complete order
@app.route('/complete_order', methods=['POST'])
def complete_order():

    # Get the user ID from the session
    user_id = session.get("user_id")
    user = auth.get_user(user_id)
    username = user.display_name

    # Get the cart items from the database
    cart_items = db.reference(f"/users/{username}/cart").get()
    total_sum, tax, shipping, grand_total = calculate_cart_total(cart_items)

    # Generate the order ID, order date, order time and order status
    order_id = f"{username}_{len_orders(username) + 1}"
    import datetime
    order_date = datetime.datetime.now().strftime("%Y-%m-%d")
    order_time = datetime.datetime.now().strftime("%H:%M:%S")
    order_status = "Order Placed"

    # Get the user data from the form data
    data = request.json
    fullname = data['fullname']
    phone = data['phone']
    address = data['address']
    city = data['city']
    zipcode = data['zipcode']

    # set the cart_items to the orders
    basic_ref = f"/users/{username}/orders/{order_id}"
    db.reference(basic_ref+"/order_id").set(order_id)
    db.reference(basic_ref+"/total").set(grand_total)
    db.reference(basic_ref+"/sub_total").set(total_sum)
    db.reference(basic_ref+"/tax").set(tax)
    db.reference(basic_ref+"/shipping").set(shipping)
    db.reference(basic_ref+"/status").set(order_status)
    db.reference(basic_ref+"/date").set(order_date)
    db.reference(basic_ref+"/time").set(order_time)
    db.reference(basic_ref+"/products").set(cart_items)
    db.reference(basic_ref+"/address").set(address)
    db.reference(basic_ref+"/city").set(city)
    db.reference(basic_ref+"/zipcode").set(zipcode)
    db.reference(basic_ref+"/phone").set(phone)
    db.reference(basic_ref+"/fullname").set(fullname)
    db.reference(basic_ref+"/username").set(username)

    #delete the cart upon successfull order completion
    db.reference(f"/users/{username}/cart").delete()

    # redirect to the home page
    return redirect(url_for('home'))

# function to get the orders from the database
def get_orders(username):
    orders = db.reference(f"/users/{username}/orders").get()
    return orders

# function to get the order details from the database
def get_order_details(username, order_id):
    order = db.reference(f"/users/{username}/orders/{order_id}").get()
    return order


# Route for order details page
@app.route('/order_details/<order_id>')
def order_details(order_id):

    # Get the user object from Firebase Authentication and login session
    user = auth.get_user(session.get("user_id"))
    username = user.display_name
    order = get_order_details(username, order_id)

    # If order exists, render the order details page
    if order:
        return render_template('order_details.html', order=order)
    else:
        return 'Order not found', 404

# Route for profile page
@app.route('/profile')
def profile():
    # Get the user object from Firebase Authentication and login session
    user = auth.get_user(session.get("user_id"))
    display_name = user.display_name

    # update the user object with the data from the database
    user = db.reference("/users").child(user.display_name).get()
    orders = get_orders(display_name)

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