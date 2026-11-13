from flask import Flask, request, jsonify
import os

app = Flask(__name__)

VALID_KEYS = ["VIP-2024", "NURIX-A8F2-K9L1", "PRO-2024", "FRIEND-01"]
LOCKED_DEVICES = {}

# Той самий маленький скрипт
SCRIPT_CODE = """
(function() {
    var isRunning = false;
    function tap(el) {
        if (!el) return;
        var r = el.getBoundingClientRect();
        ['touchstart', 'touchend', 'mousedown', 'mouseup', 'click'].forEach(function(t) {
            el.dispatchEvent(new MouseEvent(t, { view: window, bubbles: true, cancelable: true, clientX: r.left + r.width/2, clientY: r.top + r.height/2 }));
        });
    }
    function start() {
        var b = document.createElement('div');
        b.innerText = '▶';
        b.style.cssText = 'position:fixed;bottom:50px;left:15px;width:40px;height:40px;background:#4CAF50;color:white;border-radius:50%;z-index:2147483647;opacity:0.15;cursor:pointer;display:flex;justify-content:center;align-items:center;font-weight:bold;font-size:14px;';
        b.onclick = function() {
            if (isRunning) { isRunning = false; b.innerText = '▶'; b.style.background = '#4CAF50'; return; }
            isRunning = true; b.innerText = '⏹'; b.style.background = '#f44336'; b.style.opacity = '0.8'; loop();
        };
        document.body.appendChild(b);
    }
    function loop() {
        if (!isRunning) return;
        var txt = document.body.innerText.substring(0, 2000).replace(/\\n+/g, ' ').trim();
        var opts = [];
        var els = [];
        document.querySelectorAll('div, span, label, button').forEach(function(el) {
            var t = el.innerText.trim();
            if (t.length > 2 && t.length < 100 && !t.includes('Запитання') && !t.includes('Почати') && !t.includes('Добіжи') && !t.includes('LIVE') && !t.includes('Далі') && !t.includes('Завершити')) {
                if (/^[A-DА-Г]\\s/.test(t)) {
                    if (el.children.length === 0 || el.tagName === 'BUTTON' || el.tagName === 'LABEL') {
                        if (!opts.includes(t)) { opts.push(t); els.push(el); }
                    }
                }
            }
        });
        if (opts.length === 0) {
            var nxt = Array.from(document.querySelectorAll('button, div, a')).find(el => {
                var t = el.innerText.trim().toLowerCase();
                return (t === 'далі' || t === 'наступне' || t === 'завершити' || t === 'продовжити');
            });
            if (nxt) { tap(nxt); setTimeout(loop, 2500); } else { setTimeout(loop, 2000); }
            return;
        }
        var p = "Виріши тест. Питання: " + txt + ". Варіанти: " + opts.join(' | ') + ". Дай правильну відповідь. Відповідай ТІЛЬКИ текстом варіанту.";
        GM_xmlhttpRequest({
            method: "POST", url: "https://openrouter.ai/api/v1/chat/completions",
            headers: { "Content-Type": "application/json", "Authorization": "Bearer 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" },
            data: JSON.stringify({ model: "openrouter/auto", messages: [{role: "user", content: p}] }),
            onload: function(res) {
                try {
                    var d = JSON.parse(res.responseText);
                    var a = d.choices[0].message.content.trim().toLowerCase();
                    var idx = -1;
                    for (var i = 0; i < opts.length; i++) {
                        if (opts[i].toLowerCase().includes(a) || a.includes(opts[i].toLowerCase().substring(2).trim())) { idx = i; break; }
                    }
                    tap((idx !== -1) ? els[idx] : els[0]);
                    setTimeout(loop, 2000);
                } catch(e) { tap(els[0]); setTimeout(loop, 2000); }
            },
            onerror: function() { tap(els[0]); setTimeout(loop, 2000); }
        });
    }
    start();
})();
"""

@app.route('/')
def home():
    return "Server is running!"

@app.route('/api/verify', methods=['POST'])
def verify():
    data = request.json
    key = data.get('licenseKey')
    device_id = data.get('deviceId')

    if key not in VALID_KEYS:
        return jsonify({"error": "Invalid key"}), 403

    if key in LOCKED_DEVICES and LOCKED_DEVICES[key] != device_id:
        return jsonify({"error": "Key locked"}), 403

    LOCKED_DEVICES[key] = device_id
    response = jsonify({"status": "ok", "script": SCRIPT_CODE})
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response, 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
