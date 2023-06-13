from flask import Blueprint, render_template, session, request, flash, url_for, g, Flask
from werkzeug.utils import redirect

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