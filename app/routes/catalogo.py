from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Modulo

catalogo_bp = Blueprint('catalogo', __name__)

@catalogo_bp.route('/modulos')
@login_required
def modulos():
    modulos = Modulo.query.all()
    return render_template('modulos.html', modulos=modulos, usuario=current_user)
