import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from pypos.db import get_db

bp = Blueprint('product', __name__, url_prefix='/product')