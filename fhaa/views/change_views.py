"""
개인 정보 수정 페이지
"""
from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
from flask import Blueprint, render_template
from fhaa import db


bp = Blueprint('change', __name__, url_prefix='/change')


@bp.route('/change')
def changeH():
    session['user_id'] = "test@test.com"
    # session['user_type'] = "hospital"
    session['user_type'] = "patient"


    user_id = session.get('user_type')
    if user_id == "patient":
        return render_template('change/changeN.html')
    elif user_id == "hospital":
        return render_template('change/changeH.html')

