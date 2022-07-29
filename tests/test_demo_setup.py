from pypos.db import get_db
from pypos.demo_setup import setup
from pypos.models import dao


def test_employee_setup_works(app):
    with app.app_context():
        # TODO make this test more efficient
        setup.setup_user_data()
        owner_user = dao.get_user_by_name('jane_oconnor')
        employee_user = dao.get_user_by_name('dale_raymond')
        cashier_user = dao.get_user_by_name('breanna_rosario')
        client_user = dao.get_user_by_name('mauricio_galvan')
        client_child_user = dao.get_user_by_name('john_galvan')

        assert owner_user
        assert employee_user
        assert cashier_user
        assert client_user
        assert client_child_user
