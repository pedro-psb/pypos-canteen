from flask import request, redirect, render_template, session

from pypos.blueprints.auth.util import login_required
from . import bp

# Common
@bp.route('/index')
@bp.route('/')
def index():
    return render_template("public/index.html")

@bp.route('/register')
def register():
    return render_template("auth/register.html")

@bp.route('/login')
def login():
    return render_template("auth/login.html")

# Manager
@bp.route('/product_management')
@login_required(permissions=['acess_product_management'])
def product_management():
    return render_template("product/index.html")

# Cashier
@bp.route('/poin_of_sale')
@login_required(permissions=['acess_pos'])
def pos_interface():
    return render_template("pos/index.html")

# Client
@bp.route('/client_dashboard')
@login_required(permissions=['acess_client_dashboard'])
def client_dashboard():
    return render_template("client/index.html")