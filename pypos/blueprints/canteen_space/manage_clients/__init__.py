from flask import Blueprint

bp = Blueprint('manage_clients', __name__, url_prefix='/manage-clients')
from .views import *