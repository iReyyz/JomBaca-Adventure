from flask import Blueprint, render_template
from flask_login import login_required, current_user

battle_bp = Blueprint('battle', __name__)

@battle_bp.route('/battle')
@login_required
def battle_arena():
    return render_template('dashboard.html', user=current_user, battle_mode=True)
