import json
import logging
import multiprocessing as mp
import random

from collections import OrderedDict
from flask import Flask, jsonify, request, abort
from uuid import uuid4
from werkzeug.exceptions import HTTPException

LOGGER = logging.getLogger()


class Server:
    def __init__(self):
        manager = mp.Manager()
        self.db = {}
        self.task_q, self.q = manager.Queue(), manager.Queue()

        listener = mp.Process(target=self._db_listener, daemon=True)
        listener.start()

        classifier = mp.Process(target=self._classify, daemon=True)
        classifier.start()

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
                uuid, sentence = m[1]["uuid"], m[1]["sentence"]
                self.db[uuid] = {"sentence": sentence}
                self.task_q.put((uuid, sentence))
            elif m[0] == "update_outcome":
                self.db[m[1]["uuid"]].update(
                    {"hasFoulLanguage": m[1]["hasFoulLanguage"]}
                )

    def _query_ml_api(self, *args):
        """this mocks the ML api"""

        state = random.choice([1, 2, 3])

        if state == 1:
            return {"hasFoulLanguage": True}
        elif state == 2:
            return {"hasFoulLanguage": False}
        elif state == 3:
            return None

    def _classify(self):
        retry_queue = OrderedDict()

        while True:
            if (
                self.task_q.empty()
            ):  # TODO: using exponential backoff might be better here
                success_uuids = []
                new_retry_queue = retry_queue.copy()
                for uuid, info in retry_queue.items():
                    outcome = self._query_ml_api(info["sentence"])
                    if outcome is not None:
                        success_uuids.append(uuid)
                        self.q.put(
                            (
                                "update_outcome",
                                {"uuid": uuid, "hasFoulLanguage": outcome},
                            )
                        )
                        new_retry_queue.pop(uuid)
                        LOGGER.debug(f'query for {info["sentence"]} succeeded!')
                        continue
                    info["count"] += 1
                    if info["count"] > 5:
                        LOGGER.debug(
                            f'query for {info["sentence"]} failed too many times - abandoning!'
                        )
                        new_retry_queue.pop(uuid)
                retry_queue = new_retry_queue

            uuid, sentence = self.task_q.get()
            outcome = self._query_ml_api(sentence)
            if outcome is not None:
                self.q.put(
                    (
                        "update_outcome",
                        {"uuid": uuid, "hasFoulLanguage": outcome},
                    )
                )
                LOGGER.debug(f"query for {sentence} succeeded!")
                continue

            LOGGER.debug(f"query for {sentence} failed, placing in retry queue")
            retry_queue[uuid] = {"count": 1, "sentence": sentence}

    def _generate_sentence(self, data):

        for paragraph in data["paragraphs"]:
            for sentence in paragraph.split("."):
                if sentence == "" or sentence == " ":
                    continue
                yield sentence.strip()

    def build_server(self, config):

        app = Flask("sprout")

        @app.errorhandler(HTTPException)
        def _error_handler(err):
            response = err.get_response()
            response.data = json.dumps({"SPROUT": err.name.upper() or err.description})
            response.content_type = "application/json"

            return response

        @app.route("/posts/", methods=["POST"])
        def _posts():
            data = request.json
            if "paragraphs" not in data:
                abort(400)

            uuids = [
                self._generate_uuid_for_sentence(sentence)
                for sentence in self._generate_sentence(data)
            ]
            LOGGER.debug(f"generated uuids: {uuids}")

            return jsonify({"SPROUT": "SUCCESS"})

        return app
