from pydantic import ValidationError
import pytest
from pypos.models.client_transaction_model import ClientTransaction

valid_form_data = [(
    'valid_01', {
        'datetime': "2022-12-12 12:23:23",
        'transaction_type': 'deposit',
        'value': '13.05'
    }), (
    'valid_02', {
        'datetime': "2022-12-12 6:00:32",
        'transaction_type': 'withdraw',
        'value': '13.05'
    })
]

invalid_form_data = [(
    'invalid date format', {
        'datetime': "2022/12/12 12:23:23",
        'transaction_type': 'deposit',
        'value': '13.05'
    }), (
    # 'invalid time format', {
    #     'datetime': "2022-12-12 6:00",
    #     'transaction_type': 'withdraw',
    #     'value': '13.05'
    # }), (
    'invalid transaction type', {
        'datetime': "2022-12-12 6:00",
        'transaction_type': 'withdraws',
        'value': '13.05'
    }), (
    'invalid transaction type', {
        'datetime': "2022-12-12 6:00",
        'transaction_type': '2',
        'value': '13.05'
    }), (
    'invalid value', {
        'datetime': "2022-12-12 6:00",
        'transaction_type': 'withdraw',
        'value': '-1'
    }),
]


@pytest.mark.parametrize(('message', 'form_data'), [*valid_form_data])
def test_transaction_account_valid(app, message, form_data):
    with app.app_context():
        user = ClientTransaction(**form_data)
        assert user, "Must pass validation"


@pytest.mark.parametrize(('message', 'form_data'), [*invalid_form_data])
def test_transaction_account_invalid(app, message, form_data):
    with app.app_context():
        with pytest.raises(ValidationError):
            ClientTransaction(**form_data)
