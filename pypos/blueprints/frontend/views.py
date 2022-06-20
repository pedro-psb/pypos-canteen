import json
from re import L
from unicodedata import category
from flask import request, redirect, render_template, session

from pypos.blueprints.auth.util import login_required, get_db, public_acess_only
from . import bp

# Public


@bp.route('/index')
@bp.route('/')
def index():
    return render_template("public/index.html")

@bp.route('/user/choose_role')
@public_acess_only
def choose_role():
    return render_template("public/choose_role.html")

@bp.route('/register')
@public_acess_only
def register_client():
    return render_template("public/register_client.html")

@bp.route('/register_employee')
def register_employee():
    return render_template("public/register_employee.html")

@bp.route('/register_canteen')
@public_acess_only
def register_canteen():
    return render_template("public/register_canteen.html")


@bp.route('/login')
@public_acess_only
def login():
    return render_template("public/login.html")

# Common


@bp.route('/user-settings')
@login_required(permissions=['acess_product_management'])
def user_settings():
    return render_template("user/settings_user.html")


@bp.route('/unauthorized')
def unauthorized():
    return render_template("user/unauthorized.html")

# Canteen


@bp.route('/canteen')
@login_required(permissions=['acess_canteen_index'])
def canteen_index():
    return render_template("user/canteen_index.html")

# Owner


@bp.route('/canteen/manage-employees')
@login_required(permissions=['acess_product_management'])
def manage_employees():
    return render_template("user/management_employees.html")


@bp.route('/canteen/settings')
@login_required(permissions=['acess_product_management'])
def canteen_settings():
    return render_template("user/settings_canteen.html")

# Manager


@bp.route('/canteen/manage-products')
@login_required(permissions=['acess_product_management'])
def manage_products():
    db = get_db()
    products_query = "SELECT p.id, p.name, p.price, p.active, pc.name as category_name " \
        "FROM product p LEFT JOIN product_category pc ON p.category = pc.id;"
    categories_query = '''
        SELECT pc.id, pc.name, pc.description, pc.active, COUNT(*) as products_inside
        FROM product_category pc INNER JOIN product p ON p.category = pc.id
        GROUP BY pc.id UNION
        SELECT pc.id, pc.name, pc.description, pc.active, '0' as products_inside
        FROM product_category pc LEFT JOIN product p ON p.category = pc.id
        WHERE p.id IS NULL;
    '''
    all_products = db.execute(products_query)
    all_categories = db.execute(categories_query)
    data = {
        'products': [dict(prod) for prod in all_products],
        'categories': [dict(cat) for cat in all_categories],
    }
    return render_template("user/management_products.html", data=data)


@bp.route('/canteen/manage-products/add_product')
@login_required(permissions=['acess_product_management'])
def manage_products_add_product():
    db = get_db()
    categories_query = "SELECT name, id, active FROM product_category;"
    all_categories = db.execute(categories_query)
    data = {
        'categories': [dict(cat) for cat in all_categories],
    }
    return render_template("user/management_products_add_product.html", data=data)


@bp.route('/canteen/manage-products/add_category')
@login_required(permissions=['acess_product_management'])
def manage_products_add_category():
    return render_template("user/management_products_add_category.html")


@bp.route('/canteen/manage-products/update_product/<int:id>')
@login_required(permissions=['acess_product_management'])
def manage_products_update_product(id):
    db = get_db()
    get_product_query = "SELECT id, name, price, category FROM product WHERE id=?"
    get_category_query = "SELECT id, name FROM product_category WHERE active=1;"

    product = db.execute(get_product_query, (id,)).fetchone()
    all_categories = db.execute(get_category_query).fetchall()
    data = {
        'product': dict(product),
        'categories': [dict(cat) for cat in all_categories],
    }
    return render_template("user/management_products_update_product.html", data=data)


@bp.route('/canteen/manage-products/update_category/<int:id>')
@login_required(permissions=['acess_product_management'])
def manage_products_update_category(id):
    db = get_db()
    get_category_query = "SELECT id, name, description FROM product_category WHERE id=?"
    category = db.execute(get_category_query, (id,)).fetchone()
    data = {
        'category': dict(category),
    }
    return render_template("user/management_products_update_category.html", data=data)

# Cashier


@bp.route('/canteen/point-of-sale')
@login_required(permissions=['acess_pos'])
def pos_main():
    db = get_db()
    products = db.execute('''
        SELECT p.name, p.id, p.price, pc.name as category FROM product p
        LEFT JOIN product_category pc ON p.category = pc.id
        WHERE p.active=1;
    ''').fetchall()
    data = {'products': [dict(prod) for prod in products]}
    return render_template("user/pos_main.html", data=data)


@bp.route('/canteen/reports')
@login_required(permissions=['acess_reports'])
def pos_reports():
    data = {
        'transactions': [
            {
                'date': '12/12/12',
                'products': [
                    {'name': 'Foo', 'quantity': '2'},
                    {'name': 'Bar', 'quantity': '1'},
                    {'name': 'Spam', 'quantity': '4'}
                ],
                'payment_method': 'Money',
                'discount': 2.0,
                'total_value': 23.50
            },
            {
                'date': '13/12/12',
                'products': [
                    {'name': 'Foo', 'quantity': '2'},
                    {'name': 'Spam', 'quantity': '4'}
                ],
                'payment_method': 'Credit Card',
                'discount': 0,
                'total_value': 50
            },
            {
                'date': '14/12/12',
                'products': [
                    {'name': 'Bar', 'quantity': '1'},
                    {'name': 'Spam', 'quantity': '4'}
                ],
                'payment_method': 'Money',
                'discount': 5.0,
                'total_value': 4.78
            }
        ]
    }
    query = """
        SELECT tp.date, pm.name AS payment_method, tp.discount, tp.total_value,
        group_concat('{"name":"' || p.name || '","quantity":"' || tpi.quantity || '"}') AS products
        FROM transaction_product tp
        INNER JOIN transaction_product_item tpi ON tp.id=tpi.transaction_product_id
        INNER JOIN product p ON p.id = tpi.product_id
        INNER JOIN payment_method pm ON tp.payment_method = pm.id
        GROUP BY tp.id;
    """
    db = get_db()
    all_transactions = db.execute(query).fetchall()

    for key, transaction in enumerate(all_transactions):
        transaction_parsed = dict(transaction)
        products_string = transaction_parsed.get('products')
        product_parsed = json.loads(f'[{products_string}]')

        # products_quantities = products_string.split(';')
        # for product_quantity in products_quantities:
        #     product_quantity_split = product_quantity.split(',')
        #     product = product_quantity_split(1)

        transaction_parsed['products'] = product_parsed
        all_transactions[key] = transaction_parsed

    print(all_transactions)
    data = {'transactions': all_transactions}

    return render_template("user/pos_reports.html", data=data)


@bp.route('/canteen/manage-clients')
@login_required(permissions=['acess_client_management'])
def manage_clients():
    return render_template("user/management_clients.html")

# Client


@bp.route('/client')
@login_required(permissions=['acess_client_dashboard'])
def client_index():
    return render_template("user/client_index.html")


@bp.route('/client/manage')
@login_required(permissions=['acess_client_dashboard'])
def client_manage():
    return render_template("user/client_manage.html")

# AJAX


@bp.route('/pos/get_products')
@login_required(permissions=['acess_pos'])
def get_products():
    data = [
        {
            'category': 'lunch',
            'products': [
                {'name': 'Rice', 'price': 12.50, 'id': 1},
                {'name': 'Beans', 'price': 20, 'id': 2},
            ]
        },
        {
            'category': 'breakfast',
            'products': [
                {'name': 'Bread and Milk', 'price': 22.50, 'id': 3},
                {'name': 'Pão de Queijo', 'price': 1.50, 'id': 4},
            ]
        },
    ]
    return render_template("user/pos_main.html", data=data)
