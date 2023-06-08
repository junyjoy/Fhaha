"""
회원가입, 가입축하
Authors: jlee (junlee9834@gmail.com)
"""

from flask import Blueprint, render_template, request, url_for, g, flash
from fhaa.forms import UserCreateForm, HospitalCreateForm
from fhaa.models import User, Hospital
from fhaa import db
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup/')
def signup():
    return render_template('auth/signup.html')

@bp.route('/signup/hospital/', methods=('GET', 'POST'))
def hospital_signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(pat_ema=form.email.data).first()
        if not user:
            user = User(pat_ema=form.email.data,
                        pat_name=form.name.data,
                        password=generate_password_hash(form.password1.data),
                        pat_tel=form.phone.data,
                        pat_bir=form.birth.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth/congrats'))
        else:
            flash('이미 존재하는 일반 사용자입니다.')
    return render_template('auth/hospital_signup.html', form=form)


@bp.route('/signup/patient/', methods=('GET', 'POST'))
def patient_signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(pat_ema=form.email.data).first()
        if not user:
            user = User(pat_ema=form.email.data,
                        pat_name=form.name.data,
                        pat_pw=generate_password_hash(form.password1.data),
                        pat_tel=form.phone.data,
                        pat_bir=form.birth.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth/congrats'))
        else:
            flash('이미 존재하는 병원 사용자입니다.')
    return render_template('auth/patient_signup.html', form=form)


@bp.route('/congrats/')
def congrats():
    return render_template('auth/congrats.html')

