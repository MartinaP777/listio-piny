"""Listio Pinterest piny 1000x1500 – generator (Lora + Poppins, mobily se snimky z videi)."""
import subprocess, os, csv
from PIL import Image
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = REPO + "/zdroje/frames/"   # snimky obrazovek pozvanek z videi
D = REPO + "/zdroje/"          # fotky planovace a rozlucky
OUT = REPO + "/out"            # vystup (negituje se); os.makedirs(OUT, exist_ok=True)

TH = {
 "green": dict(bg="radial-gradient(ellipse at 50% 45%, #1f6b3f 0%, #0f3d24 70%)", fg="#fbf6ea", acc="#d9b768", pill="#d9b768", pillfg="#173d26"),
 "burg":  dict(bg="radial-gradient(ellipse at 50% 45%, #8a2b45 0%, #4a1020 75%)", fg="#fbf1ea", acc="#e3c07a", pill="#e3c07a", pillfg="#4a1020"),
 "pink":  dict(bg="radial-gradient(ellipse at 50% 45%, #fbe9ec 0%, #f2cfd6 80%)", fg="#6e2a3a", acc="#b4536b", pill="#b4536b", pillfg="#ffffff"),
 "navy":  dict(bg="radial-gradient(ellipse at 50% 45%, #1d3a66 0%, #0b1a33 75%)", fg="#f4f1ea", acc="#d6b36c", pill="#d6b36c", pillfg="#0b1a33"),
 "cream": dict(bg="radial-gradient(ellipse at 50% 40%, #fbf5ee 0%, #efe2d6 85%)", fg="#5e2b36", acc="#9a5a68", pill="#8c3f52", pillfg="#ffffff"),
}

def phone(img, w, x, y, rot=0, z=1, play=False, label=None, lc="#fff", playcol="#333"):
    h = w * 2.04
    pb = (f'<div class="play" style="width:{w*.34}px;height:{w*.34}px"><div class="tri" style="border-left:{w*.11}px solid {playcol};'
          f'border-top:{w*.07}px solid transparent;border-bottom:{w*.07}px solid transparent"></div></div>') if play else ""
    lab = (f'<div style="position:absolute;left:{x}px;top:{y+h+16}px;width:{w}px;z-index:5;text-align:center;font:600 30px Poppins;'
           f'letter-spacing:4px;color:{lc}">{label}</div>') if label else ""
    return (f'<div class="ph" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);z-index:{z}">'
            f'<div class="scr" style="background-image:url(\'file://{F}{img}.jpg\')"></div><div class="notch"></div>{pb}</div>{lab}')

def card(path, x, y, w, h, rot=0, pos="center"):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);border-radius:28px;'
            f'background:url(\'file://{path}\') {pos}/cover;box-shadow:0 25px 55px rgba(0,0,0,.25);border:10px solid #fff"></div>')

def bubble(text, x, y):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;z-index:6;background:#fff;color:#2b2b2b;font:500 28px Poppins;'
            f'padding:18px 26px;border-radius:26px 26px 26px 6px;box-shadow:0 10px 25px rgba(0,0,0,.18)">{text}</div>')

def page(t, kicker, head, body, sub, pill, hsize=92):
    T = TH[t]
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
    @font-face{{font-family:Lora;src:url(file:///usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf)}}
    @font-face{{font-family:Lora;font-style:italic;src:url(file:///usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf)}}
    *{{margin:0;padding:0;box-sizing:border-box}}
    body{{width:1000px;height:1500px;overflow:hidden;background:{T['bg']};font-family:Lora,serif;color:{T['fg']};position:relative}}
    .k{{position:absolute;top:70px;width:100%;text-align:center;font:600 30px Poppins;letter-spacing:6px;color:{T['acc']}}}
    .h{{position:absolute;top:125px;left:40px;right:40px;text-align:center;font-weight:600;font-size:{hsize}px;line-height:1.08}}
    .ph{{position:absolute;background:#111;border-radius:52px;padding:13px;box-shadow:0 30px 60px rgba(0,0,0,.45)}}
    .scr{{width:100%;height:100%;border-radius:40px;background-size:cover;background-position:center}}
    .notch{{position:absolute;top:24px;left:50%;transform:translateX(-50%);width:28%;height:22px;background:#111;border-radius:12px}}
    .play{{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);border-radius:50%;background:rgba(255,255,255,.9);display:flex;align-items:center;justify-content:center;box-shadow:0 6px 20px rgba(0,0,0,.3)}}
    .tri{{width:0;height:0;margin-left:8px}}
    .sub{{position:absolute;bottom:232px;width:100%;text-align:center;font-size:50px;font-style:italic;font-weight:500}}
    .pill{{position:absolute;bottom:118px;left:50%;transform:translateX(-50%);background:{T['pill']};color:{T['pillfg']};font:600 30px Poppins;padding:16px 40px;border-radius:50px;white-space:nowrap}}
    .brand{{position:absolute;bottom:45px;width:100%;text-align:center;font:600 26px Poppins;letter-spacing:10px;color:{T['acc']}}}
    </style></head><body><div class="k">{kicker}</div><div class="h">{head}</div>{body}
    <div class="sub">{sub}</div><div class="pill">{pill}</div><div class="brand">LISTIO</div></body></html>'''

CZP = "Šablona v Canvě · pošlete přes WhatsApp"
ENP = "Canva template · send via WhatsApp"
PC = {"green": "#173d26", "burg": "#6b1a30", "pink": "#b4536b", "navy": "#0b1a33"}

def three(a, b, c, t):  # 3 mobily, prostredni s play
    return phone(a, 295, 60, 470, -8, 1) + phone(b, 335, 332, 420, 0, 3, play=True, playcol=PC[t]) + phone(c, 295, 645, 470, 8, 1)
def two(a, b, la, lb, t):
    return phone(a, 330, 125, 400, -5, 2, label=la, lc=TH[t]['acc']) + phone(b, 330, 545, 400, 5, 2, label=lb, lc=TH[t]['acc'])
def pair(a, b, t, bub):
    return phone(a, 360, 95, 420, -4, 2, play=True, playcol=PC[t]) + phone(b, 330, 565, 480, 5, 1) + bubble(bub, 500, 410)
def single(a, t, items):
    li = "".join(f'<div style="margin:0 0 34px;font:600 40px Poppins">✓ {i}</div>' for i in items)
    return phone(a, 360, 560, 400, 4, 2, play=True, playcol=PC[t]) + f'<div style="position:absolute;left:60px;top:540px;width:500px;color:{TH[t]["fg"]}">{li}</div>'

# (soubor, datum, cas, nastenka, listing, slug, n, title, desc, keywords, html)
P = []
def add(*a): P.append(a)

add("listio-planovac-vanoce", "2026-12-06", "09:30", "Plánování svatby", "4456042662", "planovac", 1,
    "Svatební plánovač PDF – zasnoubení o Vánocích? Začněte tady",
    "Svatební plánovač PDF česky pro čerstvě zasnoubené. Checklist na 12 měsíců, rozpočet svatby, seznam hostů i zasedací pořádek – k tisku i do tabletu. Zasnoubili jste se o Vánocích? 💍 Stáhněte si plánovač na Etsy a začněte plánovat ještě dnes.",
    "svatební plánovač, plánování svatby, svatební checklist, rozpočet svatby, zasnoubení",
    page("cream", "SVATEBNÍ PLÁNOVAČ PDF", "Zasnoubili jste se<br><i>o Vánocích?</i>",
         card(D + "Listio-planovac-foto.jpg", 150, 430, 700, 700, -2), "Plán na 12 měsíců krok za krokem", "Česky · k tisku i do tabletu"))
add("listio-smaragdova-pusti", "2026-12-06", "13:30", "Svatební video pozvánka", "4516268309", "smaragd", 1,
    "Svatební video pozvánka smaragdově zelená – pozvánka do mobilu",
    "Svatební video pozvánka ve smaragdově zelené – hosté ji dostanou do mobilu přes WhatsApp. S hudbou a vaší fotkou, úprava v Canvě za pár minut, bez tisku a poštovného. 💚 Stáhněte si šablonu na Etsy a pošlete pozvánku ještě dnes.",
    "svatební video pozvánka, svatební oznámení, pozvánka do mobilu, zelená svatba, svatba 2027",
    page("green", "SMARAGDOVÁ SVATBA", "Pozvánka, kterou<br>hosté opravdu pustí", three("g_title", "g_photo", "g_date", "green"),
         "Video pozvánka s hudbou a fotkou", CZP))
add("listio-rozlucka-kviz", "2026-12-06", "20:30", "Rozlučka se svobodou", "4465904365", "rozlucka", 1,
    "Hry na rozlučku se svobodou – kvíz pro nevěstu a deníček PDF",
    "Hry na rozlučku se svobodou, u kterých se nasmějete: kvíz Jak dobře nevěsta zná ženicha a nevěstin rozlučkový deníček. PDF k tisku, hotové za pár minut. 🥂 Stáhněte si hry na Etsy a rozlučka je připravená.",
    "rozlučka se svobodou, hry na rozlučku, kvíz pro nevěstu, rozlučka nevěsty, družičky",
    page("pink", "ROZLUČKA SE SVOBODOU", "Zná nevěsta opravdu<br><i>svého ženicha?</i>",
         card(D + "Listio-rozlucka-foto.jpg", 80, 440, 840, 700, 2), "Kvíz a další hry pro družičky", "PDF k tisku · hotovo za pár minut", hsize=86))
add("listio-vinova-dva-jazyky", "2026-12-07", "09:30", "Svatební video pozvánka", "4612705891", "burgundy-bil", 1,
    "Svatební video pozvánka česky i anglicky – vínová, Canva",
    "Dvojjazyčná svatební video pozvánka česky i anglicky ve vínové barvě – ideální, když máte hosty ze zahraničí. Úprava v Canvě, odeslání přes WhatsApp. 🍷 Stáhněte si šablonu na Etsy a pozvěte všechny hosty najednou.",
    "svatební video pozvánka, dvojjazyčná pozvánka, vínová svatba, svatební oznámení, svatba 2027",
    page("burg", "ČESKY &amp; ENGLISH", "Jedna pozvánka,<br>dva jazyky", two("b_cz", "b_en", "ČESKY", "ENGLISH", "burg"),
         "Pro hosty z Česka i ze zahraničí", CZP))
add("listio-namornicka-zima", "2026-12-07", "13:30", "Plánování svatby", "4516244917", "namornicka", 1,
    "Zimní svatební video pozvánka – námořnická modrá a zlatá",
    "Zimní svatba? Svatební video pozvánka v námořnické modré se zlatou působí elegantně a slavnostně. S hudbou a fotkou, úprava v Canvě, odeslání do mobilu přes WhatsApp. 💙 Stáhněte si šablonu na Etsy a pozvěte hosty ještě dnes.",
    "zimní svatba, svatební video pozvánka, modrá svatba, svatební oznámení, pozvánka do mobilu",
    page("navy", "ZIMNÍ SVATBA", "Elegantní jako<br>zimní večer", three("n_title", "n_photo", "n_date", "navy"),
         "Modrozlatá video pozvánka", CZP))
add("listio-ruzova-odeslano", "2026-12-07", "20:30", "Růžová svatba inspirace", "4610369897", "pink-bil", 1,
    "Svatební video pozvánka do mobilu – růžová, bez tisku a pošty",
    "Růžová svatební video pozvánka česky i anglicky – pošlete ji hostům do mobilu za pár minut, bez tisku a poštovného. Úprava jmen, data a fotky v Canvě. 🌸 Stáhněte si šablonu na Etsy a pozvánka může letět ještě dnes.",
    "svatební video pozvánka, růžová svatba, pozvánka do mobilu, svatební oznámení, digitální pozvánka",
    page("pink", "HOTOVO ZA PÁR MINUT", "Pozvánka do mobilu<br>bez tisku a pošty", pair("p_ph2", "p_date", "pink", "Pozvánka odeslána ✓✓"),
         "Růžová video pozvánka česky i anglicky", CZP))
add("listio-planovac-checklist", "2026-12-08", "09:30", "Plánování svatby", "4456042662", "planovac", 2,
    "Svatební checklist na 12 měsíců – plánovač svatby PDF česky",
    "Svatební checklist na 12 měsíců krok za krokem: co zařídit rok, půl roku i týden před svatbou. Součástí plánovače je rozpočet, seznam hostů a zasedací pořádek. ✅ Stáhněte si svatební plánovač na Etsy a nic nezapomenete.",
    "svatební checklist, plánování svatby, svatební plánovač, příprava svatby, svatba 2027",
    page("cream", "SVATEBNÍ CHECKLIST", "Na nic<br><i>nezapomenete</i>",
         card(D + "Listio-planovac-foto.jpg", 150, 430, 700, 700, 2, "center 60%"), "Od 12 měsíců předem po svatební ráno", "Svatební plánovač PDF · česky"))
add("listio-en-burgundy-watch", "2026-12-08", "13:30", "Wedding Video Invitations", "4516370312", "burgundy-en", 1,
    "Burgundy Wedding Video Invitation – Animated Canva Template",
    "Burgundy and gold wedding video invitation your guests will actually watch. Add your photo, music and details in Canva and send it by WhatsApp or text – no printing, no postage. 🍷 Download the template on Etsy today.",
    "wedding video invitation, burgundy wedding, animated wedding invitation, canva wedding invitation, digital invitation",
    page("burg", "VIDEO WEDDING INVITATION", "Your guests will<br><i>actually watch it</i>", three("b_en", "be_photo", "be_date", "burg"),
         "Burgundy &amp; gold, with music and photo", ENP))
add("listio-vinova-podzim", "2026-12-08", "20:30", "Svatební video pozvánka", "4516360870", "vinova", 1,
    "Svatební video pozvánka vínová a zlatá – animovaná pozvánka do mobilu",
    "Vínová svatební video pozvánka se zlatým písmem pro podzimní i zimní svatbu. S hudbou a vaší fotkou, úprava v Canvě za pár minut, odeslání přes WhatsApp. 🍷 Stáhněte si šablonu na Etsy a pozvěte hosty ještě dnes.",
    "svatební video pozvánka, vínová svatba, zimní svatba, svatební oznámení, pozvánka whatsapp",
    page("burg", "VÍNOVÁ SVATBA", "Slavnostní pozvánka<br>přímo do mobilu", single("b_cz", "burg", ["vaše fotka a hudba", "harmonogram dne", "potvrzení účasti", "vše upravíte v Canvě"]),
         "Vínová video pozvánka se zlatou", CZP))
add("listio-smaragdova-info", "2026-12-09", "09:30", "Plánování svatby", "4516268309", "smaragd", 2,
    "Svatební video pozvánka s harmonogramem a RSVP – smaragdová",
    "Svatební video pozvánka, ve které hosté najdou vše: harmonogram dne, ubytování, dress code i potvrzení účasti. Smaragdově zelená, úprava v Canvě, odeslání do mobilu. 💚 Stáhněte si šablonu na Etsy a ušetřete hostům otázky.",
    "svatební video pozvánka, harmonogram svatby, potvrzení účasti, zelená svatba, svatební oznámení",
    page("green", "9 ANIMOVANÝCH STRAN", "Vše, co hosté<br>potřebují vědět", three("g_harm", "g_info", "g_rsvp", "green"),
         "Harmonogram, informace i RSVP", CZP))
add("listio-en-pink-invite", "2026-12-09", "13:30", "Wedding Video Invitations", "4610369897", "pink-bil-en", 1,
    "Pink Wedding Video Invitation – Send to Guests by WhatsApp",
    "Pink wedding video invitation in English and Czech – send it straight to your guests' phones in minutes. Edit names, date and photo in Canva. No printing, no postage. 🌸 Download the template on Etsy today.",
    "wedding video invitation, pink wedding, digital wedding invite, canva wedding invitation, whatsapp invitation",
    page("pink", "DIGITAL WEDDING INVITATION", "Invite your guests<br><i>in minutes</i>", pair("p_en", "pe_date", "pink", "Invitation sent ✓✓"),
         "Pink video invitation with music", ENP))
add("listio-rozlucka-hry", "2026-12-09", "20:30", "Rozlučka se svobodou", "4465904365", "rozlucka", 2,
    "Kvíz pro nevěstu na rozlučku – jak dobře zná svého ženicha?",
    "Kvíz pro nevěstu na rozlučku se svobodou: kolik otázek o ženichovi zodpoví správně? Plus další hry a rozlučkový deníček v jednom PDF k tisku. 😄 Stáhněte si hry na Etsy a zábava je zajištěná.",
    "kvíz pro nevěstu, rozlučka se svobodou, hry na rozlučku, rozlučka nevěsty, svatba 2027",
    page("pink", "HRY NA ROZLUČKU", "Rozlučka, na kterou<br><i>se nezapomíná</i>",
         card(D + "Listio-rozlucka-foto.jpg", 80, 440, 840, 700, -2, "60% center"), "Nevěstin rozlučkový deníček", "PDF k tisku · hotovo za pár minut", hsize=86))
add("listio-namornicka-rsvp", "2026-12-10", "09:30", "Svatební video pozvánka", "4516244917", "namornicka", 2,
    "Svatební video pozvánka s potvrzením účasti – modrá a zlatá",
    "Svatební video pozvánka s harmonogramem a potvrzením účasti přímo v pozvánce. Námořnická modrá se zlatou, úprava v Canvě, odeslání do mobilu přes WhatsApp. 💙 Stáhněte si šablonu na Etsy a mějte přehled o hostech.",
    "potvrzení účasti, svatební video pozvánka, harmonogram svatby, modrá svatba, svatební oznámení",
    page("navy", "RSVP V POZVÁNCE", "Hosté potvrdí účast<br>přímo v mobilu", three("n_harm", "n_photo", "n_rsvp", "navy"),
         "Harmonogram, fotka i RSVP", CZP, hsize=86))
add("listio-vinova-rsvp", "2026-12-10", "13:30", "Svatební video pozvánka", "4612705891", "burgundy-bil", 2,
    "Dvojjazyčná svatební pozvánka s harmonogramem – česky i anglicky",
    "Svatební video pozvánka česky i anglicky: harmonogram, informace pro hosty a potvrzení účasti v obou jazycích. Vínová se zlatou, úprava v Canvě. 🍷 Stáhněte si šablonu na Etsy a pozvěte hosty z Česka i ze zahraničí.",
    "dvojjazyčná pozvánka, svatební video pozvánka, harmonogram svatby, vínová svatba, svatba 2027",
    page("burg", "ČESKY &amp; ENGLISH", "Harmonogram<br>v obou jazycích", two("b_harm", "be_harm", "ČESKY", "ENGLISH", "burg"),
         "Pro hosty z Česka i ze zahraničí", CZP))
add("listio-planovac-rozpocet", "2026-12-10", "20:30", "Plánování svatby", "4456042662", "planovac", 3,
    "Rozpočet svatby a seznam hostů – svatební plánovač PDF",
    "Kolik stojí svatba? Svatební plánovač PDF vám pomůže hlídat rozpočet, sestavit seznam hostů a zasedací pořádek. Česky, k tisku i do tabletu. 💍 Stáhněte si plánovač na Etsy a mějte svatbu pod kontrolou.",
    "rozpočet svatby, seznam hostů, svatební plánovač, zasedací pořádek, plánování svatby",
    page("cream", "SVATEBNÍ PLÁNOVAČ PDF", "Kolik stojí<br><i>svatba?</i>",
         card(D + "Listio-planovac-foto.jpg", 150, 430, 700, 700, -2, "center 40%"), "Rozpočet, hosté i zasedací pořádek", "Česky · k tisku i do tabletu"))
add("listio-smaragdova-zahrada", "2026-12-11", "09:30", "Svatební video pozvánka", "4516268309", "smaragd", 3,
    "Zelená svatební video pozvánka s fotkou – šablona Canva",
    "Zelená svatební video pozvánka s vaší fotkou a hudbou – elegantní jako letní zahrada. Hotová v Canvě za pár minut, hosté ji otevřou v mobilu. 💚 Stáhněte si šablonu na Etsy a pošlete pozvánku ještě dnes.",
    "svatební video pozvánka, zelená svatba, svatební oznámení, pozvánka s fotkou, šablona canva",
    page("green", "SVATBA V ZELENÉ", "Vaše fotka,<br>vaše hudba", single("g_photo", "green", ["vaše fotka a hudba", "harmonogram dne", "potvrzení účasti", "vše upravíte v Canvě"]),
         "Smaragdová video pozvánka", CZP))
add("listio-en-burgundy-rsvp", "2026-12-11", "13:30", "Wedding Video Invitations", "4516370312", "burgundy-en", 2,
    "Wedding Video Invitation with RSVP and Timeline – Burgundy",
    "Animated wedding video invitation with timeline and RSVP page included. Burgundy and gold, edit everything in Canva and send to guests by WhatsApp or text. 🍷 Download the template on Etsy and invite your guests today.",
    "wedding video invitation, rsvp invitation, wedding timeline, burgundy wedding, canva template",
    page("burg", "RSVP INCLUDED", "Everything guests<br><i>need to know</i>", three("be_harm", "be_photo", "be_rsvp", "burg"),
         "Timeline, photo and RSVP", ENP))
add("listio-ruzova-jaro", "2026-12-11", "20:30", "Růžová svatba inspirace", "4610369897", "pink-bil", 2,
    "Jarní svatba 2027 – růžová svatební video pozvánka česky i anglicky",
    "Plánujete jarní svatbu 2027? Růžová svatební video pozvánka s hudbou a fotkou, česky i anglicky. Úprava v Canvě, odeslání do mobilu přes WhatsApp. 🌸 Stáhněte si šablonu na Etsy a pozvěte hosty ještě dnes.",
    "jarní svatba, růžová svatba, svatební video pozvánka, svatba 2027, svatební oznámení",
    page("pink", "JARO 2027", "Jarní svatba?<br>Pozvánka, která kvete", three("p_photo", "p_ph2", "p_rsvp", "pink"),
         "Růžová video pozvánka česky i anglicky", CZP, hsize=84))

UTC = {"09:30": "08:30", "13:30": "12:30", "20:30": "19:30"}
RAW = "https://raw.githubusercontent.com/MartinaP777/listio-piny/main/piny/"
rows = []
for (fn, d, t, board, lid, slug, n, title, desc, kw, html) in P:
    assert len(title) <= 100 and len(desc) <= 500, fn
    hp = f"{OUT}/{fn}.html"; open(hp, "w", encoding="utf-8").write(html)
    png = f"{OUT}/{fn}.png"
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                    "--window-size=1000,1500", f"--screenshot={png}", f"file://{hp}"], capture_output=True, timeout=60)
    Image.open(png).convert("RGB").save(f"{OUT}/{fn}.jpg", quality=90); os.remove(png)
    rows.append({"Title": title, "Media URL": RAW + fn + ".jpg", "Pinterest board": board, "Thumbnail": "", "Description": desc,
                 "Link": f"https://listio.etsy.com/listing/{lid}?utm_source=pinterest&utm_medium=social&utm_content={slug}-pin{n}",
                 "Publish date": f"{d}T{UTC[t]}:00", "Keywords": kw})
with open(f"{OUT}/listio_piny_6-11-12.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
ims = [Image.open(f"{OUT}/{p[0]}.jpg").resize((250, 375)) for p in P]
s = Image.new("RGB", (6 * 250, 3 * 375), "white")
for i, im in enumerate(ims): s.paste(im, ((i % 6) * 250, (i // 6) * 375))
s.save(f"{OUT}/kolaz.jpg", quality=85)
print(len(P))
