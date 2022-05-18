from os import lseek
from flask import Flask, jsonify, request


def build_server(config):

    app = Flask("sprout")

    @app.route("/posts", methods=["POST"])
    def _posts():

        data = request.form

    return app
