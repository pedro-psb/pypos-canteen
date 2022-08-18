import os

from flask import Flask, current_app, send_from_directory, url_for
from werkzeug.exceptions import NotFound

from pypos.blueprints import user_space


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="ieouwer09832njflçasdf983",
        DATABASE=os.path.join(app.instance_path, "pypos.sqlite"),
        PRODUCT_IMG_FOLDER="uploads/product",
        AVATAR_IMG_FOLDER="uploads/avatar",
        MAX_CONTENT_LENGTH=5 * 1000 * 1000,  # max upload size 5mb
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    register_views(app)
    register_blueprints(app)

    # Database config
    from . import db

    db.init_app(app)
    flask_env = app.config.get("ENV", "production")
    if not app.testing and flask_env != "development":
        with app.app_context():
            print("initializing and populating db ...")
            db.init_db()
            db.populate_db()
            print("done")

    return app


def register_blueprints(app: Flask):
    from .blueprints import auth, canteen_space, frontend

    app.register_blueprint(auth.bp)
    app.register_blueprint(canteen_space.bp)
    app.register_blueprint(frontend.bp)
    app.register_blueprint(user_space.bp)


def register_views(app):
    # a simple page that says hello
    @app.route("/hello")
    def hello():
        return "Hello, World!"

    @app.route("/img/product/<filename>")
    def get_product_img(filename):
        """Looks in the `uploads` Folder then the `static/img/products` Folder"""
        try:
            serve_response = send_from_directory(
                current_app.config["PRODUCT_IMG_FOLDER"], filename
            )
        except NotFound:
            serve_response = send_from_directory("static/img/products", filename)
        return serve_response

    @app.route("/img/avatar/<filename>")
    def get_avatar_img(filename):
        return send_from_directory(current_app.config["AVATAR_IMG_FOLDER"], filename)


# Sitemap helper
def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)
