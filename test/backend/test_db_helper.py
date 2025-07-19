import pytest

from backend import db_helper


def test_get_all_expenses_by_date():
    expenses = db_helper.get_all_expenses_by_date("2024-08-15")
    assert len(expenses) == 1
    assert expenses[0]["expense_date"].strftime("%Y-%m-%d") == "2024-08-15"
    assert expenses[0]["amount"] == 10
    assert expenses[0]["category"] == "Shopping"
    assert expenses[0]["notes"] == "Bought potatoes"

def test_get_all_expenses_by_date_invalid():
    expenses = db_helper.get_all_expenses_by_date("9999-08-15")
    assert expenses == 'No expenses found for 9999-08-15'

def test_fetch_expense_summary_invalid_date():
    summary = db_helper.fetch_expense_summary("2099-08-15", "2099-08-17")
    assert len(summary) == 0



