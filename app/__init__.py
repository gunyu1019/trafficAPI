import importlib.util
import logging
import os

from flask import Flask
from app.directory import directory


def create_app():
    app = Flask(__name__)
    environment = app.config.get("ENV")
    app.config['JSON_AS_ASCII'] = False
    log = logging.getLogger("app.create_app")

    views = [
        "app.views." + file[:-3] for file in os.listdir(
            os.path.join(directory, "views")
        ) if file.endswith(".py")
    ]
    for view in views:
        spec = importlib.util.find_spec(view)
        if spec is None:
            log.error("Extension Not Found: {0}".format(view))
            continue

        lib = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(lib)  # type: ignore
        except Exception as e:
            log.error("Extension Failed: {0} ({1})".format(view, e.__class__.__name__))
            if environment == "development":
                raise e
            continue

        try:
            blueprint = getattr(lib, 'bp')
        except AttributeError:
            log.error("No Entry Point Error: {0}".format(view))
            continue

        try:
            app.register_blueprint(blueprint)
        except Exception as e:
            log.error("Extension Failed: {0} ({1})".format(view, e.__class__.__name__))
            if environment == "development":
                raise e
            continue

    return app
