import pytest
from flask import g, session
from pypos.db import get_db

def test_product_index(client, app):
    response = client.get('/product/')
    assert response.status_code == 200
    assert "Torta de Maçã" in response.text