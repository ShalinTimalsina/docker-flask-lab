"""
Basic Flask application (Single-stage Docker lab).
Provides simple JSON endpoints without any database dependency.
"""
from flask import Flask, jsonify

app = Flask(__name__)

# Root endpoint returning a friendly welcome message
@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "message": "Welcome to Flask Docker Lab!",
        "status": "running"
    }), 200

# Health check endpoint for monitoring container health
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy"
    }), 200

if __name__ == "__main__":
    # Run Flask on all network interfaces (0.0.0.0) on port 5000
    app.run(host="0.0.0.0", port=5000)
