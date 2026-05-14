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
- ⏸️ **Auto-pauza** — psaní se automaticky pozastaví pokud je fokus na AutoTyperu místo cílového pole
- 🔍 **Automatické nalezení Tesseractu** — není potřeba ručně nastavovat cestu

---

## 📦 Instalace

### Prerekvizity

- **Python 3.10+** — [python.org](https://www.python.org/downloads/) — při instalaci zatrhnout **"Add Python to PATH"**
- **winget** — součástí Windows 10/11

### 1. Spusť installer

Dvakrát klikni na `installer.bat` (nebo pravým tlačítkem → **Spustit jako správce** pokud narazíš na problémy s oprávněními).

Installer automaticky:
- nainstaluje všechny Python knihovny (`customtkinter`, `pillow`, `pytesseract`, `pynput`, `pyinstaller`)
- stáhne a nainstaluje **Tesseract OCR** přes winget
- sestaví `AutoTyper.exe` s progress barem

### 2. Spusť aplikaci

Hotový EXE najdeš v:
```
dist\AutoTyper.exe
```

> Tesseract se hledá automaticky — žádná ruční konfigurace cesty není potřeba.  
> Pokud ho installer nenajde, zobrazí se chybová hláška s instrukcemi.

---

## 🚀 Použití

| Krok | Popis |
|------|-------|
| 1 | Stiskni **F8** nebo klikni na **▶ SPUSTIT OCR** |
| 2 | Přetáhni výběr přes oblast s textem |
| 3 | Přepni do cílového pole (máš X sekund dle nastaveného čekání) |
| 4 | AutoTyper začne psát — pokud klikneš zpět na AutoTyper, psaní se **pozastaví** dokud neklikneš jinam |

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
- [pyinstaller](https://pyinstaller.org/)
- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)

---

## 📄 Licence

MIT — volně použitelné a upravitelné.
