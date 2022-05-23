from flask import Blueprint

from . import product_mng, point_of_sale
bp = Blueprint('canteen', __name__, url_prefix='/canteen')
bp.register_blueprint(product_mng.bp)
bp.register_blueprint(point_of_sale.bp)
