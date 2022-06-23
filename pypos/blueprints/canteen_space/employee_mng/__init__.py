from flask import Blueprint

bp = Blueprint('manage_employee', __name__, url_prefix='/manage_employee')
from .views import *