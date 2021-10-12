from flask import Blueprint, render_template
from ..database_main import get_data_to_anal

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods = ['GET'])
def sales():
    return render_template('index.html', a='ABC'), 200
@main_bp.route('/introduce', methods=['GET'])
def dash():
    return render_template('introduce.html'), 200
