import json
from pprint import pprint
from flask import render_template, session

from pypos.blueprints.auth.util import login_required, get_db, public_acess_only
from pypos.models import dao
from pypos.models.client_transaction_model import ClientTransaction
from pypos.models.transactions_dao import Product, RegularPurchase, UserAccountPurchase, UserRecharge
from . import bp

# Public

PAYMENT_METHODS = [
    ('cash', 'Cash'), ('debit_card', 'Debit Card'), ('pix', 'PIX'),
    ('credit_card', 'Credit Card'), ('user_account', 'User Account')
]
PAYMENT_METHODS_NO_USER = [
    ('cash', 'Cash'), ('debit_card', 'Debit Card'),
    ('credit_card', 'Credit Card'), ('pix', 'PIX'),
]


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
    data = {'employees': get_all_employees()}
    return render_template("user/management_employees.html", data=data)


@bp.route('/canteen/add-employee')
def manage_employees_add():
    data = {
        'roles': get_all_roles()
    }
    return render_template("user/management_employees_add.html", data=data)


@bp.route('/canteen/update-employee/<int:id>')
def manage_employees_update(id):
    data = {
        'employee': get_user_by_id(id),
        'roles': get_all_roles()
    }
    return render_template("user/management_employees_update.html", data=data)


@bp.route('/canteen/settings')
@login_required(permissions=['acess_product_management'])
def canteen_settings():
    return render_template("user/settings_canteen.html")


# Manager


@bp.route('/canteen/manage-products')
@login_required(permissions=['acess_product_management'])
def manage_products():
    db = get_db()
    canteen_id = session.get('canteen_id')

    products_query = """
        SELECT p.id, p.name, p.price, p.active, pc.name as category_name
        FROM product p LEFT JOIN product_category pc ON p.category = pc.id
        WHERE p.canteen_id=?;
    """
    categories_query = '''
        SELECT pc.id, pc.name, pc.description, pc.active, COUNT(*) as products_inside
        FROM product_category pc INNER JOIN product p ON p.category = pc.id
        GROUP BY pc.id HAVING p.canteen_id=? UNION
        SELECT pc.id, pc.name, pc.description, pc.active, '0' as products_inside
        FROM product_category pc LEFT JOIN product p ON p.category = pc.id
        WHERE p.id IS NULL AND pc.canteen_id=?;
    '''
    all_products = db.execute(products_query, (canteen_id,))
    all_categories = db.execute(categories_query, (canteen_id, canteen_id))
    data = {
        'products': [dict(prod) for prod in all_products],
        'categories': [dict(cat) for cat in all_categories],
    }
    return render_template("user/management_products.html", data=data)


@bp.route('/canteen/manage-products/add_product')
@login_required(permissions=['acess_product_management'])
def manage_products_add_product():
    db = get_db()
    canteen_id = session.get('canteen_id')

    categories_query = "SELECT name, id, active FROM product_category WHERE canteen_id=?;"
    all_categories = db.execute(categories_query, (canteen_id,))
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
    canteen_id = session.get('canteen_id')

    get_product_query = "SELECT id, name, price, category FROM product WHERE id=? AND canteen_id=?"
    get_category_query = "SELECT id, name FROM product_category WHERE active=1 AND canteen_id=?;"

    product = db.execute(get_product_query, (id, canteen_id)).fetchone()
    all_categories = db.execute(get_category_query, (canteen_id,)).fetchall()
    data = {
        'product': dict(product),
        'categories': [dict(cat) for cat in all_categories],
    }
    return render_template("user/management_products_update_product.html", data=data)


@bp.route('/canteen/manage-products/update_category/<int:id>')
@login_required(permissions=['acess_product_management'])
def manage_products_update_category(id):
    db = get_db()
    canteen_id = session.get('canteen_id')

    get_category_query = """
        SELECT id, name, description FROM product_category
        WHERE id=? AND canteen_id=?;
    """
    category = db.execute(get_category_query, (id, canteen_id)).fetchone()
    data = {
        'category': dict(category),
    }
    return render_template("user/management_products_update_category.html", data=data)

# Cashier


@bp.route('/canteen/point-of-sale')
@login_required(permissions=['acess_pos'])
def pos_main():
    db = get_db()
    canteen_id = session.get('canteen_id')
    data = {
        'products': dao.get_product_list_by_canteen_id(canteen_id),
        'payment_methods': PAYMENT_METHODS,
        'user_list': dao.get_client_list_by_canteen_id(canteen_id)
    }
    return render_template("user/pos_main.html", data=data)


@bp.route('/canteen/reports')
@login_required(permissions=['acess_reports'])
def pos_reports():
    # TODO make a link to the transaction details with a popover
    canteen_id = session.get('canteen_id')

    all_transactions = dao.get_all_transactions_by_canteen_id(canteen_id)
    pending_transactions = [t for t in all_transactions if t['pending']]
    regular_transactions = [t for t in all_transactions if not t['pending']]
    data = {
        'transactions': regular_transactions,
        'pending_transactions': pending_transactions
    }
    return render_template("user/pos_reports.html", data=data)


@bp.route('/canteen/manage-clients')
@login_required(permissions=['acess_client_management'])
def manage_clients():
    canteen_id = session['canteen_id']
    clients = dao.get_client_list_by_canteen_id(canteen_id)
    data = {
        'clients': clients
    }
    return render_template("user/management_clients.html", data=data)


@bp.route('/canteen/manage-clients/add')
@login_required(permissions=['acess_client_management'])
def manage_clients_add():
    return render_template("user/management_clients_add.html")


@bp.route('/canteen/manage-clients/recharge/<int:account_id>')
@login_required(permissions=['acess_client_management'])
def manage_clients_recharge(account_id):
    data = {
        "account_id": account_id,
        "payment_methods": PAYMENT_METHODS_NO_USER
    }
    return render_template("user/management_clients_recharge.html", data=data)


# Client


@bp.route('/client')
@login_required(permissions=['acess_client_dashboard'])
def client_index():
    user_id = session['user_id']
    data = {
        'transactions': dao.get_all_transactions_by_user_id(user_id),
        'balance': dao.get_user_balance_by_id(user_id)
    }
    return render_template("user/client_index.html", data=data)


@bp.route('/client/manage')
@login_required(permissions=['acess_client_dashboard'])
def client_manage():
    canteen_id = session['canteen_id']
    user_child_list = dao.get_user_child_list(canteen_id)
    data = {
        'user_child_list': user_child_list,
    }
    return render_template("user/client_manage.html", data=data)


@bp.route('/client/manage/add_dependent')
@login_required(permissions=['acess_client_dashboard'])
def client_manage_add():
    return render_template("user/client_manage_add.html")


@bp.route('/client/manage/update_dependent/<int:user_id>')
@login_required(permissions=['acess_client_dashboard'])
def client_manage_update(user_id):
    user_data = dao.get_user_by_id(user_id)
    user_data = stringify_nones_in_dict(user_data)
    return render_template('user/client_manage_update.html', data=user_data)


def stringify_nones_in_dict(data: dict) -> dict:
    for k, v in data.items():
        if not v:
            data[k] = ""
    return data


@bp.route('/client/deposit')
@login_required(permissions=['acess_client_dashboard',
                             'acess_client_account_management'])
def client_deposit():
    data = {
        'payment_methods': PAYMENT_METHODS_NO_USER
    }
    return render_template("user/client_deposit.html", data=data)


def select_non_employee_roles():
    # select employee roles based on fixed non-emplyed roles
    not_employee_roles = ["owner", "client",
                          "client_dependent", "temporary_client"]
    not_employee_roles = map(lambda x: f"'{x}'", not_employee_roles)
    not_employee_roles = f"({','.join(not_employee_roles)})"
    return not_employee_roles


def get_all_employees():
    db = get_db()
    not_employee_roles = select_non_employee_roles()
    query = f"SELECT * FROM user WHERE role_name NOT IN {not_employee_roles} AND active=1;"
    all_employees = db.execute(query).fetchall()
    all_employees = [dict(employee) for employee in all_employees]
    return all_employees


def get_all_roles():
    db = get_db()
    not_employee_roles = select_non_employee_roles()
    query = f"SELECT * FROM role WHERE name NOT IN {not_employee_roles};"
    all_roles = db.execute(query).fetchall()
    all_roles = [dict(role) for role in all_roles]
    return all_roles


def get_user_by_id(id):
    db = get_db()
    query = "SELECT * FROM user WHERE id=?;"
    user = db.execute(query, (id,)).fetchone()
    user = dict(user)
    return user
