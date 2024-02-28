from service.linebot import *


def config_route(app):
    @app.route("/hello")
    def products():
        return {"products": {"Message": "Get all products.."}}, 200

    @app.route("/callback", methods=['POST'])
    def linebot():
        linebot_server()
        return 'OK', 200

    @app.route("/push", methods=['POST'])
    def linebot_push():
        linebot_push_server()
        return 'OK', 200
