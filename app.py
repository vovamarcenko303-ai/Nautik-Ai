from flask import Flask, request, jsonify
import os

app = Flask(__name__)

VALID_KEYS = [
    "VIP-2024",
    "MY-FRIEND",
    "TEST-123"
    "admines-2376"
]

LOCKED_DEVICES = {}

@app.route('/')
def home():
    return "Server is running!"

@app.route('/api/verify', methods=['POST'])
def verify():
    data = request.json
    key = data.get('licenseKey')
    device_id = data.get('deviceId')

    if key not in VALID_KEYS:
        return jsonify({"error": "Невірний ключ"}), 403

    if key in LOCKED_DEVICES and LOCKED_DEVICES[key] != device_id:
        return jsonify({"error": "Ключ вже використовується на іншому пристрої"}), 403

    LOCKED_DEVICES[key] = device_id
    return jsonify({"status": "ok", "message": "Ключ активовано"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
