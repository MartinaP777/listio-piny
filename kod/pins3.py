"""Listio piny 12.–20. 12. 2026 – generator (stejne funkce jako pins2.py + cardlist)."""
import subprocess, os, csv
from PIL import Image
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = REPO + "/zdroje/frames/"   # snimky obrazovek pozvanek z videi
D = REPO + "/zdroje/"          # fotky planovace a rozlucky
OUT = REPO + "/out"; os.makedirs(OUT, exist_ok=True)  # vystup (neni v gitu)

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

def cardlist(path, t, items, rot=-3, pos="center"):  # fotka vlevo + seznam vpravo (planovac)
    li = "".join(f'<div style="margin:0 0 34px;font:600 38px Poppins">✓ {i}</div>' for i in items)
    return card(path, 55, 450, 470, 640, rot, pos) + f'<div style="position:absolute;left:575px;top:560px;width:400px;color:{TH[t]["fg"]}">{li}</div>'

# (soubor, datum, cas, nastenka, listing, slug, n, title, desc, keywords, html)
P = []
def add(*a): P.append(a)
PL = D + "Listio-planovac-foto.jpg"; RZ = D + "Listio-rozlucka-foto.jpg"
PLC = "Česky · k tisku i do tabletu"; RZP = "PDF k tisku · hotovo za pár minut"
SVP, PLS, MIN, RUZ, WVI, ROZ = "Svatební video pozvánka", "Plánování svatby", "Minimalistický styl", "Růžová svatba inspirace", "Wedding Video Invitations", "Rozlučka se svobodou"
G, BB, V, BE, N, PB, PE, PN, R = "4516268309", "4612705891", "4516360870", "4516370312", "4516244917", "4610369897", "4610369897", "4456042662", "4465904365"
IT = ["vaše fotka a hudba", "harmonogram dne", "potvrzení účasti", "vše upravíte v Canvě"]

# --- 12. 12.
add("listio-planovac-darek", "2026-12-12", "09:30", PLS, PN, "planovac", 4,
    "Svatební plánovač PDF – dárek pro snoubence pod stromeček",
    "Svatební plánovač PDF jako dárek pod stromeček pro čerstvě zasnoubené. Checklist na 12 měsíců, rozpočet svatby, seznam hostů a zasedací pořádek – česky, k tisku i do tabletu. 🎁 Stáhněte si plánovač na Etsy, máte ho hned.",
    "svatební plánovač, dárek pro snoubence, plánování svatby, zasnoubení, svatba 2027",
    page("cream", "DÁREK PRO SNOUBENCE", "Dárek pod<br><i>stromeček</i>",
         cardlist(PL, "cream", ["checklist na 12 měsíců", "rozpočet svatby", "seznam hostů", "zasedací pořádek"]), "Svatební plánovač PDF česky", "Stáhnete hned · k tisku i do tabletu"))
add("listio-smaragdova-datum", "2026-12-12", "13:30", SVP, G, "smaragd", 4,
    "Svatební video pozvánka 2027 – smaragdová, pošlete přes WhatsApp",
    "Svatební video pozvánka na svatbu 2027 ve smaragdově zelené. Hosté si datum uloží rovnou do mobilu – s hudbou, vaší fotkou a potvrzením účasti. Úprava v Canvě za pár minut. 💚 Stáhněte si šablonu na Etsy a pošlete pozvánku ještě dnes.",
    "svatební video pozvánka, svatba 2027, pozvánka do mobilu, zelená svatba, svatební oznámení",
    page("green", "SVATBA 2027", "Uložte si datum<br><i>do mobilu</i>", pair("g_date", "g_photo", "green", "Pozvánka odeslána ✓✓"),
         "Smaragdová video pozvánka s hudbou", CZP))
add("listio-en-burgundy-nopost", "2026-12-12", "20:30", WVI, BE, "burgundy-en", 3,
    "Burgundy Wedding Video Invitation – No Printing, No Postage",
    "Burgundy and gold wedding video invitation you send straight to your guests' phones. No printing, no postage – just edit names, date and photo in Canva and share by WhatsApp or text. 🍷 Download the template on Etsy today.",
    "wedding video invitation, burgundy wedding, digital wedding invitation, canva wedding invitation, save the date",
    page("burg", "SAVE THE DATE 2027", "No printing,<br><i>no postage</i>", pair("b_en", "be_date", "burg", "Invitation sent ✓✓"),
         "Burgundy &amp; gold video invitation", ENP))
# --- 13. 12.
add("listio-namornicka-zlata", "2026-12-13", "09:30", SVP, N, "namornicka", 3,
    "Svatební video pozvánka modrá se zlatou – šablona Canva",
    "Svatební video pozvánka v námořnické modré se zlatým písmem – elegantní volba pro zimní i večerní svatbu. Fotka, hudba, harmonogram i potvrzení účasti, úprava v Canvě. 💙 Stáhněte si šablonu na Etsy a pošlete ji hostům do mobilu.",
    "svatební video pozvánka, modrá svatba, šablona canva, svatební oznámení, zimní svatba",
    page("navy", "NÁMOŘNICKÁ &amp; ZLATÁ", "Pozvánka,<br><i>která zazáří</i>", single("n_title", "navy", IT),
         "Modrozlatá video pozvánka", CZP))
add("listio-ruzova-tanec", "2026-12-13", "13:30", RUZ, PB, "pink-bil", 3,
    "Růžová svatební video pozvánka – česky i anglicky, Canva",
    "Něžná růžová svatební video pozvánka s květinami, česky i anglicky. Vaše fotka, hudba a všechny informace pro hosty – upravíte v Canvě a pošlete do mobilu přes WhatsApp. 🌸 Stáhněte si šablonu na Etsy.",
    "růžová svatba, svatební video pozvánka, dvojjazyčná pozvánka, svatební oznámení, šablona canva",
    page("pink", "RŮŽOVÁ SVATBA", "Něžná jako<br><i>první tanec</i>", three("p_photo", "p_ph2", "p_date", "pink"),
         "Video pozvánka česky i anglicky", CZP))
add("listio-vinova-zima", "2026-12-13", "20:30", SVP, V, "vinova", 2,
    "Svatební video pozvánka na zimní svatbu – vínová a zlatá",
    "Svatební video pozvánka na zimní svatbu ve vínové barvě se zlatým písmem. S hudbou, vaší fotkou a harmonogramem dne – úprava v Canvě za pár minut, odeslání přes WhatsApp. 🍷 Stáhněte si šablonu na Etsy a pozvěte hosty ještě dnes.",
    "zimní svatba, svatební video pozvánka, vínová svatba, pozvánka do mobilu, svatba 2027",
    page("burg", "SVATBA V ZIMĚ", "Vínová a zlatá<br><i>na zimní svatbu</i>", three("b_cz", "b_photo", "b_date", "burg"),
         "Animovaná pozvánka s hudbou", CZP, hsize=86))
# --- 14. 12.
add("listio-planovac-prvni-kroky", "2026-12-14", "09:30", PLS, PN, "planovac", 5,
    "Plánování svatby – co zařídit jako první po zasnoubení",
    "Plánování svatby krok za krokem: co zařídit jako první po zasnoubení, co půl roku předem a co týden před svatbou. Svatební plánovač PDF česky s checklistem, rozpočtem a seznamem hostů. 💍 Stáhněte si ho na Etsy a začněte v klidu.",
    "plánování svatby, zasnoubení, svatební checklist, svatební plánovač, příprava svatby",
    page("cream", "PRÁVĚ ZASNOUBENÍ?", "Co zařídit<br><i>jako první?</i>", card(PL, 150, 430, 700, 700, 3, "center 55%"),
         "Checklist od zásnub po svatbu", PLC))
add("listio-vinova-zahranici", "2026-12-14", "13:30", SVP, BB, "burgundy-bil", 3,
    "Dvojjazyčná svatební video pozvánka – hosté ze zahraničí",
    "Máte hosty ze zahraničí? Dvojjazyčná svatební video pozvánka česky i anglicky ve vínové a zlaté – všichni dostanou stejně krásnou pozvánku do mobilu. Úprava v Canvě. 🍷 Stáhněte si šablonu na Etsy.",
    "dvojjazyčná pozvánka, svatební video pozvánka, mezinárodní svatba, vínová svatba, svatební oznámení",
    page("burg", "ČESKY &amp; ENGLISH", "Hosté ze<br><i>zahraničí?</i>", two("b_date", "be_date", "ČESKY", "ENGLISH", "burg"),
         "Jedna pozvánka ve dvou jazycích", CZP))
add("listio-rozlucka-druzicky", "2026-12-14", "20:30", ROZ, R, "rozlucka", 3,
    "Hry na rozlučku se svobodou – PDF k tisku pro družičky",
    "Hry na rozlučku se svobodou pro družičky: kvíz o ženichovi, úkoly pro nevěstu a rozlučkový deníček. PDF k tisku, připravené za pár minut. 🥂 Stáhněte si hry na Etsy a rozlučka bude stát za to.",
    "hry na rozlučku, rozlučka se svobodou, družičky, kvíz pro nevěstu, rozlučka nevěsty",
    page("pink", "ROZLUČKA SE SVOBODOU", "Družičky,<br><i>tohle je pro vás</i>", card(RZ, 80, 440, 840, 700, -2),
         "Hry a kvíz na rozlučku", RZP, hsize=86))
# --- 15. 12.
add("listio-smaragdova-bez-papiru", "2026-12-15", "09:30", MIN, G, "smaragd", 5,
    "Svatební video pozvánka bez tisku – zelená, minimalistická",
    "Svatební video pozvánka bez tisku a papíru – minimalistická, zelená a elegantní. Hosté ji dostanou do mobilu i s harmonogramem a potvrzením účasti. Úprava v Canvě za pár minut. 💚 Stáhněte si šablonu na Etsy.",
    "svatební video pozvánka, minimalistická svatba, digitální pozvánka, zelená svatba, ekologická svatba",
    page("green", "MINIMALISTICKÝ STYL", "Méně papíru,<br><i>víc radosti</i>", three("g_harm", "g_title", "g_rsvp", "green"),
         "Pozvánka rovnou do mobilu", CZP))
add("listio-en-burgundy-music", "2026-12-15", "13:30", WVI, BE, "burgundy-en", 4,
    "Animated Wedding Invitation with Music – Burgundy Canva Template",
    "Animated wedding video invitation with your own music and photo, timeline and RSVP page. Burgundy and gold, easy to edit in Canva and send by WhatsApp or text. 🍷 Download the template on Etsy and invite your guests today.",
    "animated wedding invitation, wedding video invitation, burgundy wedding, canva template, rsvp invitation",
    page("burg", "ANIMATED INVITATION", "Wedding invite<br><i>with music</i>", single("be_photo", "burg", ["your photo &amp; music", "wedding timeline", "RSVP page", "edit in Canva"]),
         "Burgundy &amp; gold", ENP))
add("listio-en-pink-spring", "2026-12-15", "20:30", WVI, PE, "pink-bil-en", 2,
    "Pink Floral Wedding Video Invitation – Spring Wedding 2027",
    "Pink floral wedding video invitation for your spring wedding 2027 – in English and Czech. Add your photo, music and details in Canva and send it to guests' phones in minutes. 🌸 Download the template on Etsy today.",
    "pink wedding invitation, floral wedding invitation, wedding video invitation, spring wedding, canva template",
    page("pink", "SPRING WEDDING 2027", "Soft pink<br><i>&amp; romantic</i>", three("p_en", "pe_photo", "pe_date", "pink"),
         "Floral video invitation with music", ENP))
# --- 16. 12.
add("listio-planovac-hoste", "2026-12-16", "09:30", PLS, PN, "planovac", 6,
    "Zasedací pořádek a seznam hostů – svatební plánovač PDF",
    "Zasedací pořádek a seznam hostů bez chaosu: svatební plánovač PDF česky vám pomůže hlídat potvrzení účasti, menu i rozesazení stolů. K tisku i do tabletu. 💍 Stáhněte si plánovač na Etsy.",
    "zasedací pořádek, seznam hostů, svatební plánovač, plánování svatby, svatba 2027",
    page("cream", "SEZNAM HOSTŮ", "Kdo bude<br><i>sedět s kým?</i>",
         cardlist(PL, "cream", ["seznam hostů", "potvrzení účasti", "zasedací pořádek", "menu a dárky"], 3, "center 35%"), "Hosté a stoly pod kontrolou", PLC))
add("listio-namornicka-minimal", "2026-12-16", "13:30", MIN, N, "namornicka", 4,
    "Elegantní svatební video pozvánka – minimalistická, modrá",
    "Elegantní minimalistická svatební video pozvánka v tmavě modré se zlatou. Čisté písmo, vaše fotka a všechny informace pro hosty – upravíte v Canvě, pošlete do mobilu. 💙 Stáhněte si šablonu na Etsy.",
    "minimalistická svatba, elegantní svatba, svatební video pozvánka, modrá svatba, svatební oznámení",
    page("navy", "ELEGANTNÍ SVATBA", "Méně je<br><i>někdy více</i>", three("n_date", "n_photo", "n_harm", "navy"),
         "Minimalistická video pozvánka", CZP))
add("listio-vinova-rsvp2", "2026-12-16", "20:30", SVP, V, "vinova", 3,
    "Svatební video pozvánka s RSVP – vínová, pozvánka do mobilu",
    "Svatební video pozvánka s potvrzením účasti: hosté odpoví hned a vy máte přehled. Vínová se zlatou, s harmonogramem dne, úprava v Canvě, odeslání přes WhatsApp. 🍷 Stáhněte si šablonu na Etsy.",
    "potvrzení účasti, svatební video pozvánka, vínová svatba, pozvánka do mobilu, svatební oznámení",
    page("burg", "POTVRZENÍ ÚČASTI", "Kdo přijde?<br><i>Víte hned</i>", pair("b_rsvp", "b_harm", "burg", "Přijdeme! ✓✓"),
         "Vínová pozvánka s RSVP", CZP))
# --- 17. 12.
add("listio-vinova-cz-en-rsvp", "2026-12-17", "09:30", SVP, BB, "burgundy-bil", 4,
    "Svatební pozvánka česky a anglicky – video šablona v Canvě",
    "Svatební pozvánka česky a anglicky jako video – vínová a zlatá, s fotkou, harmonogramem a potvrzením účasti v obou jazycích. Upravíte v Canvě, pošlete přes WhatsApp. 🍷 Stáhněte si šablonu na Etsy.",
    "svatební pozvánka anglicky, dvojjazyčná pozvánka, svatební video pozvánka, šablona canva, svatba 2027",
    page("burg", "ČESKY &amp; ENGLISH", "RSVP<br><i>v obou jazycích</i>", two("b_rsvp", "be_rsvp", "ČESKY", "ENGLISH", "burg"),
         "Pro hosty z Česka i ze zahraničí", CZP))
add("listio-smaragdova-vecer", "2026-12-17", "13:30", SVP, G, "smaragd", 6,
    "Svatební video pozvánka šablona Canva – hotová za jeden večer",
    "Šablona svatební video pozvánky v Canvě: upravíte jména, datum a fotku za jeden večer a pošlete hostům přes WhatsApp. Smaragdově zelená, s hudbou. 💚 Stáhněte si šablonu na Etsy a pozvánka je hotová.",
    "šablona canva, svatební video pozvánka, svatební oznámení, zelená svatba, pozvánka whatsapp",
    page("green", "HOTOVO ZA PÁR MINUT", "Pozvánka hotová<br><i>za jeden večer</i>", single("g_date", "green", ["upravíte jména a datum", "přidáte svou fotku", "pošlete přes WhatsApp", "bez tisku a pošty"]),
         "Smaragdová video pozvánka", CZP, hsize=86))
add("listio-ruzova-romanticka", "2026-12-17", "20:30", RUZ, PB, "pink-bil", 4,
    "Romantická svatební pozvánka do mobilu – růžová video pozvánka",
    "Romantická růžová svatební video pozvánka s květinami – pošlete ji hostům do mobilu, česky i anglicky. Fotka, hudba, informace i potvrzení účasti, úprava v Canvě. 🌸 Stáhněte si šablonu na Etsy.",
    "romantická svatba, růžová svatba, svatební video pozvánka, pozvánka do mobilu, svatební oznámení",
    page("pink", "RŮŽOVÁ &amp; ZELENÁ", "Romantická<br><i>pozvánka do mobilu</i>", single("p_photo", "pink", IT),
         "Video pozvánka s květinami", CZP, hsize=86))
# --- 18. 12.
add("listio-planovac-novy-rok", "2026-12-18", "09:30", PLS, PN, "planovac", 7,
    "Svatební plánovač 2027 – plánování svatby bez stresu, PDF",
    "Svatba v roce 2027? Svatební plánovač PDF česky vás provede vším: checklist na 12 měsíců, rozpočet, hosté, dodavatelé i zasedací pořádek. 🥂 Stáhněte si plánovač na Etsy a začněte nový rok s plánem.",
    "svatební plánovač, svatba 2027, plánování svatby, svatební checklist, rozpočet svatby",
    page("cream", "NOVÝ ROK, NOVÝ PLÁN", "Svatba 2027<br><i>bez stresu</i>", card(PL, 150, 430, 700, 700, -3, "center 70%"),
         "Vše na jednom místě", PLC))
add("listio-en-burgundy-whatsapp", "2026-12-18", "13:30", WVI, BE, "burgundy-en", 5,
    "Digital Wedding Invitation for WhatsApp – Burgundy &amp; Gold".replace("&amp;", "&"),
    "Digital wedding invitation made for WhatsApp: a burgundy and gold video your guests open on their phones, with timeline and RSVP. Edit in Canva in minutes. 🍷 Download the template on Etsy today.",
    "digital wedding invitation, whatsapp invitation, wedding video invitation, burgundy wedding, canva template",
    page("burg", "SAVE THE DATE", "Send it by<br><i>WhatsApp</i>", three("be_harm", "b_en", "be_date", "burg"),
         "Burgundy video invitation", ENP))
add("listio-namornicka-harmonogram", "2026-12-18", "20:30", SVP, N, "namornicka", 5,
    "Svatební video pozvánka s harmonogramem dne – modrá a zlatá",
    "Svatební video pozvánka s harmonogramem dne: hosté vědí, kdy je obřad, oběd i první tanec. Námořnická modrá se zlatou, úprava v Canvě, odeslání přes WhatsApp. 💙 Stáhněte si šablonu na Etsy.",
    "harmonogram svatby, svatební video pozvánka, modrá svatba, svatební oznámení, pozvánka do mobilu",
    page("navy", "HARMONOGRAM DNE", "Hosté vědí,<br><i>kdy a kde</i>", single("n_harm", "navy", ["harmonogram dne", "místo konání", "potvrzení účasti", "vše upravíte v Canvě"]),
         "Modrozlatá video pozvánka", CZP))
# --- 19. 12.
add("listio-vinova-nezapomenutelna", "2026-12-19", "09:30", SVP, V, "vinova", 4,
    "Vínová svatební video pozvánka – animovaná šablona Canva",
    "Vínová svatební video pozvánka se zlatým písmem, která hosty potěší: animace, hudba, vaše fotka a harmonogram dne. Úprava v Canvě za pár minut, odeslání do mobilu. 🍷 Stáhněte si šablonu na Etsy.",
    "vínová svatba, svatební video pozvánka, animovaná pozvánka, šablona canva, svatební oznámení",
    page("burg", "VÍNOVÁ SVATBA", "Pozvánka, na kterou<br><i>se nezapomíná</i>", three("b_date", "b_cz", "b_harm", "burg"),
         "Animovaná pozvánka s hudbou", CZP, hsize=80))
add("listio-rozlucka-smich", "2026-12-19", "13:30", ROZ, R, "rozlucka", 4,
    "Kvíz pro nevěstu a hry na rozlučku – stáhněte PDF",
    "Kvíz pro nevěstu a další hry na rozlučku se svobodou, u kterých se nasmějete do rána. PDF k tisku, stačí vytisknout a hrát. 😄 Stáhněte si hry na Etsy a rozlučka je připravená.",
    "kvíz pro nevěstu, hry na rozlučku, rozlučka se svobodou, rozlučka nevěsty, družičky",
    page("pink", "HRY NA ROZLUČKU", "Smích až<br><i>do rána</i>", card(RZ, 80, 440, 840, 700, 2, "40% center"),
         "Kvíz pro nevěstu a další hry", RZP))
add("listio-vinova-pro-vsechny", "2026-12-19", "20:30", SVP, BB, "burgundy-bil", 5,
    "Svatební video pozvánka pro rodinu i přátele – česky a anglicky",
    "Svatební video pozvánka, které rozumí všichni: česky i anglicky, vínová se zlatou, s hudbou a fotkou. Ideální pro rodinu i přátele ze zahraničí. Úprava v Canvě. 🍷 Stáhněte si šablonu na Etsy.",
    "dvojjazyčná pozvánka, svatební video pozvánka, svatební pozvánka anglicky, vínová svatba, svatba 2027",
    page("burg", "PRO RODINU I PŘÁTELE", "Pozvánka, které<br><i>rozumí všichni</i>", three("b_cz", "b_en", "be_date", "burg"),
         "Česky i anglicky v jedné šabloně", CZP, hsize=86))
# --- 20. 12.
add("listio-planovac-rozpocet2", "2026-12-20", "09:30", PLS, PN, "planovac", 8,
    "Rozpočet svatby 2027 – tabulka ve svatebním plánovači PDF",
    "Rozpočet svatby 2027 pod kontrolou: tabulka výdajů ve svatebním plánovači PDF ukáže, kolik utratíte za místo, jídlo, šaty i fotografa. Česky, k tisku i do tabletu. 💍 Stáhněte si plánovač na Etsy.",
    "rozpočet svatby, kolik stojí svatba, svatební plánovač, plánování svatby, svatba 2027",
    page("cream", "ROZPOČET SVATBY", "Kolik utratíme<br><i>a za co?</i>",
         cardlist(PL, "cream", ["místo a jídlo", "šaty a oblek", "foto a hudba", "výzdoba"], -2, "center 65%"), "Rozpočet přehledně na jednom místě", PLC))
add("listio-smaragdova-v-zelenem", "2026-12-20", "13:30", SVP, G, "smaragd", 7,
    "Zelená svatba 2027 – smaragdová video pozvánka do mobilu",
    "Zelená svatba 2027? Smaragdová svatební video pozvánka s hudbou, fotkou, harmonogramem a informacemi pro hosty (ubytování, dress code). Úprava v Canvě, odeslání do mobilu. 💚 Stáhněte si šablonu na Etsy.",
    "zelená svatba, svatba 2027, svatební video pozvánka, dress code svatba, pozvánka do mobilu",
    page("green", "ZELENÁ SVATBA", "Svatba<br><i>v zeleném</i>", three("g_info", "g_photo", "g_harm", "green"),
         "Informace pro hosty v pozvánce", CZP))
add("listio-ruzova-informace", "2026-12-20", "20:30", RUZ, PB, "pink-bil", 5,
    "Růžová svatební video pozvánka s harmonogramem – Canva",
    "Růžová svatební video pozvánka s harmonogramem, informacemi pro hosty a potvrzením účasti – česky i anglicky. Úprava v Canvě, odeslání do mobilu přes WhatsApp. 🌸 Stáhněte si šablonu na Etsy a potěšte hosty.",
    "růžová svatba, svatební video pozvánka, harmonogram svatby, svatební oznámení, šablona canva",
    page("pink", "SVATBA 2027", "Pozvánka,<br><i>která potěší</i>", three("p_harm", "p_ph2", "p_rsvp", "pink"),
         "Video pozvánka česky i anglicky", CZP))

UTC = {"09:30": "08:30", "13:30": "12:30", "20:30": "19:30"}
RAW = "https://raw.githubusercontent.com/MartinaP777/listio-piny/main/piny/"
CSVN = "listio_piny_12-20-12.csv"
from concurrent.futures import ThreadPoolExecutor
def render(p):
    fn, html = p[0], p[-1]
    hp = f"{OUT}/{fn}.html"; open(hp, "w", encoding="utf-8").write(html)
    png = f"{OUT}/{fn}.png"
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                    f"--user-data-dir=/tmp/chr-{fn}", "--window-size=1000,1500", f"--screenshot={png}", f"file://{hp}"], capture_output=True, timeout=90)
    Image.open(png).convert("RGB").save(f"{OUT}/{fn}.jpg", quality=90); os.remove(png)
rows = []
for (fn, d, t, board, lid, slug, n, title, desc, kw, html) in P:
    assert len(title) <= 100 and len(desc) <= 500, fn
    rows.append({"Title": title, "Media URL": RAW + fn + ".jpg", "Pinterest board": board, "Thumbnail": "", "Description": desc,
                 "Link": f"https://listio.etsy.com/listing/{lid}?utm_source=pinterest&utm_medium=social&utm_content={slug}-pin{n}",
                 "Publish date": f"{d}T{UTC[t]}:00", "Keywords": kw})
with open(f"{OUT}/{CSVN}", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
import sys
if "--csv" not in sys.argv:
    with ThreadPoolExecutor(4) as ex: list(ex.map(render, P))
    ims = [Image.open(f"{OUT}/{p[0]}.jpg").resize((250, 375)) for p in P]
    s = Image.new("RGB", (9 * 250, 3 * 375), "white")   # sloupec = den, radek = cas
    for i, im in enumerate(ims): s.paste(im, ((i // 3) * 250, (i % 3) * 375))
    s.save(f"{OUT}/kolaz-12-20-12.jpg", quality=85)
print(len(P))
