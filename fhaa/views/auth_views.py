from flask import Blueprint

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup/', methods=('GET', 'POST'))
def register():
    return 'Register Page'


@bp.route('/congrats/')
def congrats():
    return 'Congrats Page'