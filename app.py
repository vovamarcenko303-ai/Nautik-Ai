from flask import Flask, request, jsonify
import os

app = Flask(__name__)

VALID_KEYS = [
    "VIP-2024", "MY-FRIEND", "TEST-123", "FRIEND-01", "FRIEND-02",
    "FRIEND-03", "FRIEND-04", "FRIEND-05", "FRIEND-06", "Stishd-07",
    "FRIEND-08", "FRIEND-09", "FRIEND-10", "PRO-2024", "Groncik-239",
    "DANYLO-VIP", "MAX-BEST", "ALEX-777", "SCHOOL-TOP", "GIFTOSR-024"
]

LOCKED_DEVICES = {}

# Зверни увагу: тут використано звичайні лапки та правильне кодування
SCRIPT_CODE = """
(function() {
    var isRunning = false;
    
    function createModal() {
        if (document.getElementById('nurix-modal')) return;
        
        var modal = document.createElement('div');
        modal.id = 'nurix-modal';
        // Новий дизайн: більш сучасний, градієнтний, з іншими кольорами
        modal.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(10,10,15,0.95);z-index:2147483647;display:flex;justify-content:center;align-items:center;backdrop-filter:blur(8px);';
        
        modal.innerHTML = `
            <div style="background:linear-gradient(135deg, #1e1e24 0%, #121216 100%); border:1px solid #333; border-radius:20px; padding:35px 25px; width:330px; text-align:center; box-shadow:0 20px 40px rgba(0,0,0,0.8); font-family: -apple-system, sans-serif; position:relative; overflow:hidden;">
                
                <div style="position:absolute; top:0; left:0; width:100%; height:4px; background:linear-gradient(90deg, #ff9800, #ff5722);"></div>

                <h2 style="color:#fff; font-size:26px; margin:0 0 5px 0; font-weight:800; letter-spacing:1px;">NURIX</h2>
                <p style="color:#ff9800; font-size:11px; margin:0 0 25px 0; text-transform:uppercase; letter-spacing:2px; font-weight:bold;">Naurok Helper</p>
                
                <div style="background:#2a2a30; border-radius:12px; padding:5px; margin-bottom:20px; border:1px solid #444;">
                    <input type="text" id="nurix-key" placeholder="Введіть ключ..." style="width:100%; padding:15px; background:transparent; border:none; color:white; font-size:16px; text-align:center; box-sizing:border-box; outline:none;">
                </div>
                
                <button id="nurix-activate" style="width:100%; padding:16px; background:linear-gradient(90deg, #4CAF50, #2E7D32); color:white; border:none; border-radius:12px; font-size:16px; font-weight:bold; cursor:pointer; margin-bottom:20px; transition:0.2s; box-shadow:0 4px 15px rgba(76, 175, 80, 0.3);">Активувати</button>
                
                <div style="width:100%; height:1px; background:#333; margin-bottom:20px;"></div>

                <a href="https://t.me/fojuxu" target="_blank" style="display:flex; justify-content:center; align-items:center; gap:10px; width:100%; padding:14px; background:transparent; color:#0088cc; text-decoration:none; border:1px solid #0088cc; border-radius:12px; font-size:14px; font-weight:bold; box-sizing:border-box;">
                    <span>Купити ключ</span>
                </a>
            </div>
        `;
        document.body.appendChild(modal);

        document.getElementById('nurix-activate').onclick = function() {
            var key = document.getElementById('nurix-key').value.trim();
            if (!key) return;
            
            var btn = this;
            btn.innerText = 'Перевірка...';
            btn.style.background = '#555';

            var str = navigator.userAgent + screen.width + screen.height;
            var hash = 0;
            for (var i = 0; i < str.length; i++) hash = ((hash << 5) - hash) + str.charCodeAt(i);
            var devId = "DEV-" + Math.abs(hash);

            GM_xmlhttpRequest({
                method: 'POST',
                url: 'https://naurok-ai.onrender.com/api/verify',
                headers: { 'Content-Type': 'application/json' },
                data: JSON.stringify({ licenseKey: key, deviceId: devId }),
                onload: function(res) {
                    if (res.status === 200) {
                        localStorage.setItem('my_naurok_key', key);
                        modal.remove();
                        startMainScript();
                    } else {
                        btn.innerText = 'Активувати';
                        btn.style.background = 'linear-gradient(90deg, #4CAF50, #2E7D32)';
                        alert('Невірний ключ');
                    }
                },
                onerror: function() {
                    btn.innerText = 'Активувати';
                    btn.style.background = 'linear-gradient(90deg, #4CAF50, #2E7D32)';
                    alert('Сервер недоступний');
                }
            });
        };
    }

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

    var savedKey = localStorage.getItem('my_naurok_key');
    if (savedKey) {
        startMainScript();
    } else {
        createModal();
    }
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
    
    # Вказуємо кодування UTF-8
    response = jsonify({"status": "ok", "script": SCRIPT_CODE})
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response, 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
