import sqlite3
from pathlib import Path

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


# The Python functions that will run the schema.sql


def init_db():
    db = get_db()
    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))
    with current_app.open_resource("initial_data.sql") as f:
        db.executescript(f.read().decode("utf8"))
    clear_uploaded_files()


def clear_uploaded_files():
    uploaded_files = Path("pypos/uploads").glob("**/[!.]*")
    for file in uploaded_files:
        if file.is_file():
            file.unlink()


def populate_db():
    from pypos.demo_setup.setup import (
        setup_product_data,
        setup_transaction_data,
        setup_user_data,
    )

    setup_user_data()
    setup_product_data()
    setup_transaction_data()


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


@click.command("populate-db")
@with_appcontext
def populate_db_command():
    """Populate the database."""
    populate_db()
    click.echo("Populated the database.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(populate_db_command)
