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

# Owner
@bp.route('/canteen/manage-employees')
@login_required(permissions=['acess_product_management'])
def manage_emplyess():
    return render_template("user/management_employees.html")

@bp.route('/canteen/settings')
@login_required(permissions=['acess_product_management'])
def canteen_settings():
    return render_template("user/settings_canteen.html")

# Manager
@bp.route('/canteen/manage-products')
@login_required(permissions=['acess_product_management'])
def manage_products():
    return render_template("user/management_products.html")

# Cashier
@bp.route('/canteen/point-of-sale')
@login_required(permissions=['acess_pos'])
def pos_main():
    return render_template("user/pos_main.html")

@bp.route('/canteen/reports')
@login_required(permissions=['acess_pos'])
def pos_reports():
    return render_template("user/pos_reports.html")

@bp.route('/canteen/manage-clients')
@login_required(permissions=['acess_pos'])
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