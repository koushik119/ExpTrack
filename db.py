import sqlite3
from datetime import date, datetime, time, timedelta,timezone
import dateutil.relativedelta
import calendar


conn = sqlite3.connect('test.db')

# conn.execute('''CREATE TABLE EXPENSES(timestamp INT PRIMARY KEY NOT NULL, category TEXT NOT NULL, expense INT NOT NULL);''')

def insertExpense(timestamp, category, expense):
    conn.execute("INSERT INTO EXPENSES VALUES(?,?,?)", (timestamp, category, expense))
    conn.commit()
    print("Expense added")


def expensesCountThisMonth():
    # get current month's beginning timestamp
    begTime = int(datetime.today().replace(day=1,hour=0,minute=0,second=0,microsecond=0).timestamp())
    # get all expenses from this month
    expenses = conn.execute("SELECT COUNT(*) FROM EXPENSES WHERE timestamp >= ?", (begTime,))
    # return the count
    return expenses.fetchone()[0]

def totalExpenseThisMonth():
    # get current month's beginning timestamp
    begTime = int(datetime.today().replace(day=1,hour=0,minute=0,second=0,microsecond=0).timestamp())
    # get all expenses from this month
    expenses = conn.execute("SELECT SUM(expense) FROM EXPENSES WHERE timestamp >= ?", (begTime,))
    # return the count
    sum = expenses.fetchone()[0]
    if sum is None:
        return 0
    return sum

def totalExpenseLastMonth():
    last_day_of_prev_month = date.today().replace(day=1) - timedelta(days=1)
    lastMonthEndTime = int(datetime.combine(last_day_of_prev_month, time(23,59,59)).timestamp())
    lastMonthBegTime = int(datetime.combine(date.today().replace(day=1) - timedelta(days=last_day_of_prev_month.day), time(0,0,0)).timestamp())
    
    expenses = conn.execute("SELECT SUM(expense) FROM EXPENSES WHERE timestamp >= ? AND timestamp <= ?", (lastMonthBegTime, lastMonthEndTime))

    # return expenses.fetchone()[0] if expenses.fetchone()[0] else 0
    sum = expenses.fetchone()[0]
    if sum is None:
        return 0
    return sum
    

def expenseByCategory():
    begTime = int(datetime.today().replace(day=1,hour=0,minute=0,second=0,microsecond=0).timestamp())

    expenses = conn.execute("SELECT category, SUM(expense) FROM EXPENSES WHERE timestamp >= ? GROUP BY category", (begTime,))

    return expenses.fetchall()
# def fun(e):
#     return e[0]

def listByCategoryThisMonth(category):
    begTime = int(datetime.today().replace(day=1,hour=0,minute=0,second=0,microsecond=0).timestamp())
    expenseList=conn.execute("SELECT expense,timestamp FROM EXPENSES WHERE category=? AND timestamp >= ?",(category,begTime))
    return expenseList.fetchall()

def listByCategoryPreviousMonth(category):
    begTime = int(datetime.today().replace(month=1,day=1,hour=0,minute=0,second=0,microsecond=0).timestamp())
    last_day_of_prev_month = date.today().replace(day=1) - timedelta(days=1)
    lastMonthEndTime = int(datetime.combine(last_day_of_prev_month, time(23,59,59)).timestamp())
    expenseList=conn.execute("SELECT expense,timestamp FROM EXPENSES WHERE category=? AND timestamp >= ? AND timestamp<=?",(category,begTime,lastMonthEndTime))
    return expenseList.fetchall()

#insertExpense(int(datetime.today().replace(month=3,day=1).timestamp()),"Shopping",60)
ex=listByCategoryPreviousMonth("Shopping")
# time_data =str(datetime.fromtimestamp(ex[3][1]))
# format_data = "%y-%m-%d %H:%M:%S"
ex.sort(reverse=True)
# today1=today.month
print(ex)
# print(calendar.month_name[today])
# print(int(datetime.today().replace(month=3).timestamp()))

# print(totalExpenseLastMonth())
#for i in ex:
#print(datetime.today().replace(month=1,day=1,hour=0,minute=0,second=0,microsecond=0))