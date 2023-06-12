from flask import Blueprint, render_template

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/')
def index():
    return render_template('main/main.html')

@bp.route('/im')
def im():
    return render_template('main/IM_adv.html')

@bp.route('/der')
def der():
    return render_template('main/DER_adv.html')

@bp.route('/uro')
def uro():
    return render_template('main/URO_adv.html')

@bp.route('/obgy')
def obgy():
    return render_template('main/OBGY_adv.html')

@bp.route('/oph')
def oph():
    return render_template('main/OPH_adv.html')

@bp.route('/os')
def os():
    return render_template('main/OS_adv.html')

@bp.route('/ent')
def ent():
    return render_template('main/ENT_adv.html')

@bp.route('/dt')
def dt():
    return render_template('main/DT_adv.html')

@bp.route('/pd')
def pd():
    return render_template('main/PD_adv.html')