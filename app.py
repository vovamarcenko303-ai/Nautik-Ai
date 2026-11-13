from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Твої ключі
VALID_KEYS = [
    "VIP-2024", "MY-FRIEND", "TEST-123", "FRIEND-01", "FRIEND-02",
    "FRIEND-03", "FRIEND-04", "FRIEND-05", "FRIEND-06", "FRIEND-07",
    "FRIEND-08", "FRIEND-09", "FRIEND-10", "PRO-2024", "NAUROK-HELPER",
    "DANYLO-VIP", "MAX-BEST", "ALEX-777", "SCHOOL-TOP", "GIFT-2024",
    "NURIX-A8F2-K9L1", "NURIX-B3X7-M4P9", "PRO-VIP-2024-XYZ", "FRIEND-QW8-ER4"
]

LOCKED_DEVICES = {}

# Ось той самий скрипт, який сам тицяє
SCRIPT_CODE = """
(function() {
    var isRunning = false;
    function tap(element) {
        if (!element) return;
        var rect = element.getBoundingClientRect();
        var x = rect.left + rect.width / 2;
        var y = rect.top + rect.height / 2;
        ['touchstart', 'touchend', 'mousedown', 'mouseup', 'click'].forEach(function(type) {
            element.dispatchEvent(new MouseEvent(type, { view: window, bubbles: true, cancelable: true, clientX: x, clientY: y }));
        });
    }
    function startMainScript() {
        var btn = document.createElement('div');
        btn.innerText = '▶';
        btn.style.cssText = 'position:fixed;bottom:50px;left:15px;width:40px;height:40px;background:#4CAF50;color:white;border-radius:50%;z-index:2147483647;opacity:0.15;cursor:pointer;display:flex;justify-content:center;align-items:center;font-weight:bold;font-size:14px;';
        btn.onclick = function() {
            if (isRunning) { isRunning = false; btn.innerText = '▶'; btn.style.background = '#4CAF50'; return; }
            isRunning = true; btn.innerText = '⏹'; btn.style.background = '#f44336'; btn.style.opacity = '0.8'; runAutoPilot();
        };
        document.body.appendChild(btn);
    }
    function runAutoPilot() {
        if (!isRunning) return;
        var currentQuestionText = document.body.innerText.substring(0, 200).trim();
        var text = document.body.innerText.substring(0, 2000).replace(/\\n+/g, ' ').trim();
        var options = [];
        var optionElements = [];
        document.querySelectorAll('div, span, label, button').forEach(function(el) {
            var t = el.innerText.trim();
            if (t.length > 2 && t.length < 100 && !t.includes('Запитання') && !t.includes('Почати') && !t.includes('Добіжи') && !t.includes('LIVE') && !t.includes('Далі') && !t.includes('Завершити')) {
                if (/^[A-DА-Г]\\s/.test(t)) {
                    if (el.children.length === 0 || el.tagName === 'BUTTON' || el.tagName === 'LABEL') {
                        if (!options.includes(t)) { options.push(t); optionElements.push(el); }
                    }
                }
            }
        });
        if (options.length === 0) {
            var nextBtn = Array.from(document.querySelectorAll('button, div, a')).find(el => {
                var t = el.innerText.trim().toLowerCase();
                return (t === 'далі' || t === 'наступне' || t === 'завершити' || t === 'продовжити');
            });
            if (nextBtn) { tap(nextBtn); setTimeout(runAutoPilot, 2500); } else { setTimeout(runAutoPilot, 2000); }
            return;
        }
        var promptText = "Виріши тест. Питання: " + text + ". Варіанти: " + options.join(' | ') + ". Дай правильну відповідь (або декілька). Відповідай ТІЛЬКИ номерами варіантів через кому (наприклад: 1 або 1,3).";
        
        GM_xmlhttpRequest({
            method: "POST", url: "https://openrouter.ai/api/v1/chat/completions",
            headers: { "Content-Type": "application/json", "Authorization": "Bearer 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" },
            data: JSON.stringify({ model: "openrouter/auto", messages: [{role: "user", content: promptText}] }),
            onload: function(response) {
                try {
                    var data = JSON.parse(response.responseText);
                    var answer = data.choices[0].message.content.trim();
                    var matches = answer.match(/\\d+/g);
                    var targetsToClick = [];
                    if (matches && matches.length > 0) {
                        matches.forEach(function(numStr) {
                            var num = parseInt(numStr);
                            if (num >= 1 && num <= options.length) targetsToClick.push(optionElements[num - 1]);
                        });
                    } 
                    if (targetsToClick.length > 0) { stubbornClick(targetsToClick, currentQuestionText); }
                    else { setTimeout(runAutoPilot, 2000); }
                } catch(e) { setTimeout(runAutoPilot, 2000); }
            },
            onerror: function() { setTimeout(runAutoPilot, 2000); }
        });
    }
    function stubbornClick(elements, oldQuestion) {
        if (!isRunning) return;
        elements.forEach(function(el) { tap(el); });
        setTimeout(function() {
            var newQuestion = document.body.innerText.substring(0, 200).trim();
            if (newQuestion !== oldQuestion) { setTimeout(runAutoPilot, 1500); } 
            else { stubbornClick(elements, oldQuestion); }
        }, 800); 
    }
    startMainScript();
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
