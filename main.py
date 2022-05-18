import logging
import multiprocessing as mp
from config_parse import get_config
from server.server import Server


LOGGER = logging.getLogger()


if __name__ == "__main__":
    mp.set_start_method("spawn")  # guarantees portability across os's

    config = get_config("config.cfg")

    logging.basicConfig(
        format="%(name)s - %(levelname)s - %(message)s",
        level=logging.DEBUG if config["LOGGING"]["Level"] == "debug" else logging.INFO,
        filename=config["LOGGING"]["Path"],
    )

    app = Server().build_server(config)
    app.run(host=config["SERVER"]["Host"], port=config["SERVER"]["Port"], debug=True)
