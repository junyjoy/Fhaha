from flask import Blueprint, render_template, session, request, flash, url_for, g, Flask
from werkzeug.utils import redirect
from fhaa.models import Request, Subject, Hospital, HosSub, Matching
import time, datetime
from fhaa import db
from fhaa.views.auth_views import login_required_for_patient, login_required_for_hospital, login_required_all

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



@bp.route('/detail/<int:request_id>/')
def detail(request_id):
    # request_list = Request.query.get_or_404(request_id)

    return render_template('request/user_detail.html', request=request)


@bp.route('/board/', methods = ['POST', 'GET'])   
@login_required_all
@login_required_for_hospital
def board():
    
    if request.method == 'POST':
        check = request.form.get('check')

        if check == "accept":
            f_req_id = request.form.get('req_id')
            print(f_req_id)
            request_ = Request.query.filter_by(req_id=f_req_id)
            request_.update(dict(req_chk=0))
            print(request_)
            db.session.add(request_.first())
            db.session.commit()
        else:
            f_req_id = request.form.get('req_id')
            print(f_req_id)
            request_ = Request.query.filter_by(req_id=f_req_id)
            print(request_)
            db.session.delete(request_.first())
            db.session.commit()

        return redirect(url_for('request.board'))
    
    page = request.args.get('page', type=int, default=1)  # 페이지
    request_list = Request.query.filter_by(hos_cid=g.user.hos_cid, req_chk=1)
    request_list = request_list.paginate(page=page, per_page=10)

    return render_template('request/user_list.html', request_list=request_list)



@bp.route('/hospitals/', methods = ['POST', 'GET'])   
def hospital_list():
    """환자 관점에서 환자의 의뢰를 수락한 병원들의 목록을 보여줌.

    Returns:
        render_template: request/hospital_list.html
        
    Authors: jlee <junlee9834@gmail.com>
    """
    
    if request.method == 'POST':
        check = request.form.get('check')
        
        # 환자가 `O` 버튼을 누르면
        if check == "accept":
            f_req_id = request.form.get('req_id')
            requset_ = Request.query.filter(Request.req_id==f_req_id).first()

            # Matching 테이블에 데이터 생성
            matching = Matching(
                req_id=requset_.req_id, 
                pat_ema=requset_.pat_ema, 
                hos_cid=requset_.hos_cid
            )
            db.session.add(matching)
            
            # Request 테이블에서 매칭되지 않은 의뢰를 제거
            request_del = Request.query.filter(
                Request.req_date==requset_.req_date, 
                Request.req_chk==1
            )
            for r in request_del.all():
                db.session.delete(r)
            db.session.commit()

        # 환자가 `X` 버튼을 누르면
        else:
            f_req_id = request.form.get('req_id')
            print(f_req_id)
            request_ = Request.query.filter_by(req_id=f_req_id)
            db.session.delete(request_.first())
            db.session.commit()
            
        return redirect(url_for('request.board'))
            
    page = request.args.get('page', type=int, default=1)  # 페이지
    
    # 이미 매칭된 request는 나오지 않도록 해야 함
    # outterjoin 후 mat_id가 빈 것만 가져옴
    request_list =  Request.query.outerjoin(Matching).filter(
        Request.pat_ema==g.user.pat_ema, 
        Request.req_chk==0,    
        Matching.mat_id==None
    )

    request_list = request_list.paginate(page=page, per_page=10)

    return render_template('request/hospital_list.html', request_list=request_list)



@bp.route('/match/done/')
def match_():
    if request.method == 'POST' :
        user_id = request.args.get('user_id')
        request.get_data()
        user_name = request.args.get('user_name')
        print(user_id, user_name)
        return render_template('auth/congrats.html', user_id=user_id, user_name=user_name)
    else:
        return redirect(url_for('main.index'))

@bp.route('/match/status/')
def matching():
    '''환자와 병원 모두 현재 매칭 상태를 보여줌.
    '''
    page = request.args.get('page', type=int, default=1)  # 페이지
    print(page)

    if g.user_type == "patient":
        matching_list = Matching.query.filter(Matching.pat_ema==g.user.pat_ema)
    elif g.user_type == "hospital":
        matching_list = Matching.query.filter(Matching.hos_cid==g.user.hos_cid)
    else:
        return redirect(url_for('main.index'))
     
    matching_list = matching_list.paginate(page=page, per_page=10)

    return render_template('request/match_status.html', matching_list=matching_list)


