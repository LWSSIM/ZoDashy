#!/usr/bin/env python3
"""API v1 app module. For crud api """


from flask import Flask, jsonify
from backend.models.api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

app.register_blueprint(app_views)

cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.teardown_appcontext
def teardown_db(exception):
    """teardown db"""
    from backend.models import storage

    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """ 404 page not found """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
