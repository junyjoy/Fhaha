from flask import Blueprint, render_template

bp = Blueprint('log',__name__,url_prefix='/log')

@bp.route('/login/', methods=('GET','POST'))
def login():
    return render_template('log/login.html')

@bp.route('/pat_login/', methods=('GET','POST'))
def pat_login():
    return render_template('log/pat_login.html')

@bp.route('hos_login/', methods=('GET','POST'))
def hos_login():
    return render_template('log/hos_login.html')