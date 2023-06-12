"""
개인 정보 수정 페이지
"""
from flask import Blueprint, url_for, render_template, flash, request, session, g, Flask
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
from flask import Blueprint, render_template
from fhaa import db
from fhaa.models import User


bp = Blueprint('change', __name__, url_prefix='/change')
app = Flask(__name__)

@bp.route('/change')
def change():
    # session['user_id'] = "test@test.com"
    # session['user_type'] = "hospital"
    # session['user_type'] = "patient"

    user_type = session.get('user_type')
    
    if user_type == "patient":
        test_user = User.query.get(session.get('user_id'))
        name = test_user.pat_name
        phone = test_user.pat_tel
        
        return render_template('change/changeN.html', name = name, phone = phone)
    elif user_type == "hospital":
        return render_template('change/changeH.html')
    else:
        return redirect(url_for('main.index'))

