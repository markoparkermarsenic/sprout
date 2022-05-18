import logging
from config_parse import get_config
from server.server import build_server

LOGGER = logging.getLogger()


if __name__ == "__main__":

    config = get_config("config.cfg")

    logging.basicConfig(
        format="%(name)s - %(levelname)s - %(message)s",
        level=logging.DEBUG if config["LOGGING"]["Level"] == "debug" else logging.INFO,
        filename=config["LOGGING"]["Path"],
    )

    app = build_server(config)
    app.run(host=config["SERVER"]["Host"], port=config["SERVER"]["Port"], debug=True)
