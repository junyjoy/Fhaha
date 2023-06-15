from flask import Blueprint, render_template, session, request, flash, url_for, g, Flask
from werkzeug.utils import redirect
from fhaa.models import User, Request
from fhaa.forms import UserLoginForm, HospitalLoginForm

bp = Blueprint('request', __name__, url_prefix='/request')
app = Flask(__name__)

@bp.route('/list')
def _list():
    return render_template('request/list.html')
    
@bp.route('/view')
def views():
    return render_template('request/view.html')
    
@bp.route('/write')
def write():
    return render_template('request/write.html')

@bp.route('/board/')
def board():
    page = request.args.get('page', type=int, default=1)  # 페이지
    print(page)
    request_list = Request.query.order_by(Request.req_id.desc())
    request_list = request_list.paginate(page=page, per_page=10)

    return render_template('request/user_list.html', request_list=request_list)

@bp.route('/detail/<int:request_id>/')
def detail(request_id):
    # request_list = Request.query.get_or_404(request_id)

    return render_template('request/user_detail.html', request=request)

@bp.route('/user_hoslist/')
def user_list():
    page = request.args.get('page', type=int, default=1)  # 페이지
    print(page)
    request_list = Request.query.filter_by(pat_ema=g.user.pat_ema)
    request_list = request_list.paginate(page=page, per_page=10)

    return render_template('request/user_list.html', request_list=request_list)