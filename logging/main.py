from flask import Flask, jsonify

from utils import Logger
from utils.logging_decorators import extend_logging_context
from modules.mod1 import function_from_mod1
from modules.mod2 import function_from_mod2

LOGGER = Logger(__file__)
LOG = LOGGER.get_logger()

app = Flask(__name__)


@app.route("/")
@extend_logging_context
def default_route():
    LOG.info("Hello from default route!")
    function_from_mod1()
    function_from_mod2()

    return jsonify("Hello from default route!")


@app.route("/eddy")
@extend_logging_context
def eddy_route():
    LOG.info("Hello from /eddy route!")
    function_from_mod1()
    function_from_mod2()

    return jsonify("Hello from /eddy route!")


if __name__ == "__main__":
    app.run(port=5000)
