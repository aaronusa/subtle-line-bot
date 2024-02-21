from flask import Flask
from flask_cors import CORS

from controller.routes import config_route


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

config_route(app)


app.run(port=5002, debug=True)
