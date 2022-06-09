from flask import request, redirect, render_template, session

from pypos.blueprints.auth.util import login_required
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

## Owner
@bp.route('/canteen/manage-employees')
@login_required(permissions=['acess_product_management'])
def manage_employees():
    return render_template("user/management_employees.html")

@bp.route('/canteen/settings')
@login_required(permissions=['acess_product_management'])
def canteen_settings():
    return render_template("user/settings_canteen.html")

## Manager
@bp.route('/canteen/manage-products')
@login_required(permissions=['acess_product_management'])
def manage_products():
    return render_template("user/management_products.html")

@bp.route('/canteen/manage-products/add_product')
@login_required(permissions=['acess_product_management'])
def manage_products_add_product():
    return render_template("user/management_products_add_product.html")

@bp.route('/canteen/manage-products/add_category')
@login_required(permissions=['acess_product_management'])
def manage_products_add_category():
    return render_template("user/management_products_add_category.html")

@bp.route('/canteen/manage-products/update_product')
@login_required(permissions=['acess_product_management'])
def manage_products_update_product():
    return render_template("user/management_products_update_product.html")

@bp.route('/canteen/manage-products/update_category')
@login_required(permissions=['acess_product_management'])
def manage_products_update_category():
    return render_template("user/management_products_update_category.html")

## Cashier
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