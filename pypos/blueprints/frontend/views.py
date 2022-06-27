import json
from flask import render_template, session

from pypos.blueprints.auth.util import login_required, get_db, public_acess_only
from pypos.models.client_transaction_model import ClientTransaction
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


@ bp.route('/canteen/manage-products/add_product')
@ login_required(permissions=['acess_product_management'])
def manage_products_add_product():
    db = get_db()
    canteen_id = session.get('canteen_id')

    categories_query = "SELECT name, id, active FROM product_category WHERE canteen_id=?;"
    all_categories = db.execute(categories_query, (canteen_id,))
    data = {
        'categories': [dict(cat) for cat in all_categories],
    }
    return render_template("user/management_products_add_product.html", data=data)


@ bp.route('/canteen/manage-products/add_category')
@ login_required(permissions=['acess_product_management'])
def manage_products_add_category():
    return render_template("user/management_products_add_category.html")


@ bp.route('/canteen/manage-products/update_product/<int:id>')
@ login_required(permissions=['acess_product_management'])
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


@ bp.route('/canteen/manage-products/update_category/<int:id>')
@ login_required(permissions=['acess_product_management'])
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


@ bp.route('/canteen/point-of-sale')
@ login_required(permissions=['acess_pos'])
def pos_main():
    db = get_db()
    canteen_id = session.get('canteen_id')

    products = db.execute('''
        SELECT p.name, p.id, p.price, pc.name as category FROM product p
        LEFT JOIN product_category pc ON p.category = pc.id
        WHERE p.active=1 AND p.canteen_id=?;
    ''', (canteen_id,)).fetchall()
    data = {'products': [dict(prod) for prod in products]}
    return render_template("user/pos_main.html", data=data)


@ bp.route('/canteen/reports')
@ login_required(permissions=['acess_reports'])
def pos_reports():
    canteen_id = session.get('canteen_id')
    query = """
        SELECT tp.date, pm.name AS payment_method, tp.discount, tp.total_value,
        group_concat('{"name":"' || p.name || '","quantity":"' || tpi.quantity || '"}') AS products
        FROM transaction_product tp
        INNER JOIN transaction_product_item tpi ON tp.id=tpi.transaction_product_id
        INNER JOIN product p ON p.id = tpi.product_id
        INNER JOIN payment_method pm ON tp.payment_method = pm.id
        GROUP BY tp.id HAVING p.canteen_id=?;
    """
    db = get_db()
    all_transactions = db.execute(query, (canteen_id,)).fetchall()

    for key, transaction in enumerate(all_transactions):
        transaction_parsed = dict(transaction)
        products_string = transaction_parsed.get('products')
        product_parsed = json.loads(f'[{products_string}]')

        transaction_parsed['products'] = product_parsed
        all_transactions[key] = transaction_parsed

    print(all_transactions)
    data = {'transactions': all_transactions}

    return render_template("user/pos_reports.html", data=data)


@ bp.route('/canteen/manage-clients')
@ login_required(permissions=['acess_client_management'])
def manage_clients():
    return render_template("user/management_clients.html")

# Client


@ bp.route('/client')
@ login_required(permissions=['acess_client_dashboard'])
def client_index():
    transactions = [
        ClientTransaction(
            datetime='2000-12-12 12:12:12',
            transaction_type='deposit',
            value='15.00').dict(),
        ClientTransaction(
            datetime='2000-5-2 6:43:11',
            transaction_type='deposit',
            value='3.43',
            pending=True).dict(),
        ClientTransaction(
            datetime='2001-6-5 1:2:2',
            transaction_type='withdraw',
            value='12.25').dict(),
    ]

    # Sum partial balance
    partial_memory = 0
    for t in transactions:
        if t['transaction_type'] == 'deposit' and not t['pending']:
            partial_memory = partial_memory + t['value']
        elif t['transaction_type'] == 'withdraw':
            partial_memory = partial_memory - t['value']

        t['partial'] = partial_memory

    data = {
        'transactions': transactions
    }
    return render_template("user/client_index.html", data=data)


@ bp.route('/client/manage')
@ login_required(permissions=['acess_client_dashboard'])
def client_manage():
    return render_template("user/client_manage.html")


@ bp.route('/client/deposit')
@ login_required(permissions=['acess_client_dashboard',
                              'acess_client_account_management'])
def client_deposit():
    return render_template("user/client_deposit.html")
