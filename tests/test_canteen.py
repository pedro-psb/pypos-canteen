import json
import pytest
from flask import g, session, url_for
from pypos.db import get_db

foo_product = {
    'name': 'name',
    'price': '10',
    'category': '1'
}
foo_category = {
    'name': 'sobremesa'
}
foo_transaction = {
    'products': json.dumps([
        {'id': '1', 'quantity': '1'},
        {'id': '2', 'quantity': '3'},
    ]),
    'discount': '0',
    'payment_method': '1'
}

@ pytest.mark.parametrize(
    ('query', 'endpoint_adress', 'form_data'), (
        ('SELECT COUNT(*) FROM product WHERE canteen_id=?;',
         'canteen.product.add_product', foo_product),
        ('SELECT COUNT(*) FROM product_category WHERE canteen_id=?;',
         'canteen.product.add_category', foo_category),
        ('SELECT COUNT(*) FROM transaction_product WHERE canteen_id=?;',
         'canteen.point_of_sale.add_transaction_product', foo_transaction)
    ))
def test_categories_are_isolated_by_canteen(client, auth, app, query, endpoint_adress, form_data):
    '''As a product added by a user of canteen_1, it should not be loaded with canteen_2 filter'''
    with app.app_context(), app.test_request_context():
        endpoint = url_for(endpoint_adress)
        auth.login()  # with user from canteen 1
        db = get_db()
        entity_count_from_canteen_1_before = db.execute(
            query, (1,)).fetchone()[0]
        entity_count_from_canteen_2_before = db.execute(
            query, (2,)).fetchone()[0]

        response = client.post(endpoint, data=form_data)

        entity_count_from_canteen_1_after = db.execute(
            query, (1,)).fetchone()[0]
        entity_count_from_canteen_2_after = db.execute(
            query, (2,)).fetchone()[0]

        assert entity_count_from_canteen_1_after == entity_count_from_canteen_1_before + 1
        assert entity_count_from_canteen_2_after == entity_count_from_canteen_2_before
