from flask import Blueprint, render_template

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    return render_template('base.html')


@bp.route('/congrats/')
def congrats():
    return render_template('base.html')