import pytest
from flask import g, session, url_for
from pypos.db import get_db

def test_product_index(client, app):
    form_data = {
        'name':'name',
        'price':10,
        'category':1,
        }
    
    with app.app_context():
        db = get_db()
        product_count_before = db.execute("SELECT COUNT(*) FROM product").fetchone()[0]
        
        response = client.post('/product/add_product', data=form_data)

        product_count_after = db.execute("SELECT COUNT(*) FROM product").fetchone()[0]
        assert response.status_code == 302
        assert product_count_after == product_count_before + 1