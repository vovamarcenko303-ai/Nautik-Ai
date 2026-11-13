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
    
    # Оновлений скрипт
    code = r"""
    (function() {
        var isRunning = false;
        
        function tap(el) {
            if (!el) return;
            var r = el.getBoundingClientRect();
            var x = r.left + r.width / 2;
            var y = r.top + r.height / 2;
            ['touchstart', 'touchend', 'mousedown', 'mouseup', 'click'].forEach(function(type) {
                el.dispatchEvent(new MouseEvent(type, { view: window, bubbles: true, cancelable: true, clientX: x, clientY: y }));
            });
        }

        function start() {
            var b = document.createElement('div');
            b.innerText = '▶';
            b.style.cssText = 'position:fixed;bottom:50px;left:15px;width:50px;height:50px;background:#4CAF50;color:white;border-radius:50%;z-index:2147483647;opacity:0.15;cursor:pointer;display:flex;justify-content:center;align-items:center;font-weight:bold;font-size:18px;';
            
            b.onclick = function() {
                if (isRunning) {
                    isRunning = false;
                    b.innerText = '▶';
                    b.style.background = '#4CAF50';
                    return;
                }
                isRunning = true;
                b.innerText = '⏹';
                b.style.background = '#f44336';
                b.style.opacity = '0.8';
                loop();
            };
            document.body.appendChild(b);
        }

        function loop() {
            if (!isRunning) return;

            var currentQ = document.body.innerText.substring(0, 200).trim();
            var txt = document.body.innerText.substring(0, 2000).replace(/\n+/g, ' ').trim();
            
            // ШУКАЄМО ВСІ КЛІКАБЕЛЬНІ БЛОКИ
            var opts = [];
            var els = [];
            
            document.querySelectorAll('div, span, label, button').forEach(function(el) {
                // Перевіряємо, чи елемент має текст і чи він не є частиною питання
                var t = el.innerText.trim();
                if (t.length > 5 && t.length < 200 && !t.includes('Запитання') && !t.includes('Почати') && !t.includes('Добіжи') && !t.includes('LIVE') && !t.includes('Далі') && !t.includes('Завершити')) {
                    // Перевіряємо, чи це блок, який можна натиснути (має обробник подій)
                    if (el.onclick || el.tagName === 'BUTTON' || el.tagName === 'LABEL' || el.getAttribute('role') === 'button') {
                        if (!opts.includes(t)) {
                            opts.push(t);
                            els.push(el);
                        }
                    }
                }
            });

            if (opts.length === 0) {
                // Якщо немає варіантів, шукаємо "Далі"
                var nxt = Array.from(document.querySelectorAll('button, div, a')).find(el => {
                    var t = el.innerText.trim().toLowerCase();
                    return (t === 'далі' || t === 'наступне' || t === 'завершити' || t === 'продовжити');
                });
                if (nxt) { tap(nxt); }
                setTimeout(loop, 2000);
                return;
            }

            var prompt = "Питання: " + txt + ". Варіанти: " + opts.join(' | ') + ". Дай номер правильної відповіді (1, 2, 3 або 4). Відповідай ТІЛЬКИ цифрою.";

            GM_xmlhttpRequest({
                method: "POST",
                url: "https://openrouter.ai/api/v1/chat/completions",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer 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"
                },
                data: JSON.stringify({
                    model: "openrouter/auto",
                    messages: [{ role: "user", content: prompt }]
                }),
                onload: function(res) {
                    try {
                        var data = JSON.parse(res.responseText);
                        if (data.error) {
                            alert("Помилка ШІ: " + data.error.message);
                            isRunning = false;
                            return;
                        }
                        
                        var ans = data.choices[0].message.content.trim();
                        var m = ans.match(/\d+/);
                        var idx = m ? parseInt(m[0]) - 1 : 0;

                        if (idx >= 0 && idx < els.length) {
                            tap(els[idx]);
                        } else {
                            tap(els[0]);
                        }
                        
                        setTimeout(function() {
                            var newQ = document.body.innerText.substring(0, 200).trim();
                            if (newQ !== currentQ) {
                                setTimeout(loop, 1000);
                            } else {
                                loop(); // Не вийшло, тиснемо ще раз
                            }
                        }, 1500);

                    } catch(e) {
                        setTimeout(loop, 2000);
                    }
                },
                onerror: function() {
                    setTimeout(loop, 2000);
                }
            });
        }

        start();
    })();
    """
    
    res = jsonify({"status": "ok", "script": code})
    res.headers["Content-Type"] = "application/json; charset=utf-8"
    return res, 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
