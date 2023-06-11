"""
회원가입/가입완료 페이지를 위한 블루프린트
Authors: jlee (junlee9834@gmail.com)
"""

from flask import Blueprint, render_template, request, url_for, session, g, flash
from fhaa.forms import UserCreateForm, HospitalCreateForm
from fhaa.models import User, Hospital
from fhaa import db
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('auth', __name__, url_prefix='/signup')


@bp.route('/')
def signup():
    return render_template('auth/signup.html')


@bp.route('/patient/', methods=('GET', 'POST'))
def patient_signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit() and g.user is None:
        user = User.query.filter_by(pat_ema=form.email.data).first()
        if not user:
            user = User(pat_ema=form.email.data,
                        pat_name=form.name.data,
                        pat_pw=generate_password_hash(form.password1.data),
                        pat_tel=form.phone.data,
                        pat_bir=form.birth.data)
            
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.congrats', _method='POST',user_id=user.pat_ema, user_name=user.pat_name))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/patient_signup.html', form=form)


@bp.route('/hospital/', methods=('GET', 'POST'))
def hospital_signup():
    form = HospitalCreateForm()
    if request.method == 'POST' and form.validate_on_submit() and g.user is None: 
        user = Hospital.query.filter_by(hos_cid=form.crn.data).first()
        if not user:
            print(form.address1.data + form.address2.data)
            user = Hospital(hos_cid=form.crn.data,
                        hos_pwd=generate_password_hash(form.password1.data),
                        hos_name=form.name.data,
                        hos_addr=form.address1.data + form.address2.data,
                        hos_tel=form.tel.data,
                        hos_type=form.type.data)
            db.session.add(user)
            db.session.commit()
            # 가입완료 페이지에서 id와 name을 표시하기 위함
            session['created_id'] = form.crn.data
            session['created_name'] = form.name.data
            return redirect(url_for('auth.congrats', _method='POST', user_id=user.hos_cid, user_name=user.hos_name))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/hospital_signup.html', form=form)


@bp.route('/congrats/', methods=('POST','GET'))
def congrats():
    if request.method == 'POST' :
        user_id = request.get_data('user_id')
        user_name = request.get_data('user_name')
        return render_template('auth/congrats.html', user_id=user_id, user_name=user_name)
    else:
        return redirect(url_for('main.index'))
    