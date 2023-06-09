from flask import Blueprint, render_template

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/')
def index():
    return render_template('main/main.html')

@bp.route('/adv')
def adv():
    return render_template('main/advertise.html')