import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logger
from decouple import config

logger = setup_logger('db_helper')

@contextmanager
def connect_db(commit=False, connection_check= True):
    connection = mysql.connector.connect(
        host=config('DB_HOST', default='localhost'),
        user=config('DB_USER', default='root'),
        passwd=config('DB_PASSWORD'),
        database=config('DB_NAME', default='expense_manager')
        )
    if connection_check:
        if connection.is_connected():
            print("Connection Successful")
        else:
            print("Connection Failed")

    cursor = connection.cursor(dictionary=True)

    yield cursor

    if commit:
        connection.commit()

    cursor.close()
    connection.close()

def get_all_expenses():
    with connect_db(connection_check= False) as cursor:
        cursor.execute("SELECT * FROM expenses")
        result = cursor.fetchall()
        return result

def get_all_expenses_by_date(date):
    logger.info(f"Fetching all expenses for {date}")
    with connect_db(connection_check= False) as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date=%s", (date,))
        expenses = cursor.fetchall()
        if len(expenses) == 0:
            return f"No expenses found for {date}"
        return expenses

def insert_expense(expense_date, amount, category, notes):
    logger.info(f"Inserting expense for {expense_date}")
    with connect_db(commit=True, connection_check= False) as cursor:
        cursor.execute("insert into expenses (expense_date,amount, category, notes) values (%s, %s, %s, %s)",
                      (expense_date, amount, category, notes))

def delete_expense_for_date(expense_date):
    logger.info(f"Deleting expense for {expense_date}")
    with connect_db(commit=True, connection_check= False) as cursor:
        cursor.execute("delete from expenses where expense_date = %s", (expense_date,))

def fetch_expense_summary(start_date, end_date):
    logger.info(f"Fetching expense summary for {start_date} to {end_date}")
    with connect_db(commit=False, connection_check= False) as cursor:
        query = """
                SELECT category,
                       SUM(amount) as total,
                       ROUND(SUM(amount) * 100.0 / (SELECT SUM(amount)
                                                    FROM expenses
                                                    WHERE expense_date BETWEEN %s AND %s), 2) as percentage
                FROM expenses
                WHERE expense_date BETWEEN %s AND %s
                GROUP BY category
                ORDER BY total DESC
                """
        cursor.execute(query, (start_date, end_date, start_date, end_date))
        data = cursor.fetchall()
        return data

def fetch_expense_summary_by_month():
    logger.info("Fetching expense summary by month")
    with connect_db(commit=False, connection_check=False) as cursor:
        query = """
            SELECT MONTH(expense_date) AS month_number,
                   MONTHNAME(expense_date) AS month_name,
                   SUM(amount) AS total
            FROM expenses
            GROUP BY MONTH(expense_date), MONTHNAME(expense_date)
            ORDER BY MONTH(expense_date) ASC
        """
        cursor.execute(query)
        data = cursor.fetchall()
        return data

if __name__ == '__main__':
    #get_all_expenses()
    # expense = get_all_expenses_by_date("2024-08-02")
    # print(expense)
    # insert_expense("2024-10-28", 40, "Food", "Samosa")
    # expense = get_all_expenses_by_date("2024-10-28")
    # print(expense)
    # delete_expense_for_date("2024-10-28")
    # expense = get_all_expenses_by_date("2024-10-28")
    # print(expense)
    # get_all_expenses_by_date("2024-09-29")
    # delete_expense_for_date("2024-09-29")
    # get_all_expenses_by_date("2024-09-29")
    # summary = fetch_expense_summary('2024-08-01', '2024-08-05')
    # for record in summary:
    #     print(record)

    summary = fetch_expense_summary_by_month()
    for result in summary:
        print(result)

