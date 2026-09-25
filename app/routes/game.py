from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import db, User, Score

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

@game_bp.route('/save-score', methods=['POST'])
@login_required
def save_score():
    data = request.get_json()
    points = data.get('score', 0)
    
    if points > 0:
        # Update user total XP & Coins
        current_user.xp += points
        current_user.coins += (points // 10) * 2  # 2 coins per 10 pts
        current_user.level = (current_user.xp // 50) + 1  # level up every 50 XP
        
        # Save score entry
        new_score = Score(user_id=current_user.id, points=points)
        db.session.add(new_score)
        db.session.commit()
        
    return jsonify({
        'status': 'success',
        'new_xp': current_user.xp,
        'new_coins': current_user.coins,
        'new_level': current_user.level
    })

@game_bp.route('/shop')
@login_required
def shop():
    return render_template('shop.html', user=current_user)

@game_bp.route('/buy-item', methods=['POST'])
@login_required
def buy_item():
    cost = int(request.form.get('cost', 0))
    item_name = request.form.get('item_name', 'Item')
    
    if current_user.coins >= cost:
        current_user.coins -= cost
        db.session.commit()
        flash(f'Tahniah! Anda berjaya membeli {item_name}! 🎉', 'success')
    else:
        flash('Syiling tidak mencukupi untuk membeli item ini! 🪙', 'error')
        
    return redirect(url_for('game.shop'))


