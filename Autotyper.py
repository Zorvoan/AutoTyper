import tkinter as tk
import sys
import os
import urllib.request
import json
import subprocess
import tempfile

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)
import customtkinter as ctk
from PIL import ImageGrab
import pytesseract
from pynput.keyboard import Controller, Key
from pynput import keyboard
import threading
import time
import re
import ctypes

ctypes.windll.user32.SetProcessDPIAware()

# ==================================================
# VERZE
# ==================================================

CURRENT_VERSION = "1.2.0"
GITHUB_REPO     = "Zorvoan/AutoTyper"

# ==================================================
# TESSERACT
# ==================================================

def find_tesseract():
    candidates = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        os.path.join(os.environ.get("LOCALAPPDATA", ""), r"Programs\Tesseract-OCR\tesseract.exe"),
        os.path.join(os.environ.get("APPDATA", ""),       r"Programs\Tesseract-OCR\tesseract.exe"),
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path
    import shutil
    found = shutil.which("tesseract")
    if found:
        return found
    return None

_tess = find_tesseract()
if _tess:
    pytesseract.pytesseract.tesseract_cmd = _tess
    # Nastav TESSDATA_PREFIX na tessdata slozku vedle tesseract.exe
    # Prepise pripadne spatne nastavenou systemovou env promennou
    _tessdata = os.path.join(os.path.dirname(_tess), "tessdata")
    if os.path.isdir(_tessdata):
        os.environ["TESSDATA_PREFIX"] = _tessdata
else:
    import tkinter.messagebox as mb
    mb.showerror(
        "Tesseract nenalezen",
        "Tesseract OCR nebyl nalezen.\n\nNainstaluj ho pres installer.bat\nnebo nastav cestu rucne v Autotyper.py."
    )

# ==================================================
# UPDATE CHECKER
# ==================================================

def check_for_update():
    try:
        url = "https://api.github.com/repos/" + GITHUB_REPO + "/releases/latest"
        req = urllib.request.Request(url, headers={"User-Agent": "AutoTyper"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
        latest = data.get("tag_name", "").lstrip("v")
        if latest and latest != CURRENT_VERSION:
            exe_url = None
            for asset in data.get("assets", []):
                if asset["name"].lower().endswith(".exe"):
                    exe_url = asset["browser_download_url"]
                    break
            root.after(0, lambda: show_update_banner(latest, exe_url))
    except Exception:
        pass

def show_update_banner(new_version, exe_url):
    banner = ctk.CTkFrame(root, fg_color="#2a1f3d", corner_radius=10)
    banner.pack(fill="x", padx=18, pady=(0, 6), before=slider_frame_speed)

    left = ctk.CTkFrame(banner, fg_color="transparent")
    left.pack(side="left", padx=14, pady=8)

    ctk.CTkLabel(left,
                 text="Dostupna nova verze v" + new_version,
                 font=ctk.CTkFont("Segoe UI", 11, "bold"),
                 text_color="#c084fc").pack(anchor="w")
    ctk.CTkLabel(left,
                 text="Aktualni verze: v" + CURRENT_VERSION,
                 font=ctk.CTkFont("Segoe UI", 10),
                 text_color=SUBTEXT).pack(anchor="w")

    def do_update():
        if not exe_url:
            import webbrowser
            webbrowser.open("https://github.com/" + GITHUB_REPO + "/releases/latest")
            return
        update_btn.configure(state="disabled", text="Stahuji...")
        threading.Thread(target=download_and_replace, args=(exe_url,), daemon=True).start()

    update_btn = ctk.CTkButton(
        banner,
        text="Aktualizovat",
        command=do_update,
        fg_color="#7c3aed",
        hover_color="#6d28d9",
        text_color="#ffffff",
        font=ctk.CTkFont("Segoe UI", 11, "bold"),
        width=130,
        height=32,
        corner_radius=8,
    )
    update_btn.pack(side="right", padx=14, pady=8)

def download_and_replace(exe_url):
    try:
        current_exe = sys.executable if getattr(sys, "frozen", False) else None
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".exe")
        tmp.close()
        urllib.request.urlretrieve(exe_url, tmp.name)
        if current_exe:
            bat = tempfile.NamedTemporaryFile(delete=False, suffix=".bat", mode="w")
            bat.write("@echo off\n")
            bat.write("timeout /t 2 >nul\n")
            bat.write("move /y \"" + tmp.name + "\" \"" + current_exe + "\"\n")
            bat.write("start \"\" \"" + current_exe + "\"\n")
            bat.write("del \"%~f0\"\n")
            bat.close()
            subprocess.Popen(["cmd", "/c", bat.name], creationflags=subprocess.CREATE_NO_WINDOW)
            root.after(0, root.destroy)
        else:
            import webbrowser
            webbrowser.open("https://github.com/" + GITHUB_REPO + "/releases/latest")
    except Exception as e:
        root.after(0, lambda: set_status("[!] Update selhal: " + str(e), WARNING))

# ==================================================
# THEME
# ==================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ACCENT  = "#5865f2"
ACCENT2 = "#4752c4"
SUCCESS = "#43b581"
WARNING = "#faa61a"
TEXT    = "#e8eaf6"
SUBTEXT = "#8b8fa8"
BG      = "#0f1117"
SURFACE = "#1a1d27"
BORDER  = "#2a2d3e"

# ==================================================
# KEYBOARD
# ==================================================

kb = Controller()

# ==================================================
# WINDOW
# ==================================================

root = ctk.CTk()
root.title("OCR AutoTyper")
icon_path = resource_path("icon.ico")
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)
root.geometry("500x780")
root.resizable(False, False)
root.attributes("-topmost", True)
root.configure(fg_color=BG)

# ==================================================
# VARIABLES
# ==================================================

speed_var  = tk.DoubleVar(value=0.08)
delay_var  = tk.DoubleVar(value=4.0)
repeat_var  = tk.StringVar(value="1")
style_var   = tk.StringVar(value="normal")
filter_on   = tk.BooleanVar(value=False)
filter_char = tk.StringVar(value="a")

# ==================================================
# OCR AREA SELECT
# ==================================================

start_x = start_y = end_x = end_y = 0


def select_area():
    global start_x, start_y, end_x, end_y

    # Reset pred kazdym vyberem
    start_x = start_y = end_x = end_y = 0

    overlay = tk.Toplevel(root)
    overlay.attributes("-fullscreen", True)
    overlay.attributes("-alpha", 0.35)
    overlay.attributes("-topmost", True)
    overlay.configure(bg="black")

    overlay.update()
    hwnd = ctypes.windll.user32.GetParent(overlay.winfo_id())
    HWND_TOPMOST = -1
    SWP_NOMOVE   = 0x0002
    SWP_NOSIZE   = 0x0001
    ctypes.windll.user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)
    ctypes.windll.user32.SetForegroundWindow(hwnd)

    canvas = tk.Canvas(overlay, cursor="cross", bg="black", highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    rect = None

    def mouse_down(event):
        global start_x, start_y
        start_x, start_y = event.x, event.y

    def mouse_move(event):
        nonlocal rect
        if rect:
            canvas.delete(rect)
        rect = canvas.create_rectangle(
            start_x, start_y, event.x, event.y,
            outline=ACCENT, width=2, dash=(4, 2)
        )

    def mouse_up(event):
        global end_x, end_y
        end_x, end_y = event.x, event.y
        overlay.destroy()

    canvas.bind("<ButtonPress-1>",   mouse_down)
    canvas.bind("<B1-Motion>",       mouse_move)
    canvas.bind("<ButtonRelease-1>", mouse_up)

    overlay.grab_set()
    root.wait_window(overlay)

    return (
        min(start_x, end_x), min(start_y, end_y),
        max(start_x, end_x), max(start_y, end_y)
    )

# ==================================================
# CLEAN TEXT
# ==================================================


def clean_text(text):
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# ==================================================
# FOCUS CHECK
# ==================================================

def is_autotyper_focused():
    """Vrati True pokud ma fokus okno AutoTyperu (ne cilove pole)."""
    try:
        hwnd_focused = ctypes.windll.user32.GetForegroundWindow()
        hwnd_root = ctypes.windll.user32.GetParent(root.winfo_id())
        if hwnd_root == 0:
            hwnd_root = root.winfo_id()
        return hwnd_focused == hwnd_root
    except Exception:
        return False

# ==================================================
# SLOW TYPE
# ==================================================


def slow_type(text, speed):
    for char in text:
        # Pokud je fokus na AutoTyperu, pozastav a cekej
        while is_autotyper_focused():
            set_status("⏸  Klikni do ciloveho pole pro pokracovani...", WARNING)
            time.sleep(0.2)
        set_status("⌨  Píšu...", SUCCESS)
        kb.type(char)
        time.sleep(speed)

# ==================================================
# STATUS HELPER
# ==================================================


def set_status(msg, color=TEXT):
    status_label.configure(text=msg, text_color=color)
    root.update_idletasks()

# ==================================================
# OCR PROCESS
# ==================================================


def process_ocr():
    start_btn.configure(state="disabled", text="⏳  Běží...")
    set_status("▣  Vyber oblast na obrazovce...", WARNING)

    # Skryj okno aby se nedostalo do screenshotu
    root.after(0, root.withdraw)
    time.sleep(0.3)

    bbox = select_area()

    # Pokud uzivatel nic nevybral (zadne tazeni), zrus
    if bbox[0] == bbox[2] or bbox[1] == bbox[3]:
        root.after(0, root.deiconify)
        set_status("●  Připraveno", SUCCESS)
        start_btn.configure(state="normal", text="▶   SPUSTIT OCR")
        return

    set_status("⟳  Zpracovávám OCR...", SUBTEXT)
    screenshot = ImageGrab.grab(bbox=bbox)

    # Obnov okno az po screenshotu
    root.after(0, root.deiconify)

    text = pytesseract.image_to_string(screenshot, lang="eng")
    text = clean_text(text)

    if style_var.get() == "inverted":
        text = text[::-1]

    # Filtr slov podle pismenka
    if filter_on.get():
        char = filter_char.get().lower()
        words = text.split()
        filtered = [w for w in words if char in w.lower()]
        text = " ".join(filtered)

    text_box.configure(state="normal")
    text_box.delete("1.0", tk.END)
    text_box.insert(tk.END, text)
    text_box.configure(state="disabled")

    delay = delay_var.get()
    for remaining in range(int(delay), 0, -1):
        set_status(f"⏱  Klikni do textového pole... {remaining}s", WARNING)
        time.sleep(1)

    set_status("⌨  Píšu...", SUCCESS)

    repeat = int(repeat_var.get())
    for i in range(repeat):
        slow_type(text, speed_var.get())
        if i < repeat - 1:
            kb.press(Key.space)
            kb.release(Key.space)

    set_status("✓  Hotovo", SUCCESS)
    start_btn.configure(state="normal", text="▶   SPUSTIT OCR")

# ==================================================
# THREAD
# ==================================================


def start_thread():
    threading.Thread(target=process_ocr, daemon=True).start()

# ==================================================
# HOTKEY
# ==================================================


def on_press(key):
    if key == keyboard.Key.f8:
        start_thread()


listener = keyboard.Listener(on_press=on_press)
listener.start()

root.after(1000, lambda: threading.Thread(target=check_for_update, daemon=True).start())

# ==================================================
# GUI
# ==================================================

# ── Header ──────────────────────────────────────────
header = ctk.CTkFrame(root, fg_color="transparent")
header.pack(fill="x", padx=18, pady=(18, 0))

ctk.CTkLabel(
    header,
    text="OCR AutoTyper",
    font=ctk.CTkFont("Segoe UI", 18, "bold"),
    text_color=TEXT,
).pack(side="left")

ctk.CTkLabel(
    header,
    text="  F8  ",
    font=ctk.CTkFont("Segoe UI", 11, "bold"),
    fg_color=ACCENT,
    text_color="#ffffff",
    corner_radius=6,
).pack(side="right", pady=4)

# divider
ctk.CTkFrame(root, height=1, fg_color=BORDER).pack(fill="x", padx=18, pady=(10, 6))

# ── Slider helper ────────────────────────────────────
def make_slider(parent, label, sublabel, variable, from_, to, fmt):
    card = ctk.CTkFrame(parent, fg_color=SURFACE, corner_radius=10)
    card.pack(fill="x", padx=18, pady=(0, 8))

    top = ctk.CTkFrame(card, fg_color="transparent")
    top.pack(fill="x", padx=14, pady=(10, 0))

    ctk.CTkLabel(top, text=label,
                 font=ctk.CTkFont("Segoe UI", 16, "bold"),
                 text_color=TEXT).pack(side="left")

    val_lbl = ctk.CTkLabel(top, text=fmt(variable.get()),
                           font=ctk.CTkFont("Segoe UI", 16, "bold"),
                           text_color=ACCENT)
    val_lbl.pack(side="right")

    ctk.CTkLabel(card, text=sublabel,
                 font=ctk.CTkFont("Segoe UI", 10),
                 text_color=SUBTEXT).pack(anchor="w", padx=14)

    def on_change(v):
        val_lbl.configure(text=fmt(float(v)))

    ctk.CTkSlider(
        card,
        from_=from_, to=to,
        variable=variable,
        command=on_change,
        button_color=ACCENT,
        button_hover_color=ACCENT2,
        progress_color=ACCENT,
        fg_color=BORDER,
    ).pack(fill="x", padx=14, pady=(4, 12))
    return card


slider_frame_speed = make_slider(root, "Rychlost psaní", "Prodleva mezi znaky",
            speed_var, 0.01, 0.3, lambda v: f"{v:.2f} s")

make_slider(root, "Čekání před psaním", "Čas na přepnutí do cílového pole",
            delay_var, 1.0, 15.0, lambda v: f"{int(v)} s")

# ── Repeat + Style row ───────────────────────────────
row = ctk.CTkFrame(root, fg_color="transparent")
row.pack(fill="x", padx=18, pady=(0, 8))
row.columnconfigure(0, weight=1)
row.columnconfigure(1, weight=1)

for col, (var, lbl, vals) in enumerate([
    (repeat_var, "Opakování",  ["1", "2", "3", "4", "5"]),
    (style_var,  "Styl psaní", ["normal", "inverted"]),
]):
    card = ctk.CTkFrame(row, fg_color=SURFACE, corner_radius=10)
    card.grid(row=0, column=col, sticky="nsew", padx=(0, 4) if col == 0 else (4, 0))

    ctk.CTkLabel(card, text=lbl,
                 font=ctk.CTkFont("Segoe UI", 13, "bold"),
                 text_color=TEXT).pack(anchor="w", padx=14, pady=(10, 0))

    ctk.CTkOptionMenu(
        card,
        variable=var,
        values=vals,
        fg_color=BORDER,
        button_color=ACCENT,
        button_hover_color=ACCENT2,
        text_color=TEXT,
        dropdown_fg_color=SURFACE,
        dropdown_hover_color=BORDER,
        dropdown_text_color=TEXT,
        corner_radius=8,
        font=ctk.CTkFont("Segoe UI", 10),
    ).pack(fill="x", padx=14, pady=(6, 12))

# ── Filter row ───────────────────────────────────────
filter_card = ctk.CTkFrame(root, fg_color=SURFACE, corner_radius=10)
filter_card.pack(fill="x", padx=18, pady=(0, 8))

filter_top = ctk.CTkFrame(filter_card, fg_color="transparent")
filter_top.pack(fill="x", padx=14, pady=(10, 0))

ctk.CTkLabel(filter_top, text="Filtr slov",
             font=ctk.CTkFont("Segoe UI", 13, "bold"),
             text_color=TEXT).pack(side="left")

filter_toggle = ctk.CTkSwitch(
    filter_top,
    text="",
    variable=filter_on,
    button_color=ACCENT,
    button_hover_color=ACCENT2,
    progress_color=ACCENT,
    fg_color=BORDER,
    width=40,
)
filter_toggle.pack(side="right")

filter_bottom = ctk.CTkFrame(filter_card, fg_color="transparent")
filter_bottom.pack(fill="x", padx=14, pady=(4, 10))

ctk.CTkLabel(filter_bottom,
             text="Pouze slova obsahujici pismeno:",
             font=ctk.CTkFont("Segoe UI", 10),
             text_color=SUBTEXT).pack(side="left")

LETTERS = list("abcdefghijklmnopqrstuvwxyz")
ctk.CTkOptionMenu(
    filter_bottom,
    variable=filter_char,
    values=LETTERS,
    fg_color=BORDER,
    button_color=ACCENT,
    button_hover_color=ACCENT2,
    text_color=TEXT,
    dropdown_fg_color=SURFACE,
    dropdown_hover_color=BORDER,
    dropdown_text_color=TEXT,
    corner_radius=8,
    font=ctk.CTkFont("Segoe UI", 10),
    width=60,
).pack(side="right")

# ── Start button ─────────────────────────────────────
start_btn = ctk.CTkButton(
    root,
    text="▶   SPUSTIT OCR",
    command=start_thread,
    fg_color=ACCENT,
    hover_color=ACCENT2,
    text_color="#ffffff",
    font=ctk.CTkFont("Segoe UI", 14, "bold"),
    height=44,
    corner_radius=10,
)
start_btn.pack(fill="x", padx=18, pady=(0, 8))

# ── Status bar ───────────────────────────────────────
status_frame = ctk.CTkFrame(root, fg_color=SURFACE, corner_radius=10, height=36)
status_frame.pack(fill="x", padx=18, pady=(0, 8))
status_frame.pack_propagate(False)

status_label = ctk.CTkLabel(
    status_frame,
    text="●  Připraveno",
    font=ctk.CTkFont("Segoe UI", 11),
    text_color=SUCCESS,
    anchor="w",
)
status_label.pack(fill="x", padx=14, pady=8)

# ── OCR text output ──────────────────────────────────
out_card = ctk.CTkFrame(root, fg_color=SURFACE, corner_radius=10)
out_card.pack(fill="both", expand=True, padx=18, pady=(0, 8))

ctk.CTkLabel(out_card, text="ROZPOZNANÝ TEXT",
             font=ctk.CTkFont("Segoe UI", 10, "bold"),
             text_color=SUBTEXT).pack(anchor="w", padx=14, pady=(8, 0))

ctk.CTkFrame(out_card, height=1, fg_color=BORDER).pack(fill="x", padx=14, pady=(4, 0))

# Vlastni scrollbar s kulatymi hranami
text_scroll_frame = ctk.CTkFrame(out_card, fg_color=SURFACE, corner_radius=0)
text_scroll_frame.pack(fill="both", expand=True, padx=6, pady=(0, 6))

scrollbar = ctk.CTkScrollbar(
    text_scroll_frame,
    orientation="vertical",
    button_color=ACCENT,
    button_hover_color=ACCENT2,
    fg_color=SURFACE,
    corner_radius=10,
    width=8,
)
scrollbar.pack(side="right", fill="y", padx=(0, 4), pady=6)

text_box = ctk.CTkTextbox(
    text_scroll_frame,
    fg_color=SURFACE,
    text_color=TEXT,
    font=ctk.CTkFont("Consolas", 10),
    corner_radius=0,
    border_width=0,
    wrap="word",
    state="disabled",
    yscrollcommand=scrollbar.set,
    scrollbar_button_color=SURFACE,
    scrollbar_button_hover_color=SURFACE,
)
text_box.pack(side="left", fill="both", expand=True)
scrollbar.configure(command=text_box.yview)

# ==================================================
# START
# ==================================================

root.mainloop()