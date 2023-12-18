from flask import Flask, render_template, session

from blueprints.sql_request.routes import sql_app
from blueprints.authorisation.routes import auth_app
from blueprints.order.routes import ord_app
from blueprints.manage.routes import edit_app

import json

app = Flask(__name__)

app.config['DB_CONFIG'] = json.load(open('configs/db.json', 'r'))
app.config['PERMISSION_CONFIG'] = json.load(open('configs/permissions.json', 'r'))
app.config['SECRET_KEY'] = 'secr_key'

app.register_blueprint(sql_app, url_prefix='/sql')
app.register_blueprint(auth_app, url_prefix='/auth')
app.register_blueprint(ord_app, url_prefix='/ord')
app.register_blueprint(edit_app, url_prefix='/edit')

groups = {"Waiter": "Официант",
  "Manager": "Менеджер",
  "Boss": "Управляющий",
  "Unauthorised": "Вход не выполнен"}

@app.route('/')
def index():
    if 'group_name' in session:
        result = session['group_name']
    else:
        session['group_name'] = "Unauthorised"
        result = session['group_name']

    return render_template('base.html', result=groups[result])

@app.route('/exit')
def exit_handler():
    if session['group_name'] == "Unauthorised":
        return render_template('base.html', result=groups[session['group_name']])
    session.clear()
    return render_template('exit.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)

