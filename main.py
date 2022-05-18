import logging
from config_parse import get_config

LOGGER = logging.getLogger()


if __name__ == "__main__":

    config = get_config("config.cfg")

    logging.basicConfig(
        format="%(name)s - %(levelname)s - %(message)s",
        level=logging.DEBUG if config["LOGGING"]["Level"] == "debug" else logging.INFO,
        filename=config["LOGGING"]["Path"],
    )



