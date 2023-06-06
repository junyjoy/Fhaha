"""
회원가입, 가입축하
Authors: jlee (junlee9834@gmail.com)
"""

from flask import Blueprint, render_template


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    return render_template('auth/signup.html')


@bp.route('/congrats/')
def congrats():
    return render_template('auth/congrats.html')

