from flask import Blueprint, render_template

bp = Blueprint('login',__name__,url_prefix='/login')

@bp.route('/', methods=('GET','POST'))
def login():
    return render_template('log/login.html')

@bp.route('/pat/', methods=('GET','POST'))
def pat_login():
    return render_template('log/pat_login.html')

@bp.route('/hos/', methods=('GET','POST'))
def hos_login():
    return render_template('log/hos_login.html')


@bp.route('/', methods=('GET','POST'))
def logout():
    return render_template('log/login.html')