import configparser


def get_config(path):
    config = configparser.ConfigParser()
    config["SERVER"] = {"Port": "1999", "Host": "localhost"}
    config["LOGGING"] = {"Level": "debug", "Path": "/var/log/spout/sprout.log"}

    with open(path, "w") as configfile:
        config.write(configfile)

    return config
