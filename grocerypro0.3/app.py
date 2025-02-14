from flask import Flask, render_template, request, redirect, url_for, flash
import pdfkit
import os
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from flask_login import login_required
import secrets
from flask import flash
from flask_sqlalchemy import SQLAlchemy

def add_static_products():
    product_info = {
    "Brown_sugar": {"unit": "kg", "price": 5},
    "buttermilk": {"unit": "pac", "price": 2},
    "vegetable_masala": {"unit": "pac", "price": 3},
    "washing_powder": {"unit": "pac", "price": 4},
    "salt": {"unit": "kg", "price": 1},
    "poha": {"unit": "kg", "price": 2},
    "oil": {"unit": "ltr", "price": 5},
    "tooth_paste": {"unit": "pac", "price": 2},
    "hair_conditioner": {"unit": "pac", "price": 6},
    "wheat_flour": {"unit": "kg", "price": 3},
    "red_chilli": {"unit": "pac", "price": 2},
    "jaggery": {"unit": "kg", "price": 4},
    "coffee": {"unit": "pac", "price": 5},
    "tea": {"unit": "pac", "price": 3},
    "butter": {"unit": "kg", "price": 8},
    "buttermilk_powder": {"unit": "pac", "price": 4},
    "turmeric_powder": {"unit": "pac", "price": 3},
    "hair_oil": {"unit": "ltr", "price": 7},
    "ghee": {"unit": "kg", "price": 10},
    "face_powder": {"unit": "pac", "price": 5},
    }
    existing_products = Product.query.all()

    # If not, add them to the database
    if not existing_products:
        for product_name, product_data in product_info.items():
            new_product = Product(name=product_name, price=product_data['price'])
            db.session.add(new_product)

        db.session.commit()
        flash('Static products added to the database!', 'success')


secret_key = secrets.token_hex(16)
print(secret_key)
app = Flask(__name__)
login_manager = LoginManager(app)
app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    def __init__(self, user_id):
        self.id = user_id
    id = db.Column(db.Integer, primary_key=True)    

    def get_id(self):
        return str(self.id)  

    


               
product_info = {
    "Brown_sugar": {"unit": "kg", "price": 5},
    "buttermilk": {"unit": "pac", "price": 2},
    "vegetable_masala": {"unit": "pac", "price": 3},
    "washing_powder": {"unit": "pac", "price": 4},
    "salt": {"unit": "kg", "price": 1},
    "poha": {"unit": "kg", "price": 2},
    "oil": {"unit": "ltr", "price": 5},
    "tooth_paste": {"unit": "pac", "price": 2},
    "hair_conditioner": {"unit": "pac", "price": 6},
    "wheat_flour": {"unit": "kg", "price": 3},
    "red_chilli": {"unit": "pac", "price": 2},
    "jaggery": {"unit": "kg", "price": 4},
    "coffee": {"unit": "pac", "price": 5},
    "tea": {"unit": "pac", "price": 3},
    "butter": {"unit": "kg", "price": 8},
    "buttermilk_powder": {"unit": "pac", "price": 4},
    "turmeric_powder": {"unit": "pac", "price": 3},
    "hair_oil": {"unit": "ltr", "price": 7},
    "ghee": {"unit": "kg", "price": 10},
    "face_powder": {"unit": "pac", "price": 5},
}

cart = []

total_bill = sum(float(request.form.get(f'price_{product}', 0)) for product in cart)

@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html', product_info=product_info)

@app.route('/update_prices', methods=['POST'])
def update_prices():
    for product in request.form:
        product_info[product]['price'] = float(request.form[product])

    # You may want to save the updated prices to a database or file

    return redirect(url_for('admin'))

@app.route('/add_product', methods=['POST'])
def add_product():
    new_product = request.form['new_product']
    new_price = float(request.form['new_price'])

    # Add the new product to your product_info dictionary
    product_info[new_product] = {'price': new_price}

    # You may want to save the updated product list to a database or file

    return redirect(url_for('admin'))

login_manager.login_view = 'login'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Replace the following with your actual user authentication logic
        if username == 'Amal123' and password == 'Amal@123':
            user_id = '1'
            login_user(User(user_id))
            flash('Login successful!', 'success')
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash('Invalid username or password', 'error')

    # If it's a GET request or login fails, render the login template
    return render_template('login.html')

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/')
def index():
    return render_template('index.html', product_info=product_info, cart=cart, total_bill=total_bill)

@app.route('/logout')
def logout():
    logout_user()
    flash('Logout successful!', 'success')
    return redirect(url_for('index')) 

@app.route('/show_details', methods=['POST'])
def show_details():
    selected_product = request.form.get('product')
    return render_template('index.html', product_info=product_info, selected_product=selected_product, cart=cart, total_bill=total_bill)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    selected_product = request.form.get('selected_product')
    quantity = int(request.form.get('quantity'))
    price = product_info[selected_product]['price']
    cart.append({'product': selected_product, 'quantity': quantity, 'price': price * quantity})
    total_bill = sum(item['price'] for item in cart)
    return redirect(url_for('index'))

@app.route('/billing', methods=['GET', 'POST'])
def billing():
    if request.method == 'POST':
        total_bill = sum(float(request.form.get(f'price_{product}', 0)) for product in cart)
        rendered_html = render_template('billing.html', cart=cart, total_bill=sum(item['price'] for item in cart))
        wkhtmltopdf_path = r'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
        config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
        pdf = pdfkit.from_string(rendered_html, False, configuration=config)
        response = app.response_class(pdf, content_type='application/pdf')
        response.headers['Content-Disposition'] = 'inline; filename=bill.pdf'
        return response
    return render_template('billing.html', cart=cart, total_bill=sum(item['price'] for item in cart))

if __name__ == '__main__':
    app.run(debug=True)
