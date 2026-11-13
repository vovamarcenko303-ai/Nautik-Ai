from flask import Flask, request, jsonify
import os

app = Flask(__name__)
VALID_KEYS = ["admines-2376", "NURIX-A8F2-K9L1", "VIP-2024"]

@app.route('/')
def home():
    return "OK"

@app.route('/api/verify', methods=['POST'])
def verify():
    if request.json.get('licenseKey') not in VALID_KEYS:
        return jsonify({"error": "Invalid"}), 403
    
    code = r"""
    (function() {
        var b = document.createElement('div');
        b.innerText = '💡';
        b.style.cssText = 'position:fixed;bottom:50px;left:15px;width:50px;height:50px;background:#2196F3;color:white;border-radius:50%;z-index:2147483647;opacity:0.6;display:flex;justify-content:center;align-items:center;font-size:24px;';
        
        b.onclick = function() {
            b.style.opacity = '0.2';
            var txt = document.body.innerText.substring(0, 2000).replace(/\n+/g, ' ').trim();
            var opts = [];
            var els = [];
            
            document.querySelectorAll('div, span, label, button').forEach(function(el) {
                var t = el.innerText.trim();
                if (t.length > 5 && t.length < 200 && !t.includes('Запитання') && !t.includes('Почати') && !t.includes('Добіжи') && !t.includes('LIVE') && !t.includes('Далі') && !t.includes('Завершити')) {
                    if (!opts.includes(t)) { opts.push(t); els.push(el); }
                }
            });

            if (opts.length === 0) { b.style.opacity = '0.6'; return; }

            var prompt = "Питання: " + txt + ". Варіанти: " + opts.join(' | ') + ". Дай номер правильної відповіді (1, 2, 3 або 4). Відповідай ТІЛЬКИ цифрою.";

            GM_xmlhttpRequest({
                method: "POST",
                url: "https://openrouter.ai/api/v1/chat/completions",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer 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"
                },
                data: JSON.stringify({ model: "openrouter/auto", messages: [{ role: "user", content: prompt }] }),
                onload: function(res) {
                    try {
                        var data = JSON.parse(res.responseText);
                        var ans = data.choices[0].message.content.trim();
                        var m = ans.match(/\d+/);
                        var idx = m ? parseInt(m[0]) - 1 : 0;

                        els.forEach(function(e) { e.style.backgroundColor = ''; e.style.border = ''; });

                        if (idx >= 0 && idx < els.length) {
                            els[idx].style.backgroundColor = '#4CAF50';
                            els[idx].style.color = '#fff';
                            els[idx].style.border = '4px solid #2E7D32';
                            els[idx].style.borderRadius = '10px';
                        }
                        b.style.opacity = '0.6';
                    } catch(e) { b.style.opacity = '0.6'; }
                }
            });
        };
        document.body.appendChild(b);
    })();
    """
    
    res = jsonify({"status": "ok", "script": code})
    res.headers["Content-Type"] = "application/json; charset=utf-8"
    return res, 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
