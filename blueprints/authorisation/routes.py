from flask import Blueprint, render_template, session, request, current_app
from access import login_permission_required
from database import work_with_db
from sql_provider import SQLProvider

groups = {"Waiter": "Официант",
  "Manager": "Менеджер",
  "Boss": "Управляющий",
  "Unauthorised": "Вход не выполнен"}

auth_app = Blueprint('auth', __name__, template_folder='templates')

provider = SQLProvider("blueprints/authorisation/sql")

@auth_app.route('/', methods=['GET','POST'])
@login_permission_required
def login_page():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        login = request.form.get('login', '')
        password = request.form.get('password', '')
        sql = provider.get('get_group.sql', login=login, password=password)
        result = work_with_db(current_app.config['DB_CONFIG'], sql)

        if not result:
            session['group_name'] = "Unauthorised"
            return render_template('base.html', result= groups[session['group_name']])
        session['group_name'] = list(result[0].values())[0]
        waiter_id = list(result[0].values())[1]
        if waiter_id is not None:
            session['waiter_id'] = list(result[0].values())[1]
        return render_template('base.html', result=groups[session['group_name']])

