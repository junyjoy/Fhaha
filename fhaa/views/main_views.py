from flask import Blueprint, render_template
from fhaa.models import Hospital, HosSub, Subject
import sqlalchemy

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/')
def index():
    return render_template('main/main.html')

@bp.route('/im')
def im():
    hos = Hospital.query.join(HosSub).join(Subject).filter(Hospital.hos_cid==HosSub.hos_cid, Subject.ill_type=="내과").all()

    return render_template('main/IM_adv.html',hoslist=hos)

@bp.route('/der')
def der():
    hos = Hospital.query.join(HosSub).join(Subject).filter(Hospital.hos_cid==HosSub.hos_cid, Subject.ill_type=="피부과").all()

    return render_template('main/DER_adv.html',hoslist=hos)

@bp.route('/uro')
def uro():
    hos = Hospital.query.join(HosSub).join(Subject).filter(Hospital.hos_cid==HosSub.hos_cid, Subject.ill_type=="비뇨의학과").all()

    return render_template('main/URO_adv.html',hoslist=hos)

@bp.route('/obgy')
def obgy():
    hos = Hospital.query.join(HosSub).join(Subject).filter(Hospital.hos_cid==HosSub.hos_cid, Subject.ill_type=="산부인과").all()

    return render_template('main/OBGY_adv.html',hoslist=hos)

@bp.route('/oph')
def oph():
    hos = Hospital.query.join(HosSub).join(Subject).filter(Hospital.hos_cid==HosSub.hos_cid, Subject.ill_type=="안과").all()

    return render_template('main/OPH_adv.html',hoslist=hos)

@bp.route('/os')
def os():
    hos = Hospital.query.join(HosSub).join(Subject).filter(Hospital.hos_cid==HosSub.hos_cid, Subject.ill_type=="정형외과").all()

    return render_template('main/OS_adv.html',hoslist=hos)

@bp.route('/ent')
def ent():
    hos = Hospital.query.join(HosSub).join(Subject).filter(Hospital.hos_cid==HosSub.hos_cid, Subject.ill_type=="이비인후과").all()

    return render_template('main/ENT_adv.html',hoslist=hos)

@bp.route('/dt')
def dt():
    hos = Hospital.query.join(HosSub).join(Subject).filter(Hospital.hos_cid==HosSub.hos_cid, Subject.ill_type=="치과").all()

    return render_template('main/DT_adv.html',hoslist=hos)

@bp.route('/pd')
def pd():
    hos = Hospital.query.join(HosSub).join(Subject).filter(Hospital.hos_cid==HosSub.hos_cid, Subject.ill_type=="소아과").all()

    return render_template('main/PD_adv.html',hoslist=hos)