from sqlite3 import Connection, Cursor
from typing import List

from pypos.db import get_db
from pypos.models.user_model import User, UserChildCreateForm, UserChildUpdateForm


def insert_user(user: User) -> int:
    """Insert provider client or employee to database.
    return it's id"""
    con = get_db()
    db = con.cursor()
    query = """INSERT INTO user(username, email, password,
            phone_number, role_name) VALUES(?,?,?,?,?);"""
    db.execute(
        query,
        (user.username, user.email, user.password, user.phone_number, user.role_name),
    )
    con.commit()
    user_id: int = db.lastrowid
    return user_id


def insert_user_account(user_id):
    con = get_db()
    db = con.cursor()
    query = """INSERT INTO user_account(user_id) VALUES (?);"""
    db.execute(query, [user_id])
    con.commit()


def create_user_child(form_data: UserChildCreateForm):
    con = get_db()
    db = con.cursor()

    # Insert regular user
    query = """INSERT INTO user (username, password, email, phone_number,
    role_name, canteen_id) VALUES (?,?,?,?,?,?);"""
    db.execute(
        query,
        [
            form_data.username,
            form_data.password,
            form_data.email,
            form_data.phone_number,
            form_data.role_name,
            form_data.canteen_id,
        ],
    )
    user_id = db.lastrowid

    # Insert user_child extension
    query = """INSERT INTO user_child (age, grade, user_provider_id, user_id)
    VALUES (?,?,?,?);"""
    db.execute(
        query, [form_data.age, form_data.grade, form_data.user_provider_id, user_id]
    )
    if db.rowcount < 1:
        raise ValueError("Some error ocurred with the database insert funcion")
    # Suceed
    con.commit()
    return user_id


def update_user_child(form_data: UserChildUpdateForm):
    con = get_db()
    db = con.cursor()

    # update regular user
    query = """UPDATE user SET username=:username, password=:password, email=:email,
    phone_number=:phone_number
    WHERE id=:id;"""
    db.execute(query, form_data.dict())

    # update user_child extension
    query = """UPDATE user_child SET age=:age, grade=:grade WHERE user_id=:id;"""
    db.execute(query, form_data.dict())
    # Suceed
    con.commit()


def delete_user(user_id):
    con = get_db()
    db = con.cursor()

    # update regular user
    query = """UPDATE user SET active=0 WHERE id=?"""
    db.execute(query, [user_id])
    con.commit()


# Insert over same connection


def insert_user_no_commit(db: Cursor, user: User):
    """Insert provider client or employee to database"""
    query = """INSERT INTO user(username, email, password,
            phone_number, role_name) VALUES(?,?,?,?,?);"""
    db.execute(
        query,
        (user.username, user.email, user.password, user.phone_number, user.role_name),
    )
    return db


def insert_user_account_no_commit(db: Cursor, user_id: int):
    """Insert user account to client, given it's id"""
    query = """INSERT INTO user_account(user_id) VALUES (?);"""
    db.execute(query, [user_id])
    return db


def insert_client_child_no_commit(db: Cursor, user: UserChildCreateForm):
    """Insert user account to client, given it's id"""
    # Insert regular user
    query = """INSERT INTO user (username, password, email, phone_number,
    role_name, canteen_id) VALUES (?,?,?,?,?,?);"""
    db.execute(
        query,
        [
            user.username,
            user.password,
            user.email,
            user.phone_number,
            user.role_name,
            user.canteen_id,
        ],
    )
    user_id = db.lastrowid

    # Insert user_child extension
    query = """INSERT INTO user_child (age, grade, user_provider_id, user_id)
    VALUES (?,?,?,?);"""
    db.execute(query, [user.age, user.grade, user.user_provider_id, user_id])
    return db
