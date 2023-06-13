"""
개인 정보 수정 페이지
"""
from flask import Blueprint, url_for, render_template, flash, request, session, g, Flask
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
from fhaa import db
from fhaa.forms import UserCreateForm
from fhaa.models import User


bp = Blueprint('change', __name__, url_prefix='/')
app = Flask(__name__)

@bp.route('/change', methods=['GET'])
def change_get():
    
    user_type = session.get('user_type')

    if user_type == "patient": # 일반 사용자 로그인
        # user = User.query.get(g.user_id)
        form = UserCreateForm(email=g.user.pat_ema, name=g.user.pat_name, phone=g.user.pat_tel, birth=g.user.pat_bir)
        print(form.birth.data)
        return render_template('change/changeN.html', form=form)
            

    elif user_type == "hospital": # 병원 로그인
        return render_template('change/changeH.html')

    # else:
    #     return redirect(url_for('main.index'))
    

    
    
    
@bp.route('/change', methods=['POST'])
def change_post():
    
    user_type = session.get('user_type')

    # POST 변경사항 저장할 때
    if user_type == "patient": # 일반 사용자 로그인
        oldpassword = g.user.pat_pw #db 일반 사용자 패스워드
        form = UserCreateForm(name=g.user.pat_name, phone=g.user.pat_tel)
        print(form.name.data)
        return render_template('change/changeN.html', form=form)
        # checkpassword = form.password1.data #input 사용자 pw확인 
        
    elif user_type == "hospital": # 병원 로그인
        oldpassword = g.user.hos_pwd #db 일반 사용자 패스워드
        checkpassword = form.password1.data #input 사용자 pw확인 
    
    if check_password_hash(oldpassword, checkpassword):
        # 비밀번호 일치 (db, input)
        
        # 이름 변경 가능 , 비밀번호 변경 가능, 전화번호 변경 가능
        if form.name.data is None: 
            form.name.data = g.user.pat_name
            db.add(form.name.data)
            return(form.name)
        
        elif form.password1.data and form.password2.data is None: 
            form.password1.data = oldpassword
            form.password2.data = oldpassword
            return(form.password1.data, form.password2.data)
        
        elif form.password1.data != form.password2.data:
            flash("비밀번호 틀렸음 ㅋㅋ")
        
        else:
            Nuser = User(pat_name=form.name.data,
                            pat_pw=generate_password_hash(form.password1.data),
                            pat_tel=form.phone.data)
            
            # db.session.add(Nuser)
            session.query(User).filter_by(user_name = form.name.data, password1 = form.password1.data, password2 = form.password2.data)

    else:
        flash("비밀번호 틀렸음 ㅋㅋ")
    
    return render_template('mainj/main.html')