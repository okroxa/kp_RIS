import datetime
import os

from flask import Blueprint, render_template, request, session, redirect, current_app

from access import login_permission_required
from blueprints.order.utils import add_to_basket, change, clear_order
from sql_provider import SQLProvider
from database import work_with_db, db_update

ord_app = Blueprint('ord', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

@ord_app.route('/', methods=['GET', 'POST'])
@login_permission_required
def list_orders_handler():
    if request.method == 'GET':
        cur_bas = session.get('order', [])
        sql= provider.get('order_list.sql')
        items = work_with_db(current_app.config['DB_CONFIG'], sql)
        return render_template('order.html', items=items, basket=cur_bas)
    else:
        item_id =request.form.get('idMenu')
        sql = provider.get('order_item.sql', m_id=item_id)
        items = work_with_db(current_app.config['DB_CONFIG'], sql)

        if not items:
            return "Item not found"

        if item_id is not None:
            add_to_basket(items)

        bas_id = request.form.get('idBasket')
        if bas_id is not None:
            change(bas_id)

        return redirect('/ord')

@ord_app.route('/clear')
def clear_bas_handler():
    clear_order()
    return redirect('/ord')

@ord_app.route('/back')
def back_bas_handler():
    clear_order()
    return redirect('/')

@ord_app.route('/buy')
def buy_bas_handler():
    if session.get('order'):
        return redirect('/ord/approve_order')
    return redirect('/ord')

@ord_app.route('/approve_order')
def list_orders_handler():
    cur_bas = session.get('order', [])
    cur_waiter = session.get('waiter_id', [])
    sql = provider.get('waiter_item.sql', w_id=cur_waiter)
    waiter = work_with_db(current_app.config['DB_CONFIG'], sql)

    return render_template('approve_order.html', basket=cur_bas, waiter=waiter[0]['Waitername'], date=datetime.date.today())

@ord_app.route('/approve_order/approve')
def approve_bas_handler():
    cur_bas = session.get('order', [])
    waiter_id = session.get('waiter_id')

    date = datetime.date.today()
    amount = 0
    price = 0
    sql = provider.get('get_id.sql')
    id_order = work_with_db(current_app.config['DB_CONFIG'], sql)[0]['id']
    if id_order is None:
        id_order = 0

    for b in cur_bas:
        sql = provider.get('insert_in_orderstring.sql', amount=b['number'], id_m=b['idMenu'], id_ord=int(id_order)+1)
        db_update(current_app.config['DB_CONFIG'], sql)
        amount += b['number']
        price += amount * b['Menucost']

    sql = provider.get('insert_in_order.sql', id=int(id_order)+1, date=date, price=price, amount=amount, waiter=waiter_id)
    db_update(current_app.config['DB_CONFIG'], sql)

    clear_order()

    return redirect('/ord/approve_order/result')

@ord_app.route('/approve_order/result')
def result_orders():
    return render_template('result_order.html')
