import os

from flask import Blueprint, request, render_template, current_app, redirect
from sql_provider import SQLProvider
from access import login_permission_required
from database import db_update, work_with_db


edit_app = Blueprint('edit', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

@edit_app.route('/red', methods=['GET', 'POST'])
@login_permission_required
def red_menu():
    db_config = current_app.config['DB_CONFIG']
    if request.method == 'GET':
        sql = provider.get('list_of_items.sql', table='menu')
        items = work_with_db(db_config, sql)
        return render_template('red_menu.html', items=items)
    else:
        id_menu = request.form.get('idMenu', None)
        if id_menu is not None:
            sql = provider.get('delete_menu.sql', id=id_menu)
            db_update(db_config, sql)
        return redirect('/edit/red')

@edit_app.route('/insert', methods=['GET', 'POST'])
def insert_menu():
    if request.method == 'GET':
        return render_template('insert_menu.html', forma=True)
    else:
        name = request.form.get('name', None)
        weight = request.form.get('weight', None)
        price = request.form.get('price', None)
        if name is not None and weight is not None and price is not None:
            sql = provider.get('insert_menu.sql', name=name, weight=weight, price=price)
            db_update(current_app.config['DB_CONFIG'], sql)
        return redirect('/edit/red')
