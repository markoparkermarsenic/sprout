import configparser


def get_config(path):
    config = configparser.ConfigParser()
    config["SERVER"] = {"Port": "5000", "Host": "localhost"}
    config["LOGGING"] = {"Level": "debug", "Path": "/var/log/sprout/sprout.log"}

    with open(path, "w") as configfile:
        config.write(configfile)

    return config
