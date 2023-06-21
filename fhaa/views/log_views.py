from flask import Blueprint, render_template, session, request, flash, url_for, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from fhaa import db
from fhaa.forms import UserLoginForm, HospitalLoginForm
from fhaa.models import User, Hospital, Subject
import datetime

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
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.pat_pw, form.password.data):
            error = "비밀번호가 일치하지 않습니다."
        if error is None:
            session.clear()
            session['user_id'] = user.pat_ema
            session['user_type'] = "patient"
            print(user)
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
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.hos_pwd, form.password.data):
            error = "비밀번호가 일치하지 않습니다."
        if error is None:
            session.clear()
            session['user_id'] = user.hos_cid
            session['user_type'] = "hospital"
            return redirect(url_for('main.index'))
        flash(error)
    return render_template('log/hos_login.html', form=form)


@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))


# @bp.before_app_request
# def load_logged_in_user():
#     user_id = session.get('user_id')
#     user_type = session.get('user_type')
#     if user_id is None:
#         g.user = None
#         g.user_type = None
#     elif user_type == "patient":
#         g.user = User.query.get(user_id)
#         g.user_type = user_type
#         g.user_name = g.user.pat_name
#     elif user_type == "patient":
#         g.user = User.query.get(user_id)
#         g.user_type = user_type
#         g.user_name = g.user.pat_name
    
        

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    user_type = session.get('user_type')
    
    if user_id is None or user_type is None:
        g.user = None
        g.user_type = None
    else:
        g.user_type = user_type
        if user_type == 'patient':
            g.user = User.query.get(user_id)    
            # if g.user != None: 
            #     g.user_name = g.user.pat_name
            # else : 
            #     g.user_name = "guest"
            #     g.user = User.query.get(user_id)         
            # g.user_name = g.user.pat_name
            
        elif user_type == 'hospital':
            g.user = Hospital.query.get(user_id)
            # g.user_name = g.user.hos_name
