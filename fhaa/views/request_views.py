from flask import Blueprint, render_template, session, request, flash, url_for, g, Flask
from werkzeug.utils import redirect
from fhaa.models import Request, Subject, Hospital, HosSub
import time, datetime
from fhaa import db
from fhaa.views.auth_views import login_required_for_patient, login_required_for_hospital

bp = Blueprint('request', __name__, url_prefix='/request')
#app = Flask(__name__)

# @bp.route('/list')
# def _list():
#     return render_template('request/list.html')
    
# @bp.route('/view')
# def views():
#     return render_template('request/view.html')

@bp.route('/', methods = ['GET'])    
@login_required_for_patient
def user_req() :
    addr_now = "경기도 군포시 산본천로 12"
    sub = Subject.query.all()
    return render_template('request/user_req.html',addr_now= addr_now, sub=sub)


@bp.route('/', methods = ['POST'])    
def req_post() :
    addr_now = request.form.get('location')
    f_req_type = request.form.get('req_type')
    f_req_time = request.form.get('req_time')
    f_pat_ema = session.get('user_id')
    f_req_date= datetime.datetime.now()
    f_req_req= request.form.get('req_req')
    
    # 가까운 병원 목록 만들기
    # update by jlee <junlee9834@gmail.com>
    location_lat = float(request.form.get('location_lat'))
    location_lon = float(request.form.get('location_lon'))
    lat_KM = 0.0091
    lon_KM = 0.0113
    hospitals = Hospital.query.join(HosSub).join(Subject)\
        .filter(Subject.ill_type==f_req_type)\
        .filter(Hospital.hos_lat >= location_lat-lat_KM, Hospital.hos_lat <= location_lat+lat_KM)\
        .filter(Hospital.hos_lnt >= location_lon-lon_KM, Hospital.hos_lnt <= location_lon+lon_KM)
    
    
    for hospital in hospitals:
        print(hospital.hos_addr1)
        r = Request(
                req_type = f_req_type, 
                req_loc = addr_now,
                req_time = f_req_time,
                req_req= f_req_req,
                pat_ema = f_pat_ema,
                req_date = f_req_date,
                hos_cid = hospital.hos_cid
            )
        db.session.add(r)          
    db.session.commit() 
    
    return redirect(url_for('main.index'))


@bp.route('/board/')
@login_required_for_hospital
def board():
    page = request.args.get('page', type=int, default=1)  # 페이지
    print(page)
    request_list = Request.query.filter_by(hos_cid=g.user.hos_cid).order_by(Request.req_id.desc())
    request_list = request_list.paginate(page=page, per_page=10)
 
    return render_template('request/user_list.html', request_list=request_list)


@bp.route('/detail/<int:request_id>/')
def detail(request_id):
    # request_list = Request.query.get_or_404(request_id)

    return render_template('request/user_detail.html', request=request)


@bp.route('/user_hoslist/')
def user_list():
    page = request.args.get('page', type=int, default=1)  # 페이지
    request_list = Request.query.filter(Request.pat_ema==g.user.pat_ema)
    request_list = request_list.paginate(page=page, per_page=10)

    return render_template('request/user_list.html', request_list=request_list)



@bp.route('/hospitals/')
def hospital_list():
    """환자 관점에서 환자의 의뢰를 수락한 병원들의 목록을 보여줌.

    Returns:
        render_template: request/hospital_list.html
        
    Authors: jlee <junlee9834@gmail.com>
    """
    page = request.args.get('page', type=int, default=1)  # 페이지
    print(page)
    hospital_list = Request.query.join(Hospital).filter(Request.pat_ema==g.user.pat_ema, Request.req_chk==0)
    hospital_list = hospital_list.paginate(page=page, per_page=10)

    return render_template('request/hospital_list.html', hospital_list=hospital_list)



@bp.route('/match/done/')
def match_():
    if request.method == 'POST' :
        user_id = request.args.get('user_id')
        request.get_data()
        user_name = request.args.get('user_name')
        print(user_id, user_name)
        return render_template('auth/congrats.html', user_id=user_id, user_name=user_name)
    else:
        # return redirect(url_for('main.index'))
        return render_template('request/matched.html')
