import tkinter as tk
import random

# Hiragana dictionary
hiragana = {
    "a": "あ", "i": "い", "u": "う", "e": "え", "o": "お",
    "ka": "か", "ki": "き", "ku": "く", "ke": "け", "ko": "こ",
    "sa": "さ", "shi": "し", "su": "す", "se": "せ", "so": "そ",
    "ta": "た", "chi": "ち", "tsu": "つ", "te": "て", "to": "と",
    "na": "な", "ni": "に", "nu": "ぬ", "ne": "ね", "no": "の",
    "ha": "は", "hi": "ひ", "fu": "ふ", "he": "へ", "ho": "ほ",
    "ma": "ま", "mi": "み", "mu": "む", "me": "め", "mo": "も",
    "ya": "や", "yu": "ゆ", "yo": "よ",
    "ra": "ら", "ri": "り", "ru": "る", "re": "れ", "ro": "ろ",
    "wa": "わ", "wo": "を", "n": "ん"
}

# --- SETUP ---
root = tk.Tk()
root.title("Hiragana Matching Game JP 🎴")
root.geometry("720x500")
root.config(bg="#FFF8E0")

# --- VARIABLES ---
unseen = list(hiragana.items())
random.shuffle(unseen)

current_set = []
matched = {}
symbol_buttons = []
romaji_buttons = []
round_active = False
error_count = 0
correct_total = 0
selected_symbol = None
selected_romaji = None

# --- HEADER CON ESTILO JAPONÉS ---
header_frame = tk.Frame(root, bg="#E74C3C", height=60)
header_frame.pack(fill="x", pady=(0, 10))

title_label = tk.Label(header_frame, 
                      text="🎌 Hiragana Match Master JP", 
                      font=("MS Gothic", 24, "bold"), 
                      fg="white", bg="#E74C3C")
title_label.pack(pady=10)

subtitle_label = tk.Label(header_frame,
                        text="Empareja los caracteres con su pronunciación",
                        font=("Arial", 12),
                        fg="#FFECB3", bg="#E74C3C")
subtitle_label.pack()

# --- FRAMES ---
symbol_frame = tk.Frame(root, bg="#FFF8E0")
symbol_frame.pack(pady=10)

romaji_frame = tk.Frame(root, bg="#FFF8E0")
romaji_frame.pack(pady=10)

status_label = tk.Label(root, text="", font=("Arial", 14), bg="#FFF8E0")
status_label.pack(pady=5)

stats_label = tk.Label(root, text="", font=("Arial", 12), bg="#FFF8E0")
stats_label.pack(pady=5)

# --- FUNCIONES PRINCIPALES MODIFICADAS ---

def update_stats():
    stats_label.config(
        text=f"Progreso: {correct_total}/46 | Errores: {error_count}"
    )

def next_round():
    global current_set, matched, round_active, selected_symbol, selected_romaji

    matched = {}
    selected_symbol = None
    selected_romaji = None

    for btn in symbol_buttons + romaji_buttons:
        btn.destroy()

    symbol_buttons.clear()
    romaji_buttons.clear()

    # MODIFICACIÓN: Mostrar las cartas restantes aunque sean menos de 4
    remaining = min(4, len(unseen))
    if remaining == 0:
        status_label.config(text="✅ ¡Juego completado! Todas las cartas emparejadas", fg="green")
        update_stats()
        return

    current_set = [unseen.pop() for _ in range(remaining)]
    round_active = False

    animate_shuffle()

def animate_shuffle():
    steps = 5
    delay = 150

    def do_shuffle(step):
        if step <= 0:
            show_cards()
            return
        random.shuffle(current_set)
        show_temp_symbols()
        root.after(delay, lambda: do_shuffle(step - 1))

    do_shuffle(steps)

def show_temp_symbols():
    for btn in symbol_buttons:
        btn.destroy()
    symbol_buttons.clear()

    for i, (_, symbol) in enumerate(current_set):
        btn = tk.Button(symbol_frame, text=symbol, font=("Arial", 36),
                        width=3, height=1, bg="#DCE775")
        btn.grid(row=0, column=i, padx=15)
        symbol_buttons.append(btn)

def show_cards():
    global round_active
    round_active = True

    for btn in symbol_buttons + romaji_buttons:
        btn.destroy()
    symbol_buttons.clear()
    romaji_buttons.clear()

    # Mostrar símbolos (seleccionables)
    for i, (romaji, symbol) in enumerate(current_set):
        btn = tk.Button(symbol_frame, text=symbol, font=("Arial", 36),
                        width=3, height=1, bg="#FFFFFF", relief="ridge",
                        activebackground="#FFF176")
        btn.grid(row=0, column=i, padx=15)
        btn.config(command=lambda b=btn, r=romaji: on_symbol_click(b, r))
        symbol_buttons.append(btn)

    # Mostrar pronunciaciones (seleccionables)
    romajis = [romaji for romaji, _ in current_set]
    random.shuffle(romajis)

    for i, romaji in enumerate(romajis):
        btn = tk.Button(romaji_frame, text=romaji, font=("Arial", 14),
                        width=10, height=2, bg="#F5F5F5",
                        relief="groove", activebackground="#FFF176")
        btn.grid(row=0, column=i, padx=15)
        btn.config(command=lambda b=btn, r=romaji: on_romaji_click(b, r))
        romaji_buttons.append(btn)

    update_stats()

def on_symbol_click(button, romaji):
    global selected_symbol
    if not round_active or romaji in matched:
        return

    reset_symbol_buttons()
    button.config(bg="#FFF176")
    selected_symbol = (button, romaji)
    validate_match()

def on_romaji_click(button, romaji):
    global selected_romaji
    if not round_active or romaji in matched:
        return

    reset_romaji_buttons()
    button.config(bg="#FFF176")
    selected_romaji = (button, romaji)
    validate_match()

def reset_symbol_buttons():
    for btn in symbol_buttons:
        btn.config(bg="#FFFFFF")

def reset_romaji_buttons():
    for btn in romaji_buttons:
        btn.config(bg="#F5F5F5")

def validate_match():
    global selected_symbol, selected_romaji, correct_total, error_count, round_active

    if selected_symbol and selected_romaji:
        sym_btn, sym_romaji = selected_symbol
        rom_btn, rom_romaji = selected_romaji

        if sym_romaji == rom_romaji:
            sym_btn.config(bg="lightgreen", state="disabled")
            rom_btn.config(bg="lightgreen", state="disabled")
            matched[sym_romaji] = True
            correct_total += 1
            status_label.config(text="✅ ¡Correcto!", fg="green")
        else:
            sym_btn.config(bg="tomato")
            rom_btn.config(bg="tomato")
            error_count += 1
            status_label.config(text="❌ Incorrecto, intenta de nuevo", fg="red")

        selected_symbol = None
        selected_romaji = None
        update_stats()

        # MODIFICACIÓN: Verificar si todas las cartas actuales están emparejadas
        if len(matched) == len(current_set):
            round_active = False
            root.after(1200, next_round)

# --- INICIO ---
next_round()
root.mainloop()