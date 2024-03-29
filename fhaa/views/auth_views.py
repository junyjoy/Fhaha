"""
회원가입/가입완료 페이지를 위한 블루프린트
Authors: jlee (junlee9834@gmail.com)
"""

from flask import Blueprint, render_template, request, url_for, session, g, flash
from fhaa.forms import UserCreateForm, HospitalCreateForm
from fhaa.models import User, Hospital, HosSub, Subject
from fhaa import db
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash
import functools
from fhaa.libs import gps

bp = Blueprint('auth', __name__, url_prefix='/signup')


@bp.route('/')
def signup():
    return render_template('auth/signup.html')


@bp.route('/patient/', methods=('GET', 'POST'))
def patient_signup():
    if g.user is None:
        form = UserCreateForm()
        
        if request.method == 'POST' and form.validate_on_submit():
            user = User.query.filter_by(pat_ema=form.email.data).first()
            # user가 없으면 새로운 user를 생성하고 auth.congrats로 리다이렉트
            if not user:
                user = User(pat_ema=form.email.data,
                            pat_name=form.name.data,
                            pat_pw=generate_password_hash(form.password1.data),
                            pat_tel=form.phone.data,
                            pat_bir=form.birth.data)
                
                db.session.add(user)
            
                db.session.commit()
                
                return redirect(url_for('auth.congrats', user_id=form.email.data, user_name=form.name.data), code=307)
            else:
                flash('이미 존재하는 사용자입니다.')
                
        return render_template('auth/patient_signup.html', form=form)
    
    else:
        return redirect(url_for('main.index'))


@bp.route('/hospital/', methods=('GET', 'POST'))
def hospital_signup():
    if g.user is None:
        form = HospitalCreateForm()
        if request.method == 'POST' and form.validate_on_submit() and g.user is None: 
            user = Hospital.query.filter_by(hos_cid=form.crn.data).first()
            if not user:
                hospital_location = gps.get_location(form.address1.data)

                user = Hospital(
                            hos_cid=form.crn.data,
                            hos_pwd=generate_password_hash(form.password1.data),
                            hos_name=form.name.data,
                            hos_addr1=form.address1.data,
                            hos_addr2=form.address2.data,
                            hos_tel=form.tel.data,
                            hos_lat=str(hospital_location[0]),
                            hos_lnt=str(hospital_location[1]),
                            hos_type=''
                        )
                db.session.add(user)
                db.session.commit()
                
                for ill_pid in form.subject.data:
                    hossub = HosSub(hos_cid=user.hos_cid, ill_pid=ill_pid)
                    db.session.add(hossub)
                db.session.commit()
                    
                # 가입완료 페이지에서 id와 name을 표시하기 위함
                return redirect(url_for('auth.congrats', user_id=user.hos_cid, user_name=user.hos_name), code=307)
            else:
                flash('이미 존재하는 사용자입니다.')
                
        return render_template('auth/hospital_signup.html', form=form)
    
    else:
        return redirect(url_for('main.index'))


@bp.route('/congrats', methods=('GET', 'POST'))
def congrats():
    if request.method == 'POST' :
        user_id = request.args.get('user_id')
        request.get_data()
        user_name = request.args.get('user_name')
        print(user_id, user_name)
        return render_template('auth/congrats.html', user_id=user_id, user_name=user_name)
    else:
        return redirect(url_for('main.index'))


def login_required_all(view):
    """모든 사용자로 로그인 후 이용할 수 있는 서비스에 사용됨
    """
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            _next = request.url if request.method == 'GET' else ''
            return redirect(url_for('login.login', next=_next))
        return view(*args, **kwargs)
    return wrapped_view


def login_required_for_patient(view):
    """환자로 로그인 후 이용할 수 있는 서비스에 사용됨
    """
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is not None and type(g.user) == Hospital:
            return redirect(url_for('main.index'))
        return view(*args, **kwargs)
    return wrapped_view


def login_required_for_hospital(view):
    """병원으로 로그인 후 이용할 수 있는 서비스에 사용됨
    """
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is not None and type(g.user) == User:
            return redirect(url_for('main.index'))
        return view(*args, **kwargs)
    return wrapped_view
