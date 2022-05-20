from crypt import methods
from . import bp
from models import TransactionProduct

@bp.route('add_transaction_product', methods=['POST'])
def add_transaction_product():
    pass


@bp.route('remove_transaction_product', methods=['POST'])
def remove_transaction_product():
    pass
