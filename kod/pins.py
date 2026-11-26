import subprocess, sys, os
F = "/mnt/user-data/uploads/Downloads/Listio-piny-nove/_frames/"
OUT = "/home/claude/listio/out"
os.makedirs(OUT, exist_ok=True)

THEMES = {
 "green": dict(bg="radial-gradient(ellipse at 50% 45%, #1f6b3f 0%, #0f3d24 70%)", fg="#fbf6ea", acc="#d9b768", pill="#d9b768", pillfg="#173d26"),
 "burg":  dict(bg="radial-gradient(ellipse at 50% 45%, #8a2b45 0%, #4a1020 75%)", fg="#fbf1ea", acc="#e3c07a", pill="#e3c07a", pillfg="#4a1020"),
 "pink":  dict(bg="radial-gradient(ellipse at 50% 45%, #fbe9ec 0%, #f2cfd6 80%)", fg="#6e2a3a", acc="#b4536b", pill="#b4536b", pillfg="#ffffff"),
}

def phone(img, w, x, y, rot=0, z=1, play=False, label=None, lc="#fff"):
    h = w * 2.04
    pb = ""
    if play:
        pb = f'<div class="play" style="width:{w*.34}px;height:{w*.34}px"><div class="tri" style="border-left-width:{w*.11}px;border-top-width:{w*.07}px;border-bottom-width:{w*.07}px"></div></div>'
    lab = f'<div class="lab" style="color:{lc}">{label}</div>' if label else ""
    return f'''<div class="ph" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);z-index:{z}">
      <div class="scr" style="background-image:url('file://{F}{img}.jpg')"></div><div class="notch"></div>{pb}</div>{lab and f'<div style="position:absolute;left:{x}px;top:{y+h+18}px;width:{w}px;z-index:5">{lab}</div>'}'''

def page(t, kicker, head, phones, sub, pill, extra=""):
    T = THEMES[t]
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
    @font-face{{font-family:Lora;src:url(file:///usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf)}}
    *{{margin:0;padding:0;box-sizing:border-box}}
    body{{width:1000px;height:1500px;overflow:hidden;background:{T['bg']};font-family:Lora,serif;color:{T['fg']};position:relative}}
    .k{{position:absolute;top:70px;width:100%;text-align:center;font:600 30px Poppins;letter-spacing:6px;color:{T['acc']}}}
    .h{{position:absolute;top:125px;left:50px;right:50px;text-align:center;font-weight:600;font-size:92px;line-height:1.08}}
    .ph{{position:absolute;background:#111;border-radius:52px;padding:13px;box-shadow:0 30px 60px rgba(0,0,0,.45)}}
    .scr{{width:100%;height:100%;border-radius:40px;background-size:cover;background-position:center}}
    .notch{{position:absolute;top:24px;left:50%;transform:translateX(-50%);width:28%;height:22px;background:#111;border-radius:12px}}
    .play{{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);border-radius:50%;background:rgba(255,255,255,.88);display:flex;align-items:center;justify-content:center;box-shadow:0 6px 20px rgba(0,0,0,.3)}}
    .tri{{width:0;height:0;border-style:solid;border-color:transparent transparent transparent {T['pillfg'] if t!='pink' else '#b4536b'};margin-left:8px}}
    .lab{{text-align:center;font:600 30px Poppins;letter-spacing:4px}}
    .sub{{position:absolute;bottom:190px;width:100%;text-align:center;font-size:50px;font-style:italic;font-weight:500}}
    .pill{{position:absolute;bottom:115px;left:50%;transform:translateX(-50%);background:{T['pill']};color:{T['pillfg']};font:600 30px Poppins;padding:16px 40px;border-radius:50px;white-space:nowrap}}
    .brand{{position:absolute;bottom:45px;width:100%;text-align:center;font:600 26px Poppins;letter-spacing:10px;color:{T['acc']}}}
    </style></head><body>
    <div class="k">{kicker}</div><div class="h">{head}</div>{phones}{extra}
    <div class="sub">{sub}</div><div class="pill">{pill}</div><div class="brand">LISTIO</div></body></html>'''

PINS = {
 "listio-new-smaragdova-1": page("green", "SMARAGDOVÁ SVATBA",
    "Pozvánka, kterou<br>hosté opravdu pustí",
    phone("g_title", 295, 60, 470, -8, 1) + phone("g_photo", 335, 332, 420, 0, 3, play=True) + phone("g_date", 295, 645, 470, 8, 1),
    "Video pozvánka s hudbou a fotkou", "Šablona v Canvě · pošlete přes WhatsApp"),
 "listio-new-vinova-bilingual-1": page("burg", "ČESKY &amp; ENGLISH",
    "Jedna pozvánka,<br>dva jazyky",
    phone("b_cz", 330, 125, 400, -5, 2, label="ČESKY", lc="#e3c07a") + phone("b_en", 330, 545, 400, 5, 2, label="ENGLISH", lc="#e3c07a"),
    "Pro hosty z Česka i ze zahraničí", "Šablona v Canvě · pošlete přes WhatsApp"),
 "listio-new-ruzova-bilingual-1": page("pink", "HOTOVO ZA PÁR MINUT",
    "Pozvánka do mobilu<br>bez tisku a pošty",
    phone("p_ph2", 360, 95, 420, -4, 2, play=True) + phone("p_date", 330, 565, 480, 5, 1),
    "Růžová video pozvánka česky i anglicky", "Šablona v Canvě · pošlete přes WhatsApp",
    extra='<div style="position:absolute;left:500px;top:410px;z-index:6;background:#fff;color:#2b2b2b;font:500 28px Poppins;padding:18px 26px;border-radius:26px 26px 26px 6px;box-shadow:0 10px 25px rgba(0,0,0,.18)">Pozvánka odeslána ✓✓</div>'),
}

for name, html in PINS.items():
    p = f"{OUT}/{name}.html"; open(p, "w", encoding="utf-8").write(html)
    png = f"{OUT}/{name}.png"
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                    "--window-size=1000,1500", f"--screenshot={png}", f"file://{p}"], capture_output=True, timeout=60)
    from PIL import Image
    Image.open(png).convert("RGB").save(f"{OUT}/{name}.jpg", quality=90)
    print(name)
