from flask import Flask

from blueprints.json import bp_json
from blueprints.html import bp_html


if __name__ == "__main__":
    app = Flask(__name__)

    app.register_blueprint(bp_json, url_prefix="/api/")
    app.register_blueprint(bp_html, url_prefix="/")

    app.run("0.0.0.0", 8082, debug=True)
