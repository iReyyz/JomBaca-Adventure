from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import db, User, Score, QuestionHistory

game_bp = Blueprint('game', __name__)

@game_bp.route('/')
@game_bp.route('/dashboard')
@login_required
def dashboard():
    today_str = datetime.utcnow().strftime('%Y-%m-%d')
    daily_completed = (current_user.last_daily_date == today_str)
    
    # Semak status EXP Boost aktif atau tidak
    boost_active = False
    if current_user.exp_boost_until and current_user.exp_boost_until > datetime.utcnow():
        boost_active = True
        
    return render_template('dashboard.html', user=current_user, daily_completed=daily_completed, boost_active=boost_active)

@game_bp.route('/game')
@login_required
def play_game():
    return render_template('game.html', user=current_user)

@game_bp.route('/get-seen-questions', methods=['GET'])
@login_required
def get_seen_questions():
    # Ambil soalan yang pernah dijawab pengguna dalam masa 7 hari terakhir
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent_records = QuestionHistory.query.filter(
        QuestionHistory.user_id == current_user.id,
        QuestionHistory.seen_at >= seven_days_ago
    ).all()
    seen_ids = [r.question_id for r in recent_records]
    return jsonify({'seen_ids': seen_ids})

@game_bp.route('/record-questions', methods=['POST'])
@login_required
def record_questions():
    data = request.get_json() or {}
    q_ids = data.get('question_ids', [])
    for q_id in q_ids:
        rec = QuestionHistory(user_id=current_user.id, question_id=q_id)
        db.session.add(rec)
    db.session.commit()
    return jsonify({'status': 'success'})

@game_bp.route('/save-score', methods=['POST'])
@login_required
def save_score():
    data = request.get_json() or {}
    points = data.get('score', 0)
    
    if points > 0:
        # Jika ada EXP boost aktif, ganda 1.5x XP
        gained_xp = points
        if current_user.exp_boost_until and current_user.exp_boost_until > datetime.utcnow():
            gained_xp = int(points * 1.5)
            
        current_user.xp += gained_xp
        current_user.coins += (points // 10) * 2  # 2 coins setiap 10 pts
        current_user.level = (current_user.xp // 50) + 1  # naik level setiap 50 XP
        
        # Simpan skor
        new_score = Score(user_id=current_user.id, points=points)
        db.session.add(new_score)
        db.session.commit()
        
    return jsonify({
        'status': 'success',
        'new_xp': current_user.xp,
        'new_coins': current_user.coins,
        'new_level': current_user.level
    })

@game_bp.route('/claim-daily', methods=['POST'])
@login_required
def claim_daily():
    today_str = datetime.utcnow().strftime('%Y-%m-%d')
    if current_user.last_daily_date == today_str:
        return jsonify({'status': 'already_claimed', 'message': 'Tugasan harian telah pun diselesaikan hari ini!'})
    
    # Beri ganjaran daily quest (+30 XP, 15 Coins)
    current_user.xp += 30
    current_user.coins += 15
    current_user.last_daily_date = today_str
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'new_xp': current_user.xp,
        'new_coins': current_user.coins,
        'message': 'Tahniah! Ganjaran harian diselesaikan! 🎉'
    })

@game_bp.route('/shop')
@login_required
def shop():
    boost_active = False
    if current_user.exp_boost_until and current_user.exp_boost_until > datetime.utcnow():
        boost_active = True
    return render_template('shop.html', user=current_user, boost_active=boost_active)

@game_bp.route('/buy-item', methods=['POST'])
@login_required
def buy_item():
    cost = int(request.form.get('cost', 0))
    item_type = request.form.get('item_type', 'item')
    item_value = request.form.get('item_value', '')
    item_name = request.form.get('item_name', 'Item')
    
    if current_user.coins >= cost:
        current_user.coins -= cost
        
        if item_type == 'avatar':
            current_user.avatar = item_value
            flash(f'Tahniah! Avatar anda kini bertukar ke {item_value} ({item_name})! 🎭', 'success')
        elif item_type == 'exp_boost':
            # Tambah 24 jam EXP boost
            now = datetime.utcnow()
            if current_user.exp_boost_until and current_user.exp_boost_until > now:
                current_user.exp_boost_until += timedelta(hours=24)
            else:
                current_user.exp_boost_until = now + timedelta(hours=24)
            flash(f'Tahniah! Anda mengaktifkan {item_name} (+50% Extra EXP) selama 24 jam! ⚡', 'success')
        else:
            flash(f'Tahniah! Anda berjaya membeli {item_name}! 🎉', 'success')
            
        db.session.commit()
    else:
        flash('Syiling tidak mencukupi untuk membeli item ini! 🪙', 'error')
        
    return redirect(url_for('game.shop'))


