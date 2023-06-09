from flask import Blueprint, render_template, session, request, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from fhaa import db
from fhaa.forms import UserLoginForm, HospitalLoginForm
from fhaa.models import User, Hospital

bp = Blueprint('login',__name__,url_prefix='/login')

@bp.route('/', methods=('GET','POST'))
def login():
    return render_template('log/login.html')

@bp.route('/pat/', methods=('GET','POST'))
def pat_login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(pat_ema=form.email.data).first()
        if not user:
            error = "존재하지 않는 사용자임 ㅋㅋ"
        elif not check_password_hash(user.pat_pw, form.password.data):
            error = "비밀번호 틀렸음 ㅋㅋ"
        if error is None:
            session.clear()
            session['user_id'] = user.pat_ema
            return redirect(url_for('main.index'))
        flash(error)
    return render_template('log/pat_login.html', form=form)

@bp.route('/hos/', methods=('GET','POST'))
def hos_login():
    form = HospitalLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = Hospital.query.filter_by(hos_cid=form.crn.data).first()
        if not user:
            error = "존재하지 않는 사용자임 ㅋㅋ"
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호 틀렸음 ㅋㅋ"
        if error is None:
            session.clear()
            session['hospital_cid'] = user.id
            return redirect(url_for('main.index'))
        flash(error)
    return render_template('log/hos_login.html', form=form)


@bp.route('/', methods=('GET','POST'))
def logout():
    return render_template('log/login.html')
