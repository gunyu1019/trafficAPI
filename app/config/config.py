import os

from configparser import ConfigParser
from app.directory import directory


def get_config(name: str = "config") -> ConfigParser:
    parser = ConfigParser()
    parser.read(
        os.path.join(
            directory,
            "config",
            "{0}.ini".format(name)
        ),
        encoding="utf-8"
    )
    return parser
