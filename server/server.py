from uuid import uuid4
from click import edit
from flask import Flask, jsonify, request, abort
import logging
import multiprocessing as mp

LOGGER = logging.getLogger()


class Server:
    def __init__(self):
        manager = mp.Manager()
        self.db = {}
        self.shared_db, self.q = manager.Queue(1), manager.Queue()

        listener = mp.Process(target=self._db_listener, daemon=True)
        listener.start()

    def _generate_uuid_for_sentence(self, sentence):
        """For a uuid to be generated, a sentence must be saved to the db"""

        uuid = uuid4()
        self.q.put(("new_entry", {"sentence": sentence, "uuid": uuid}))
        return uuid

    def _db_listener(self):
        LOGGER.info("Polling!")

        while True:
            m = self.q.get()
            if m[0] == "new_entry":
                self.db[m[1]["uuid"]] = {"sentence": m[1]["sentence"]}
            if m[0] == "update_outcome":
                self.db[m[1]["uuid"]].update(
                    {"hasFoulLanguage": m[1]["hasFoulLanguage"]}
                )
            if self.shared_db.full():
                self.shared_db.get()
            self.shared_db.put(self.db)

    def _classify(self, uuid):
        db = self.shared_db.get()
        LOGGER.info(db[uuid])

    def _generate_sentence(self, data):

        for paragraph in data["paragraphs"]:
            for sentence in paragraph.split("."):
                if sentence == "" or sentence == " ":
                    continue
                yield sentence.strip()

    def build_server(self, config):

        app = Flask("sprout")

        @app.route("/posts/", methods=["POST"])
        def _posts():
            data = request.json
            if "paragraphs" not in data:
                abort(400)

            uuids = [
                self._generate_uuid_for_sentence(sentence)
                for sentence in self._generate_sentence(data)
            ]

            for uuid in uuids:
                self._classify(uuid)

            return jsonify({"SPROUT": "SUCCESS"})

        return app
