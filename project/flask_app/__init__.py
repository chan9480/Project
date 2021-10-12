import os
from flask import Flask
from .machine import learn
from .database_main import get_data_to_anal

b=learn()
b.df=get_data_to_anal()
b.target = 'rating'
b.graph_x_aixs = 'origin_performance'
b.graph_y_axis = 'rating'
b.make_graph

def create_app(config=None):
    app = Flask(__name__)

    if config is not None:
        app.config.update(config)
    
    # 왜 여기에서 import 를 하고 있을까요?
    # 맨 위로 옮기게 되면 어떻게 되나요? 어떤 잠재적 문제들이 있나요?
    from flask_app.views.main_views import main_bp
    from flask_app.views.menu_views import menu_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(menu_bp)

    return app
    

if __name__ == "__main__":
    app.run(debug=True)
