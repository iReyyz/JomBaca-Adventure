from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import User, Score

game_bp = Blueprint('game', __name__)

@game_bp.route('/')
@game_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@game_bp.route('/game')
@login_required
def play_game():
    return render_template('game.html', user=current_user)

@game_bp.route('/leaderboard')
@login_required
def leaderboard():
    top_players = User.query.order_by(User.xp.desc()).limit(10).all()
    return render_template('dashboard.html', user=current_user, leaderboard=top_players)
