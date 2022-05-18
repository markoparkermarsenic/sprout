from os import lseek
from flask import Flask, jsonify, request


class Server:
    def __init__(self):
        self.db = {}

    def _save_sentence(self, sentence, outcome):

    @app.route("/posts", methods=["POST"])
    def _posts():

    def build_server(self, config):

        app = Flask("sprout")

        @app.route("/posts/", methods=["POST"])
        def _posts():
            out = {}
            data = request.json

            return jsonify(out)

        return app
