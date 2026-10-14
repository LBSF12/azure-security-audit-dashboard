from flask import Flask, jsonify
import os
from datetime import datetime

import psycopg
from flask import jsonify
app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "application": "Azure Security Audit Dashboard",
        "version": "1.2.0",
        "status": "running",
        "deployment": "Automated using GitHub Actions CI/CD"
    })


@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

@app.get("/audit-events")
def get_audit_events():
    db_host = os.environ.get("DB_HOST", "db")
    db_name = os.environ.get("DB_NAME", "auditdb")
    db_user = os.environ.get("DB_USER", "audituser")
    db_password = os.environ.get("DB_PASSWORD")

    if not db_password:
        return jsonify({"error": "Database not configured"}), 503

    try:
        with psycopg.connect(
            host=db_host,
            dbname=db_name,
            user=db_user,
            password=db_password,
            connect_timeout=5
        ) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, server_name, event_type, created_at
                    FROM audit_events
                    ORDER BY id
                """)

                records = cur.fetchall()

        events = [
            {
                "id": row[0],
                "server_name": row[1],
                "event_type": row[2],
                "created_at": row[3].isoformat()
            }
            for row in records
        ]

        return jsonify({
            "total": len(events),
            "events": events
        })

    except psycopg.Error:
        app.logger.exception("Database query failed")
        return jsonify({"error": "Database temporarily unavailable"}), 503


if __name__ == "__main__":
    app.run(debug=True)