

from fastapi import FastAPI, HTTPException
from datetime import date


import db_helper
from typing import List
from pydantic import BaseModel

app = FastAPI()


class Expense(BaseModel):
    amount: float
    category: str
    notes: str

class DateRange(BaseModel):
    start_date: date
    end_date: date

@app.get("/expenses/{expense_date}", response_model= List[Expense])
def get_expenses(expense_date: date):
    expenses = db_helper.get_all_expenses_by_date(expense_date)
    if expenses is None:
        raise HTTPException(status_code=500,detail=f"Failed to retrieve expenses for {expense_date}")
    return expenses

@app.post("/expenses/{expense_date}")
def post_expenses(expense_date: date, expenses: List[Expense]):
    try:
        db_helper.delete_expense_for_date(expense_date)
        for expense in expenses:
            db_helper.insert_expense(expense_date, expense.amount, expense.category, expense.notes)
        return "Expenses added successfully"
    except Exception:
        raise HTTPException(status_code=500, detail=f"Failed to add/update expenses for {expense_date}")

@app.post("/analytics")
def get_analytics(date_range: DateRange):
    summary = db_helper.fetch_expense_summary(date_range.start_date, date_range.end_date)
    if summary is None:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve expense summary from {date_range.start_date} to {date_range.end_date}")

    filtered_summary = [expenses for expenses in summary if expenses['total'] != 0]

    if not filtered_summary:
        raise HTTPException(
            status_code=404,
            detail=f"No expenses found for the period {date_range.start_date} to {date_range.end_date}"
        )

    return filtered_summary

@app.get("/monthly/analytics")
def get_analytics_monthly():
    summary = db_helper.fetch_expense_summary_by_month()
    if summary is None:
        raise HTTPException(status_code=500, detail= "Failed to retrieve monthly expense summary")

    if not summary:
        return {"message": "No expense data found", "data": []}
    return summary