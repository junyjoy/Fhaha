from flask import Blueprint, render_template

bp = Blueprint('login',__name__,url_prefix='/login')

@bp.route('/', methods=('GET','POST'))
def login():
    return render_template('log/login.html')

<<<<<<< HEAD
@bp.route('/pat', methods=('GET','POST'))
def pat_login():
    return render_template('log/pat_login.html')

@bp.route('/hos', methods=('GET','POST'))
=======
@bp.route('/pat/', methods=('GET','POST'))
def pat_login():
    return render_template('log/pat_login.html')

@bp.route('/hos/', methods=('GET','POST'))
>>>>>>> 2287bcee65032b95035602aaaa43d31034b62e62
def hos_login():
    return render_template('log/hos_login.html')