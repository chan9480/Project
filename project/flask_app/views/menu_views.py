from flask import Blueprint, render_template
from ..database_main import get_data, get_best_games
from ..machine import learn

menu_bp = Blueprint('menu', __name__)

@menu_bp.route('/sales_games', methods = ['GET'])
def sales():
    return render_template('menu_sales_games.html', a=get_data().to_html()), 200
@menu_bp.route('/Dashboard', methods=['GET'])
def dash():
    
    return render_template('menu_dashboard.html'), 200
@menu_bp.route('/Recommended_games', methods=['GET'])
def reco():
    return render_template('menu_recommended_games.html', b=get_best_games()), 200
