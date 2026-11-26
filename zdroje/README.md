# Podklady pro generátor pinů (kod/pins2.py)

- `frames/` – snímky obrazovek video pozvánek (540 px šířka), vytažené z videí ve Stažených souborech
  - `g_*` zelená/smaragdová (v15) · `b_*` vínová CZ (v16) · `be_*` vínová EN (v16) · `n_*` námořnická (v14) · `p_*` růžová CZ (v3) · `pe_*` růžová EN (v3)
  - přípony: title, photo, date, harm (harmonogram), info, rsvp; `p_ph2` = růžová titulka, `b_cz`/`b_en`/`p_en` = titulky
- `Listio-planovac-foto.jpg` – fotka svatebního plánovače
- `Listio-rozlucka-foto.jpg` – fotka družiček s hrami na rozlučku

Spuštění: `python3 kod/pins2.py` → `out/` (JPG, CSV, koláž). Hotové piny kopírovat do `piny/`.
