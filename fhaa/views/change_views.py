"""
개인 정보 수정 페이지
"""
from flask import Blueprint, url_for, render_template, flash, request, session, g, Flask
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
from fhaa import db
from fhaa.forms import UserUpdateForm, HospitalUpdateForm, UserDeleteForm, HospitalDeleteForm
from fhaa.models import User, Hospital, HosSub
from fhaa.views.auth_views import login_required_for_patient, login_required_all

bp = Blueprint('change', __name__, url_prefix='/change')

@bp.route('/')
def change():
    user_type = session.get('user_type')
    if user_type == "patient": # 일반 사용자 로그인
        return redirect(url_for('change.change_patient'))
    
    elif user_type == "hospital": # 병원 로그인
        return redirect(url_for('change.change_hospital'))
        
        
        

@bp.route('/patient/', methods=['GET', 'POST'])
@login_required_for_patient
def change_patient():
    
    user = User.query.filter_by(pat_ema=g.user.pat_ema)
    form = UserUpdateForm(name=g.user.pat_name, phone=g.user.pat_tel)
    
    if request.method == 'POST' and form.validate_on_submit():
        
        if check_password_hash(user.first().pat_pw, form.old_password.data):
            # 새로운 비밀번호가 존재할 경우 그 비밀번호로 변경
            if form.new_password1.data:
                user.update(dict(
                        pat_name=form.name.data, 
                        pat_pw=generate_password_hash(form.new_password1.data),
                        pat_tel=form.phone.data
                        ))
            # 새로운 비밀번호가 존재하지 않을 경우 기존 비밀번호를 다시 넣음
            else:
                user.update(dict(
                        pat_name=form.name.data, 
                        pat_pw=generate_password_hash(form.old_password.data),
                        pat_tel=form.phone.data
                        ))
                
            db.session.add(user.first())
            db.session.commit()
        else:
            flash('비밀번호 틀림ㅋㅋ')
        
        return redirect(url_for('change.change_patient'))
    
    return render_template('change/changeN.html', form=form)
    

    
@bp.route('/hospital/', methods=['GET', 'POST'])
def change_hospital():
    
    user = Hospital.query.filter_by(hos_cid=g.user.hos_cid)
    subject = HosSub.query.join(Hospital, Hospital.hos_cid==HosSub.hos_cid).filter(Hospital.hos_cid==g.user.hos_cid)
    hos_address1, hos_address2 = g.user.hos_addr.split(";block;")
    form = HospitalUpdateForm(name=g.user.hos_name, address1=hos_address1, address2=hos_address2, tel=g.user.hos_tel)
    subjects = [ x.ill_pid for x in subject.all() ]
    
    if request.method == 'POST' and form.validate_on_submit():
        
        if check_password_hash(user.first().hos_pwd, form.old_password.data):
            
            # 새로운 비밀번호가 존재할 경우 그 비밀번호로 변경
            if form.new_password1.data:
                user.update(dict(
                        hos_name=form.name.data, 
                        hos_addr=form.address1.data + ';block;' + form.address2.data,
                        hos_pwd=generate_password_hash(form.new_password1.data),
                        hos_tel=form.tel.data
                        ))
                
            # 새로운 비밀번호가 존재하지 않을 경우 기존 비밀번호를 다시 넣음
            else:
                user.update(dict(
                        hos_name=form.name.data, 
                        hos_addr=form.address1.data + ';block;' + form.address2.data,
                        hos_pwd=generate_password_hash(form.old_password.data),
                        hos_tel=form.tel.data
                        ))
                
            for del_hossub in HosSub.query.filter_by(hos_cid=user.first().hos_cid).all():
                if type(del_hossub) is HosSub:
                    db.session.delete(del_hossub)
                
            for ill_pid in form.subject.data:
                add_hossub = HosSub(hos_cid=user.first().hos_cid, ill_pid=ill_pid)
                db.session.add(add_hossub)
                
            db.session.add(user.first())
            db.session.commit()
        else:
            flash('비밀번호 틀림ㅋㅋ')
        
        return redirect(url_for('change.change_hospital'))
    
    return render_template('change/changeH.html', form=form, subjects=subjects)
    
    
@bp.route('/signout/')
@login_required_all
def signout():
    user_type = session.get('user_type')
    if user_type == "patient": # 일반 사용자
        return redirect(url_for('change.signout_patient'))
    
    elif user_type == "hospital": # 병원 
        return redirect(url_for('change.signout_hospital'))
    
    
@bp.route('/signout/patient/')
@login_required_all
def signout_patient():
    print(session.get('user_id'))
    db.session.delete(User.query.filter_by(pat_ema=session.get('user_id')).first())
    db.session.commit()
    return redirect(url_for('login.logout'))


@bp.route('/signout/hospital/')
@login_required_all
def signout_hospital():
    user = Hospital.query.filter_by(hos_cid=g.user.hos_cid)
    
    print(session.get('user_id'))
    for del_hossub in HosSub.query.filter_by(hos_cid=user.first().hos_cid).all():
        if type(del_hossub) is HosSub:
            db.session.delete(del_hossub)
        
    db.session.delete(Hospital.query.filter_by(hos_cid=session.get('user_id')).first())
    db.session.commit() 
        
    return redirect(url_for('main.index'))