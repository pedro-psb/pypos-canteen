from msilib.schema import Error
import pytest
from flask import g, got_request_exception, session, url_for, get_flashed_messages
from pypos.db import get_db
from pypos.blueprints.canteen_space.point_of_sale.errors import *
from markupsafe import escape


def test_valid_transaction(app, client):
    with app.app_context(), app.test_request_context():
        db=get_db()
        form_data = [
            {'product_id':'1', 'quantity':'1'},
            {'product_id':'2', 'quantity':'2'},
        ]
        transactions_before=db.execute(
            'SELECT count(*) FROM transaction_product;')
        raise ValueError('pesquisar como simular mandar json atraves de client.POST')
        response = client.post(
            url_for('canteen.point_of_sale.add_transaction_product'),
            data=form_data)
        transactions_after=db.execute(
            'SELECT count(*) FROM transaction_product;')
        assert response.status_code == 302
        assert transactions_after == transactions_before + 1



@ pytest.mark.parametrize(
    ('products'), (
        (['1', '2', '3']),
        (['1', '2', '3'])
    )
)
def test_invalid_transactions(app, client, products):
    pass
