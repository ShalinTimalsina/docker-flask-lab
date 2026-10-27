"""
Flask application for Multi-stage Docker lab.
Provides JSON endpoints served by Gunicorn.
"""
from flask import Flask, jsonify

app = Flask(__name__)

# Root endpoint returning greeting and environment status
@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "message": "Welcome to Flask Multi-Stage Lab!",
        "status": "running",
        "server": "gunicorn"
    }), 200

# Health check endpoint for container health probes
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy"
    }), 200

if __name__ == "__main__":
    # Local fallback for direct execution
    app.run(host="0.0.0.0", port=5000)
