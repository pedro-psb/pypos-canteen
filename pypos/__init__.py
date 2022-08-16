import os

from flask import Flask

from pypos.blueprints import user_space


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="ieouwer09832njflçasdf983",
        DATABASE=os.path.join(app.instance_path, "pypos.sqlite"),
        UPLOAD_FOLDER="uploads",  # understand better how this path works
        MAX_CONTENT_LENGTH=1 * 1000 * 1000,  # max upload size 5mb
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


def register_blueprints(app):
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


# Sitemap helper
def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)
