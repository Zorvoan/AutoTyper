# 🖥️ OCR AutoTyper

**Automaticky přečte text z obrazovky a napíše ho za tebe — kdekoliv.**

Vyber oblast na monitoru, OCR ji rozpozná a AutoTyper text postupně opíše do libovolného pole. Ideální pro situace, kdy copy-paste nefunguje (hry, locked inputy, virtuální stroje, apod.).

---

## ✨ Funkce

- 📸 **Výběr oblasti** — kliknutím a tažením vybereš přesně tu část obrazovky
- 🔤 **OCR rozpoznávání** — powered by Tesseract OCR
- ⌨️ **Pomalé psaní** — nastavitelná rychlost, přirozené tempo
- ⏱️ **Časovač** — čas na přepnutí do cílového okna před začátkem psaní
- 🔁 **Opakování** — text lze napsat vícekrát za sebou
- 🔄 **Inverted mód** — napíše text pozpátku
- ⌨️ **Hotkey F8** — spuštění bez klikání na tlačítko

---

## 📦 Instalace

### 1. Prerekvizity

- **Python 3.10+** — [python.org](https://www.python.org/downloads/)
- **pip** — součástí Pythonu
- **winget** — součástí Windows 10/11

### 2. Spusť installer

Klikni pravým tlačítkem na `installer.bat` → **Spustit jako správce** - `Není povinné`

Installer automaticky:
- nainstaluje všechny Python knihovny (`customtkinter`, `pillow`, `pytesseract`, `pynput`)
- stáhne a nainstaluje **Tesseract OCR**

### 3. Nastav cestu k Tesseractu

V souboru `Autotyper.py` uprav řádek 18 tak, aby odpovídal tvé instalaci:

```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\TVOJE_JMENO\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
```

> Výchozí cesta po instalaci přes winget je zpravidla `C:\Users\<uživatel>\AppData\Local\Programs\Tesseract-OCR\tesseract.exe`

### 4. Spusť aplikaci

```bash
python Autotyper.py
```

---

## 🚀 Použití

| Krok | Popis |
|------|-------|
| 1 | Stiskni **F8** nebo klikni na **▶ SPUSTIT OCR** |
| 2 | Přetáhni výběr přes oblast s textem |
| 3 | Přepni do cílového pole (máš X sekund dle nastaveného čekání) |
| 4 | AutoTyper začne psát |

---

## ⚙️ Nastavení

| Parametr | Popis | Výchozí |
|----------|-------|---------|
| Rychlost psaní | Prodleva mezi jednotlivými znaky | 0.08 s |
| Čekání před psaním | Čas na přepnutí do cílového okna | 4 s |
| Opakování | Kolikrát se text napíše | 1× |
| Styl | `normal` / `inverted` (text pozpátku) | normal |

---

## 🛠️ Závislosti

- [customtkinter](https://github.com/TomSchimansky/CustomTkinter)
- [Pillow](https://python-pillow.org/)
- [pytesseract](https://github.com/madmaze/pytesseract)
- [pynput](https://github.com/moses-palmer/pynput)
- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)

---

## 📄 Licence

MIT — volně použitelné a upravitelné.
