from flask import Flask
from flask_cors import CORS
import os

from controller.routes import config_route


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

config_route(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
