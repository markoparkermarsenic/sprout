from celery import Celery
from uuid import uuid4
from flask import Flask, jsonify, request, abort


class Server:
    def __init__(self):
        self.db = {}
        self.queue = []

    def _generate_uuid_for_sentence(self, sentence, outcome=None):
        """For a uuid to be generated, a sentence must be saved to the db"""

        uuid = uuid4()
        self.db[uuid] = {"sentence": sentence, "hasFoulLanguage": outcome}
        return uuid

    def build_server(self, config):

        app = Flask("sprout")

        @app.route("/posts/", methods=["POST"])
        def _posts():
            data = request.json
            if "sentence" not in data:
                abort(400)

            for sentence in data["sentence"]:
                uuid = self._generate_uuid_for_sentence(sentence)
                self._classify(uuid)

            return jsonify({"SPROUT": "SUCCESS"})

        return app
