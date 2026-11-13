from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Твої важкі ключі
VALID_KEYS = [
    "NURIX-A8F2-K9L1",
    "NURIX-B3X7-M4P9",
    "PRO-VIP-2024-XYZ",
    "FRIEND-QW8-ER4",
    "FRIEND-AS6-DF2",
    "FRIEND-ZX9-CV5",
    "DANYLO-777-MAX",
    "ALEX-TOP-2025",
    "SCHOOL-GOD-99",
    "GIFT-ULTRA-1",
    "MY-PRIVATE-KEY-01",
    "TESTER-ALPHA-1",
    "TESTER-BETA-2",
    "VIP-GOLD-ACCESS",
    "PREMIUM-NURIX-1",
    "PREMIUM-NURIX-2",
    "LUCKY-STRIKE-7",
    "MASTER-KEY-999",
    "NINJA-HACK-2024",
    "TITAN-FALL-88",
    "OMEGA-POINT-5",
    "DELTA-FORCE-3",
    "SIGMA-RULE-1",
    "ALPHA-WOLF-0"
]

# Тут зберігається прив'язка ключа до пристрою
LOCKED_DEVICES = {}

@app.route('/')
def home():
    return "Server is running!"

@app.route('/api/verify', methods=['POST'])
def verify():
    data = request.json
    key = data.get('licenseKey')
    device_id = data.get('deviceId')

    # Перевірка, чи є такий ключ у списку
    if key not in VALID_KEYS:
        return jsonify({"status": "error", "message": "Invalid key"}), 403

    # Перевірка, чи не зайнятий ключ іншим телефоном
    if key in LOCKED_DEVICES and LOCKED_DEVICES[key] != device_id:
        return jsonify({"status": "error", "message": "Key locked"}), 403

    # Прив'язуємо ключ до цього пристрою
    LOCKED_DEVICES[key] = device_id
    
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
