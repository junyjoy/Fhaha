from flask import Blueprint, render_template, session, request, flash, url_for, g, Flask
from werkzeug.utils import redirect
from fhaa.models import Request
import time
from fhaa import db

bp = Blueprint('request', __name__, url_prefix='/request')
app = Flask(__name__)

@bp.route('/list')
def _list():
    return render_template('request/list.html')
    
@bp.route('/view')
def views():
    return render_template('request/view.html')
    
@bp.route('/write', methods=["GET"])
def write():
    addr = "서울시 강남구 학동로 171 1,2층"
    pat_ema = session['user_id']
    return render_template('request/write.html', addr = addr,pat_ema=pat_ema )

bp.route('/write', methods=["POST"])
def write_db():
    req_time = request.form.get('req_time')
    req_type = request.form.get('req_type') 
    req_req = request.form.get('req_req') 
    addr = "서울시 강남구 학동로 171 1,2층"
    req_loc = addr
    req_rid =""
    pat_ema = session['user_id']
    lt = time.localtime(time.time() + int(req_time) * 60)
    print(time.strftime('%Y-%m-%d %H:%M:%S', lt))
    print( req_time, req_type, req_req)
    req = Request(req_type, req_loc, lt, req_req,req_rid, pat_ema)
           
    db.session.add(req)            
    db.session.commit()
    
    
    return redirect('/')