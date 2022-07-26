from pprint import pprint
import pytest
from pypos.models import dao

from pypos.db import get_db
from pypos.models.dao_reports import ReportSummary
from pypos.models.transactions_dao import Product, RegularPurchase


@pytest.fixture
def app_with_transactions(app):
    """Regular Purchase setup for summary calculations"""
    with app.app_context():
        purchase = RegularPurchase(
            canteen_id=1,
            products=[
                Product(id=1, quantity=1, canteen_id=1),
                Product(id=2, quantity=3, canteen_id=1)],
            payment_method="cash"
        )
        purchase.save()
    return app


class TestReportSummary:
    def test_most_sales(self, app_with_transactions):
        with app_with_transactions.app_context():
            most_sales = ReportSummary.get_most_sales()
            assert most_sales['product'] == 'Pão de Queijo'
            assert most_sales['share'] == 75

    def test_less_sales(self, app_with_transactions):
        with app_with_transactions.app_context():
            less_sales = ReportSummary.get_less_sales()
            assert less_sales['product'] == 'torta'
            assert less_sales['share'] == 25

    def test_higher_invoice(self, app_with_transactions):
        with app_with_transactions.app_context():
            most_sales = ReportSummary.get_higher_invoice()
            assert most_sales['product'] == 'Pão de Queijo'
            assert most_sales['share'] == 65.93

    def test_lower_invoice(self, app_with_transactions):
        with app_with_transactions.app_context():
            most_sales = ReportSummary.get_lower_invoice()
            assert most_sales['product'] == 'torta'
            assert most_sales['share'] == 34.07

    def test_full_summary(self, app_with_transactions):
        with app_with_transactions.app_context():
            full_summary = ReportSummary.get_full_summary()
            assert full_summary['most_sales']['product'] == 'Pão de Queijo'
            assert full_summary['most_sales']['share'] == 75
            assert full_summary['less_sales']['product'] == 'torta'
            assert full_summary['less_sales']['share'] == 25
            assert full_summary['higher_invoice']['product'] == 'Pão de Queijo'
            assert full_summary['higher_invoice']['share'] == 65.93
            assert full_summary['lower_invoice']['product'] == 'torta'
            assert full_summary['lower_invoice']['share'] == 34.07
