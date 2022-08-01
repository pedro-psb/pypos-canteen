import json
from typing import Dict, List

from pypos.models import dao, dao_users


def sample_regular_purchase() -> List[Dict]:
    return [
        {
            "payment_method": "cash",
            "products": json.dumps(
                [
                    {"id": "1", "quantity": "1"},
                    {"id": "2", "quantity": "3"},
                ]
            ),
        },
        {
            "payment_method": "cash",
            "products": json.dumps(
                [
                    {"id": "2", "quantity": "5"},
                    {"id": "3", "quantity": "5"},
                ]
            ),
        },
    ]


def sample_user_account_purchase() -> List[Dict]:
    return [
        {
            "payment_method": "cash",
            "products": json.dumps(
                [
                    {"id": "1", "quantity": "1"},
                    {"id": "2", "quantity": "3"},
                ]
            ),
            "client_id": dao.get_user_by_name("mauricio_galvan")["id"],
        },
        {
            "payment_method": "cash",
            "products": json.dumps(
                [
                    {"id": "2", "quantity": "5"},
                    {"id": "3", "quantity": "5"},
                ]
            ),
            "client_id": dao.get_user_by_name("john_galvan")["id"],
        },
    ]


def sample_user_recharge() -> List[Dict]:
    return []
