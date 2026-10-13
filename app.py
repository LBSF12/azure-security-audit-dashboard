from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "application": "Azure Security Audit Dashboard",
        "version": "1.0.0",
        "status": "running"
    })


@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    app.run(debug=True)