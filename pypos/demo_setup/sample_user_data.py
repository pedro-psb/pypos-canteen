from random import randint
from typing import Dict, List

from pypos.models import dao


def random_phone_number():
    return "(21) 9{}{}{}{}-{}{}{}{}".format(
        randint(0, 9),
        randint(0, 9),
        randint(0, 9),
        randint(0, 9),
        randint(0, 9),
        randint(0, 9),
        randint(0, 9),
        randint(0, 9),
    )


# From ID's 1 to 3
def sample_employees() -> List[Dict]:
    return [
        {
            "username": "jane_oconnor",
            "email": "jane_oconnor@gmail.com",
            "password": "pass",
            "phone_number": "(21) 91234-5678",
            "role_id": "1",  # owner
            "canteen_id": "1",
        },
        {
            "username": "dale_raymond",
            "email": "dale_raymond@gmail.com",
            "password": "pass",
            "phone_number": "(21) 98888-7777",
            "role_id": "2",  # manager
            "canteen_id": "1",
        },
        {
            "username": "breanna_rosario",
            "email": "breanna_rosario@gmail.com",
            "password": "pass",
            "phone_number": "(21) 98765-4321",
            "role_id": "3",  # cashier
            "canteen_id": "1",
        },
    ]


# From ID's 4 to 11
def sample_clients() -> List[Dict]:
    return [
        {
            "username": "mauricio_galvan",
            "email": "mauricio_galvan@gmail.com",
            "password": "pass",
            "phone_number": random_phone_number(),
            "role_id": "4",
            "canteen_id": "1",
        },
        {
            "username": "anderson_carney",
            "email": "anderson_carney@gmail.com",
            "password": "pass",
            "phone_number": random_phone_number(),
            "role_id": "4",
            "canteen_id": "1",
        },
        {
            "username": "kenley_york",
            "email": "kenley_york@gmail.com",
            "password": "pass",
            "phone_number": random_phone_number(),
            "role_id": "4",
            "canteen_id": "1",
        },
        {
            "username": "paola_stanton",
            "email": "paola_stanton@gmail.com",
            "password": "pass",
            "phone_number": random_phone_number(),
            "role_id": "4",
            "canteen_id": "1",
        },
        {
            "username": "genesis_rodriguez",
            "email": "genesis_rodriguez@gmail.com",
            "password": "pass",
            "phone_number": random_phone_number(),
            "role_id": "4",
            "canteen_id": "1",
        },
        {
            "username": "adalynn_choi",
            "email": "adalynn_choi@gmail.com",
            "password": "pass",
            "phone_number": random_phone_number(),
            "role_id": "4",
            "canteen_id": "1",
        },
        {
            "username": "ryan_foley",
            "email": "ryan_foley@gmail.com",
            "password": "pass",
            "phone_number": random_phone_number(),
            "role_id": "4",
            "canteen_id": "1",
        },
        {
            "username": "hunter_ramsey",
            "email": "hunter_ramsey@gmail.com",
            "password": "pass",
            "phone_number": random_phone_number(),
            "role_id": "4",
            "canteen_id": "1",
        },
    ]


# From ID's 12 to
def sample_client_dependents() -> List[Dict]:
    return [
        {
            "username": "john_galvan",
            "age": "12",
            "grade": "10th",
            "email": "john_galvan@gmail.com",
            "password": "pass",
            "phone_number": random_phone_number(),
            "role_name": "client_dependent",
            "user_provider_id": dao.get_user_by_name("mauricio_galvan")["id"],
            "canteen_id": "1",
        },
        {
            "username": "mary_galvan",
            "age": "10",
            "grade": "8th",
            "email": "mary_galvan@gmail.com",
            "password": "pass",
            "phone_number": random_phone_number(),
            "role_name": "client_dependent",
            "user_provider_id": dao.get_user_by_name("mauricio_galvan")["id"],
            "canteen_id": "1",
        },
        {
            "username": "anderson_galvan",
            "age": "8",
            "grade": "6th",
            "email": "anderson_galvan@gmail.com",
            "password": "pass",
            "phone_number": random_phone_number(),
            "role_name": "client_dependent",
            "user_provider_id": dao.get_user_by_name("mauricio_galvan")["id"],
            "canteen_id": "1",
        },
        {
            "username": "john_carney",
            "age": "9",
            "grade": "7th",
            "email": "john_carney@gmail.com",
            "password": "pass",
            "phone_number": random_phone_number(),
            "role_name": "client_dependent",
            "user_provider_id": dao.get_user_by_name("anderson_carney")["id"],
            "canteen_id": "1",
        },
        {
            "username": "anderson_york",
            "age": "7",
            "grade": "5th",
            "email": "anderson_york@gmail.com",
            "password": "pass",
            "phone_number": random_phone_number(),
            "user_provider_id": dao.get_user_by_name("kenley_york")["id"],
            "canteen_id": "1",
        },
        {
            "username": "astrid_york",
            "age": "5",
            "grade": "3rd",
            "email": "astrid_york@gmail.com",
            "password": "pass",
            "phone_number": random_phone_number(),
            "role_name": "client_dependent",
            "user_provider_id": dao.get_user_by_name("kenley_york")["id"],
            "canteen_id": "1",
        },
        {
            "username": "stella_stanton",
            "age": "4",
            "grade": "2nd",
            "email": "stella_stanton@gmail.com",
            "password": "pass",
            "phone_number": random_phone_number(),
            "role_name": "client_dependent",
            "user_provider_id": dao.get_user_by_name("paola_stanton")["id"],
            "canteen_id": "1",
        },
        {
            "username": "oscar_rodriguez",
            "age": "5",
            "grade": "3rd",
            "email": "oscar_rodriguez@gmail.com",
            "password": "pass",
            "phone_number": random_phone_number(),
            "role_name": "client_dependent",
            "user_provider_id": dao.get_user_by_name("genesis_rodriguez")["id"],
            "canteen_id": "1",
        },
        {
            "username": "anne_rodriguez",
            "age": "8",
            "grade": "6th",
            "email": "anne_rodriguez@gmail.com",
            "password": "pass",
            "phone_number": random_phone_number(),
            "role_name": "client_dependent",
            "user_provider_id": dao.get_user_by_name("genesis_rodriguez")["id"],
            "canteen_id": "1",
        },
        {
            "username": "adam_choi",
            "age": "6",
            "grade": "4th",
            "email": "adam_choi@gmail.com",
            "password": "pass",
            "phone_number": random_phone_number(),
            "role_name": "client_dependent",
            "user_provider_id": dao.get_user_by_name("adalynn_choi")["id"],
            "canteen_id": "1",
        },
        {
            "username": "ross_foley",
            "age": "5",
            "grade": "3rd",
            "email": "ross_foley@gmail.com",
            "password": "pass",
            "phone_number": random_phone_number(),
            "role_name": "client_dependent",
            "user_provider_id": dao.get_user_by_name("ryan_foley")["id"],
            "canteen_id": "1",
        },
        {
            "username": "rachel_foley",
            "age": "13",
            "grade": "10th",
            "email": "rachel_foley@gmail.com",
            "password": "pass",
            "phone_number": random_phone_number(),
            "role_name": "client_dependent",
            "user_provider_id": dao.get_user_by_name("ryan_foley")["id"],
            "canteen_id": "1",
        },
        {
            "username": "amy_ramsey",
            "age": "10",
            "grade": "8th",
            "email": "amy_ramsey@gmail.com",
            "password": "pass",
            "phone_number": random_phone_number(),
            "role_name": "client_dependent",
            "user_provider_id": dao.get_user_by_name("hunter_ramsey")["id"],
            "canteen_id": "1",
        },
    ]
