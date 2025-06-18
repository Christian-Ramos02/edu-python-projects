import tkinter as tk
from tkinter import messagebox
import random

# Diccionario completo de vocabulario financiero
financial_vocab = {
    # Básicos
    "Revenue": "Ingresos",
    "Profit": "Beneficio",
    "Loss": "Pérdida",
    "Investment": "Inversión",
    "Interest": "Interés",
    "Dividend": "Dividendo",
    "Stock": "Acción",
    "Bond": "Bono",
    "Asset": "Activo",
    "Liability": "Pasivo",
    "Equity": "Patrimonio neto",
    "Debt": "Deuda",
    "Capital": "Capital",
    "Cash Flow": "Flujo de caja",
    "Loan": "Préstamo",
    "Budget": "Presupuesto",

    # Intermedios/Avanzados
    "Return on Equity (ROE)": "Rentabilidad sobre el patrimonio",
    "Earnings Per Share (EPS)": "Ganancias por acción",
    "Price-to-Earnings Ratio (P/E)": "Relación precio/ganancia",
    "Net Present Value (NPV)": "Valor actual neto",
    "Internal Rate of Return (IRR)": "Tasa interna de retorno",
    "Compound Interest": "Interés compuesto",
    "Amortization": "Amortización",
    "Depreciation": "Depreciación",
    "Working Capital": "Capital de trabajo",
    "Liquidity": "Liquidez",
    "Volatility": "Volatilidad",
    "Risk Premium": "Prima de riesgo",
    "Leverage": "Apalancamiento",
    "Default Risk": "Riesgo de incumplimiento",
    "Underwriting": "Suscripción (de valores)",
    "Hedging": "Cobertura",
    "Derivatives": "Derivados",
    "Yield": "Rendimiento",
    "Benchmark": "Referencia de comparación",
    "Valuation": "Valoración",
    "Arbitrage": "Arbitraje"
}

# Separamos términos básicos y avanzados
basic_terms = list(financial_vocab.items())[:16]
advanced_terms = list(financial_vocab.items())[16:]

class FinancialVocabularyGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Financial Vocabulary Matcher JP 💹")
        self.geometry("1000x550")
        self.config(bg="#F0F8FF")
        
        # Variables de estado
        self.unseen = []
        self.current_set = []
        self.matched = {}
        self.term_buttons = []
        self.definition_buttons = []
        self.round_active = False
        self.error_count = 0
        self.correct_total = 0
        self.selected_term = None
        self.selected_definition = None
        self.advanced_mode = tk.BooleanVar(value=False)
        
        self.create_widgets()
        self.reset_game()
    
    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self, bg="#0056b3", height=80)
        header_frame.pack(fill="x", pady=(0, 10))

        tk.Label(header_frame, 
                text="💼 Financial Vocabulary Master JP", 
                font=("Arial", 24, "bold"), 
                fg="white", bg="#0056b3").pack(pady=5)
        
        tk.Label(header_frame,
                text="Empareja términos financieros con sus definiciones",
                font=("Arial", 12),
                fg="#FFD700", bg="#0056b3").pack()
        
        # Toggle Modo Avanzado
        mode_frame = tk.Frame(self, bg="#F0F8FF")
        mode_frame.pack(pady=5)
        
        self.advanced_toggle = tk.Checkbutton(
            mode_frame, 
            text="Modo CFA/Wall Street (Términos Avanzados)",
            variable=self.advanced_mode, 
            font=("Arial", 10, "bold"),
            bg="#F0F8FF", 
            command=self.reset_game
        )
        self.advanced_toggle.pack()
        
        # Frames principales
        self.terms_frame = tk.Frame(self, bg="#F0F8FF")
        self.terms_frame.pack(pady=10)
        
        self.definitions_frame = tk.Frame(self, bg="#F0F8FF")
        self.definitions_frame.pack(pady=10)
        
        self.status_label = tk.Label(self, text="", font=("Arial", 14), bg="#F0F8FF")
        self.status_label.pack(pady=5)
        
        self.stats_label = tk.Label(self, text="", font=("Arial", 12), bg="#F0F8FF")
        self.stats_label.pack(pady=5)
    
    def reset_game(self):
        """Reinicia el juego con la configuración actual"""
        # Seleccionar términos según el modo
        if self.advanced_mode.get():
            self.unseen = advanced_terms.copy()
        else:
            self.unseen = basic_terms.copy()
        
        random.shuffle(self.unseen)
        self.current_set = []
        self.matched = {}
        self.term_buttons = []
        self.definition_buttons = []
        self.round_active = False
        self.error_count = 0
        self.correct_total = 0
        self.selected_term = None
        self.selected_definition = None
        
        # Limpiar widgets
        for widget in self.terms_frame.winfo_children():
            widget.destroy()
        for widget in self.definitions_frame.winfo_children():
            widget.destroy()
        
        self.status_label.config(text="")
        self.next_round()
    
    def update_stats(self):
        total_terms = len(advanced_terms) if self.advanced_mode.get() else len(basic_terms)
        self.stats_label.config(
            text=f"Progreso: {self.correct_total}/{total_terms} | Errores: {self.error_count}"
        )
    
    def next_round(self):
        self.matched = {}
        self.selected_term = None
        self.selected_definition = None

        for btn in self.term_buttons + self.definition_buttons:
            btn.destroy()

        self.term_buttons.clear()
        self.definition_buttons.clear()

        remaining = min(4, len(self.unseen))
        if remaining == 0:
            self.show_final_results()
            return

        self.current_set = [self.unseen.pop() for _ in range(remaining)]
        self.round_active = False
        self.animate_shuffle()
    
    def show_final_results(self):
        total_terms = len(advanced_terms) if self.advanced_mode.get() else len(basic_terms)
        percentage = (self.correct_total / total_terms) * 100
        
        if percentage >= 90:
            rank = "Analyst Ready 💼📊"
            color = "#2E8B57"
        elif percentage >= 70:
            rank = "Junior in Progress 📈"
            color = "#1E90FF"
        else:
            rank = "Need more practice 💼📚"
            color = "#CD5C5C"
        
        message = f"""¡Juego completado!
        
Puntuación final: {self.correct_total}/{total_terms} ({percentage:.1f}%)
Nivel alcanzado: {rank}"""
        
        messagebox.showinfo("Resultados Finales", message)
        self.status_label.config(text=f"Resultado: {rank}", fg=color)
        self.update_stats()
    
    def animate_shuffle(self):
        steps = 5
        delay = 150

        def do_shuffle(step):
            if step <= 0:
                self.show_cards()
                return
            random.shuffle(self.current_set)
            self.show_temp_terms()
            self.after(delay, lambda: do_shuffle(step - 1))

        do_shuffle(steps)
    
    def show_temp_terms(self):
        for btn in self.term_buttons:
            btn.destroy()
        self.term_buttons.clear()

        for i, (term, _) in enumerate(self.current_set):
            btn = tk.Button(self.terms_frame, text="?", font=("Arial", 16, "bold"),
                            width=18, height=2, bg="#4682B4", fg="white")
            btn.grid(row=0, column=i, padx=10)
            self.term_buttons.append(btn)
    
    def show_cards(self):
        self.round_active = True

        for btn in self.term_buttons + self.definition_buttons:
            btn.destroy()
        self.term_buttons.clear()
        self.definition_buttons.clear()

        # Mostrar términos financieros (inglés)
        for i, (term, _) in enumerate(self.current_set):
            btn = tk.Button(self.terms_frame, text=term, 
                           font=("Arial", 12 if len(term) > 15 else 14, "bold"),
                           width=18, height=2, bg="#FFFFFF", relief="ridge",
                           activebackground="#B0E0E6", wraplength=150)
            btn.grid(row=0, column=i, padx=10)
            btn.config(command=lambda b=btn, t=term: self.on_term_click(b, t))
            self.term_buttons.append(btn)

        # Mostrar definiciones (español)
        definitions = [defn for _, defn in self.current_set]
        random.shuffle(definitions)

        for i, definition in enumerate(definitions):
            btn = tk.Button(self.definitions_frame, text=definition, 
                           font=("Arial", 11 if len(definition) > 20 else 12),
                           width=18, height=2, bg="#F5F5F5", relief="groove",
                           activebackground="#B0E0E6", wraplength=150)
            btn.grid(row=0, column=i, padx=10)
            btn.config(command=lambda b=btn, d=definition: self.on_definition_click(b, d))
            self.definition_buttons.append(btn)

        self.update_stats()
    
    def on_term_click(self, button, term):
        if not self.round_active or term in self.matched:
            return

        self.reset_term_buttons()
        button.config(bg="#B0E0E6")
        self.selected_term = (button, term)
        self.validate_match()
    
    def on_definition_click(self, button, definition):
        if not self.round_active or definition in self.matched.values():
            return

        self.reset_definition_buttons()
        button.config(bg="#B0E0E6")
        self.selected_definition = (button, definition)
        self.validate_match()
    
    def reset_term_buttons(self):
        for btn in self.term_buttons:
            btn.config(bg="#FFFFFF")
    
    def reset_definition_buttons(self):
        for btn in self.definition_buttons:
            btn.config(bg="#F5F5F5")
    
    def validate_match(self):
        if self.selected_term and self.selected_definition:
            term_btn, term = self.selected_term
            def_btn, definition = self.selected_definition

            if financial_vocab.get(term) == definition:
                term_btn.config(bg="lightgreen", state="disabled")
                def_btn.config(bg="lightgreen", state="disabled")
                self.matched[term] = definition
                self.correct_total += 1
                self.status_label.config(text="✅ ¡Correcto!", fg="green")
            else:
                term_btn.config(bg="tomato")
                def_btn.config(bg="tomato")
                self.error_count += 1
                self.status_label.config(text="❌ Incorrecto, intenta de nuevo", fg="red")

            self.selected_term = None
            self.selected_definition = None
            self.update_stats()

            if len(self.matched) == len(self.current_set):
                self.round_active = False
                self.after(1200, self.next_round)

if __name__ == "__main__":
    app = FinancialVocabularyGame()
    app.mainloop()