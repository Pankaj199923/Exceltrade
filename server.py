"""
Live Excel Dashboard Server
-----------------------------------
Ye Flask server do kaam karta hai:
1. /update endpoint par POST request accept karta hai (excel_watcher.py se aati hai)
   aur naya data sab connected browsers ko instantly push kar deta hai (via WebSocket).
2. Dashboard HTML page serve karta hai jo live data dikhata hai.

Deploy karne ke liye (internet par live dikhane ke liye), is server ko kisi
free hosting par daal do — Render.com, Railway.app, ya PythonAnywhere.
Phir apne laptop wale excel_watcher.py me SERVER_URL wahi daal do.
"""

from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "mysecretkey123"
socketio = SocketIO(app, cors_allowed_origins="*")

# In-memory store — latest sheet data (naya client connect hote hi ye bhej denge)
latest_data = {
    "sheet_name": None,
    "headers": [],
    "rows": [],
    "updated_at": None
}

# Simple shared-secret so koi bhi random banda tumhare server ko update na kar paaye
API_KEY = os.environ.get("EXCEL_DASHBOARD_KEY", "mysecretkey123")


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/update", methods=["POST"])
def update_data():
    """excel_watcher.py yahan data POST karta hai jab bhi Excel save hoti hai."""
    auth = request.headers.get("X-API-Key")
    if auth != API_KEY:
        return jsonify({"error": "unauthorized"}), 401

    payload = request.get_json(force=True)
    latest_data["sheet_name"] = payload.get("sheet_name")
    latest_data["headers"] = payload.get("headers", [])
    latest_data["rows"] = payload.get("rows", [])
    latest_data["updated_at"] = payload.get("updated_at")

    # Sab connected browsers ko turant naya data bhej do
    socketio.emit("data_update", latest_data)

    return jsonify({"status": "ok", "rows_received": len(latest_data["rows"])})


@app.route("/latest", methods=["GET"])
def get_latest():
    """Page reload hone par ya naya client connect hone par latest data."""
    return jsonify(latest_data)


@socketio.on("connect")
def handle_connect():
    # Naya browser connect hote hi usko turant latest data bhej do
    socketio.emit("data_update", latest_data)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port, debug=False, allow_unsafe_werkzeug=True)
