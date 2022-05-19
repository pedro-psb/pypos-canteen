from flask import Blueprint
from . import product_mng
bp = Blueprint('canteen', __name__, url_prefix='/canteen')
bp.register_blueprint(product_mng.bp)
