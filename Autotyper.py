import tkinter as tk
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
# TESSERACT
# ==================================================

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\User\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

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
root.geometry("500x660")
root.resizable(False, False)
root.attributes("-topmost", True)
root.configure(fg_color=BG)

# ==================================================
# VARIABLES
# ==================================================

speed_var  = tk.DoubleVar(value=0.08)
delay_var  = tk.DoubleVar(value=4.0)
repeat_var = tk.StringVar(value="1")
style_var  = tk.StringVar(value="normal")

# ==================================================
# OCR AREA SELECT
# ==================================================

start_x = start_y = end_x = end_y = 0


def select_area():
    global start_x, start_y, end_x, end_y

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
# SLOW TYPE
# ==================================================


def slow_type(text, speed):
    for char in text:
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

    bbox = select_area()

    set_status("⟳  Zpracovávám OCR...", SUBTEXT)
    screenshot = ImageGrab.grab(bbox=bbox)

    text = pytesseract.image_to_string(screenshot, lang="eng")
    text = clean_text(text)

    if style_var.get() == "inverted":
        text = text[::-1]

    text_box.configure(state="normal")
    text_box.delete("1.0", tk.END)
    text_box.insert(tk.END, text)
    text_box.configure(state="disabled")

    delay = delay_var.get()
    for remaining in range(int(delay), 0, -1):
        set_status(f"⏱  Klikni do cílového pole... {remaining}s", WARNING)
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


make_slider(root, "Rychlost psaní", "Prodleva mezi znaky",
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

text_box = ctk.CTkTextbox(
    out_card,
    fg_color=SURFACE,
    text_color=TEXT,
    font=ctk.CTkFont("Consolas", 10),
    corner_radius=0,
    border_width=0,
    wrap="word",
    state="disabled",
    scrollbar_button_color=BORDER,
    scrollbar_button_hover_color=ACCENT,
)
text_box.pack(fill="both", expand=True, padx=6, pady=(0, 6))

# ==================================================
# START
# ==================================================

root.mainloop()
