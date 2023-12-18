from flask import session, request, current_app, render_template


def group_permission_validator(config: dict, s: session, r: request):
    group_name = s.get('group_name', "Unauthorised")
    target_app = "" if len(r.endpoint.split('.')) == 1 else r.endpoint.split('.')[0]
    if group_name in config and target_app in config[group_name]:
        return True
    return False


def login_permission_required(f):
    def wrapper(*args, **kwargs):
        config = current_app.config['PERMISSION_CONFIG']
        if group_permission_validator(config, session, request):
            return f(*args, **kwargs)
        return render_template('permission_denied.html', group=session.get('group_name'))
    return wrapper
