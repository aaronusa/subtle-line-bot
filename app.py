from flask import Flask
from flask_cors import CORS
import os

from controller.routes import config_route


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

config_route(app)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
