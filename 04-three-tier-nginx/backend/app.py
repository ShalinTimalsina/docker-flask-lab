"""
Backend Flask API connected to PostgreSQL.
Handles messages storage and health checks for 3-tier Nginx lab.
"""
import os
import time
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

# Read database credentials from environment variables
DB_HOST = os.environ.get("DB_HOST", "database")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "appdb")
DB_USER = os.environ.get("DB_USER", "appuser")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "apppass123")


def get_db_connection():
    """Helper function to establish a connection to PostgreSQL."""
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


def init_db(max_retries=10, delay_seconds=2):
    """
    Retry loop on startup: Waits for PostgreSQL to accept connections,
    then creates the messages table if it does not already exist.
    """
    for attempt in range(1, max_retries + 1):
        try:
            print(f"[Database] Connection attempt {attempt}/{max_retries}...")
            conn = get_db_connection()
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS messages (
                        id SERIAL PRIMARY KEY,
                        text TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
            conn.commit()
            conn.close()
            print("[Database] Successfully connected and verified table schema.")
            return True
        except psycopg2.OperationalError as error:
            print(f"[Database] Waiting for database ({error}). Retrying in {delay_seconds}s...")
            time.sleep(delay_seconds)

    print("[Database] ERROR: Could not connect to database after maximum retries.")
    return False


# Initialize database table on server startup
init_db()


@app.route("/", methods=["GET"])
def index():
    """Root endpoint welcoming visitors and listing available API endpoints."""
    return jsonify({
        "message": "Flask 3-Tier Backend API is running!",
        "status": "online",
        "endpoints": {
            "health": "/api/health",
            "message": "/api/message"
        }
    }), 200


@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint that verifies API and database connectivity."""
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({
            "status": "healthy",
            "database": "connected"
        }), 200
    except Exception as error:
        return jsonify({
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(error)
        }), 500


@app.route("/api/message", methods=["GET"])
def get_latest_message():
    """Returns the most recently saved message from PostgreSQL."""
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT text, created_at FROM messages ORDER BY id DESC LIMIT 1;")
            row = cur.fetchone()
        conn.close()

        if row:
            return jsonify({
                "message": row[0],
                "created_at": str(row[1])
            }), 200
        else:
            return jsonify({
                "message": None
            }), 200
    except Exception as error:
        return jsonify({
            "error": "Failed to fetch message",
            "details": str(error)
        }), 500


@app.route("/api/message", methods=["POST"])
def save_message():
    """Saves a new message text sent via JSON payload."""
    data = request.get_json(silent=True) or {}
    text = data.get("text", "").strip()

    if not text:
        return jsonify({
            "error": "The 'text' field is required and cannot be empty."
        }), 400

    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO messages (text) VALUES (%s) RETURNING id, text, created_at;",
                (text,)
            )
            saved_row = cur.fetchone()
        conn.commit()
        conn.close()

        return jsonify({
            "status": "success",
            "message": saved_row[1],
            "id": saved_row[0]
        }), 201
    except Exception as error:
        return jsonify({
            "error": "Failed to save message",
            "details": str(error)
        }), 500


if __name__ == "__main__":
    # Local fallback for direct execution
    app.run(host="0.0.0.0", port=5000)
