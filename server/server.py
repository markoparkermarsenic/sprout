from uuid import uuid4
from flask import Flask, jsonify, request


class Server:
    def __init__(self):
        self.db = {}

    def _save_sentence(self, sentence, outcome):

        self.db[uuid4] = {"sentence": sentence, "hasFoulLanguage": outcome}

    def build_server(self, config):

        app = Flask("sprout")

        @app.route("/posts/", methods=["POST"])
        def _posts():
            out = {}
            data = request.json

            return jsonify(out)

        return app
