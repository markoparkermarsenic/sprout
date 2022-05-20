import unittest
from server.server import Server
from config_parse import get_config


class ServerTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.config = get_config("tests/test_config.cfg")
        super(ServerTestCase, self).__init__(*args, **kwargs)

    def setUp(self):
        app = Server().build_server(self.config)
        app.config["TESTING"] = True
        app.config["DEBUG"] = True
        self.app = app.test_client()

    def tearDown(self):
        pass  # TODO: make a clean shutdown method in server

    def test_post_bad_data(self):
        response = self.app.post(
            "/posts/",
            json={"something": "bad"},
        )
        self.assertEqual(response.status_code, 400)

    def test_post_good_data(self):
        response = self.app.post(
            "/posts/",
            json={
                "title": "This is an engaging title",
                "paragraphs": [
                    "This is the first paragraph. It contains two sentences.",
                    "This is the second parapgraph. It contains two more sentences",
                    "Third paraphraph here.",
                ],
            },
        )
        self.assertEqual(response.status_code, 200)
