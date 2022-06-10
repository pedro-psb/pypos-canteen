from flask import request, redirect, render_template, session

from pypos.blueprints.auth.util import login_required, get_db
from . import bp

# Public


@bp.route('/index')
@bp.route('/')
def index():
    return render_template("public/index.html")


@bp.route('/register')
def register():
    return render_template("public/register.html")


@bp.route('/login')
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


@bp.route('/canteen/manage-products/update_category')
@login_required(permissions=['acess_product_management'])
def manage_products_update_category():
    return render_template("user/management_products_update_category.html")

# Cashier


@bp.route('/canteen/point-of-sale')
@login_required(permissions=['acess_pos'])
def pos_main():
    return render_template("user/pos_main.html")


@bp.route('/canteen/reports')
@login_required(permissions=['acess_reports'])
def pos_reports():
    return render_template("user/pos_reports.html")


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
