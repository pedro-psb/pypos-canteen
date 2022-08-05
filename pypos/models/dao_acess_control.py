from pypos.db import get_db


def get_all_roles():
    db = get_db()
    not_employee_roles = select_non_employee_roles()
    query = f"SELECT * FROM role WHERE name NOT IN {not_employee_roles};"
    all_roles = db.execute(query).fetchall()
    all_roles = [dict(role) for role in all_roles]
    return all_roles


def select_non_employee_roles():
    # select employee roles based on fixed non-emplyed roles
    not_employee_roles = ["owner", "client", "client_dependent", "temporary_client"]
    not_employee_roles = map(lambda x: f"'{x}'", not_employee_roles)
    not_employee_roles = f"({','.join(not_employee_roles)})"
    return not_employee_roles
