from datetime import datetime

from flask import Blueprint, render_template, request, current_app

from access import login_permission_required
from database import work_with_db
from sql_provider import SQLProvider

sql_app = Blueprint('sql', __name__, template_folder='templates')

provider = SQLProvider("blueprints/sql_request/sql")

def table_cr(head, result):
    thead = "<thead>\n"
    tbody = "<tbody>\n"
    for header in head:
        thead += "<tr>\n"
        tbody += f"<th style=\"width: 10%\">{header}</th>"
    thead += "</tr>\n"
    for row in result:
        tbody += "</tr>\n"
        for value in list(row.values()):
            tbody += f"<td>{value}</td>"
    tbody += "</thead>\n"
    tbody += "</tbody>\n"

    table = "<table>\n" + thead + tbody + "</table>"
    return table

@sql_app.route('/sql_menu')
@login_permission_required
def sql_menu():
    return render_template('sql_menu.html')

@sql_app.route('/sql_dish_rep', methods=["GET", "POST"])
def get_dish_rep():
    if request.method=="GET":
        return render_template('dish_report_input.html')
    month = request.form.get("month")
    year = request.form.get("year")

    sql = provider.get('dishorder_report.sql', month=month, year=year)
    result = work_with_db(current_app.config['DB_CONFIG'], sql)

    if not result:
        return render_template('not_found.html')

    head = ['Название блюда', 'Число заказов', 'Сумма заказов']
    return render_template('result.html', result=table_cr(head, result))


@sql_app.route('/sql_waiters_rep', methods=["GET", "POST"])
def get_waiters_rep():
    if request.method=="GET":
        return render_template('waiters_report_input.html')
    month = request.form.get("month")
    year = request.form.get("year")

    sql = provider.get('waiters_report.sql', month=month, year=year)
    result = work_with_db(current_app.config['DB_CONFIG'], sql)

    if not result:
        return render_template('not_found.html')

    head = ['Имя официанта', 'Число заказов', 'Сумма заказов']
    return render_template('result.html', result=table_cr(head,result))


@sql_app.route('/sql_orders', methods=["GET", "POST"])
def get_orders_rep():
    if request.method=="GET":
        return render_template('orders_input.html')
    date = request.form.get("date")
    year = request.form.get("year")

    sql = provider.get('get_orders.sql', date=date)
    result = work_with_db(current_app.config['DB_CONFIG'], sql)

    if not result:
        return render_template('not_found.html')

    head = ['Имя официанта', 'Число блюд', 'Сумма заказа']
    return render_template('result.html', result=table_cr(head,result))