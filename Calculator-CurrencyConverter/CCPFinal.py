"""
Vintage–Styled Financial Toolkit
Solution 1: **All interactive buttons converted to `ttk.Button`
             and `ttk.Menubutton` for full macOS compatibility"""
import tkinter as tk
from tkinter import ttk, font as tkFont
import math
import requests

# ------------ GLOBAL VINTAGE SETTINGS ---------------------------------------
HANDWRITTEN = "Comic Sans MS"
CREAM_BG    = "#FAF3E0"
PAPER_BG    = "#F5E6C4"
INK_DARK    = "#5B4636"

# --------------------------------------------------------------------------- #
#  PRIMARY WINDOW                                                             #
# --------------------------------------------------------------------------- #
class FinancialApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Python Multi-Tool – Vintage Edition")
        self.geometry("1000x600")
        self.configure(bg=CREAM_BG)

        # Fonts
        self.vintage_font = tkFont.Font(family=HANDWRITTEN, size=20, weight="bold")
        self.small_font   = tkFont.Font(family=HANDWRITTEN, size=14, weight="bold")

        # ttk styling (macOS-safe)
        style = ttk.Style(self)
        style.theme_use("clam")                         # cross-platform neutral theme
        style.configure(
            "Vintage.TButton",
            font=self.vintage_font,
            foreground="white",
            background="#8B5A2B",
            padding=(10, 4),
        )
        style.map(
            "Vintage.TButton",
            background=[("active", "#8B5A2B"), ("pressed", "#8B5A2B")],
            foreground=[("disabled", "#aaaaaa")],
        )

        style.configure(
            "Vintage.TMenubutton",
            font=self.small_font,
            foreground="white",
            background="#8B5A2B",
            padding=(10, 4),
        )

        # ENTRY & LABEL widget options (plain Tk widgets are fine)
        self.entry_opts = {
            "bg": "#FFF8DC",
            "fg": INK_DARK,
            "font": self.vintage_font,
            "bd": 2,
            "relief": tk.GROOVE,
            "insertbackground": INK_DARK,
        }
        self.label_opts = {
            "bg": PAPER_BG,
            "fg": INK_DARK,
            "font": self.vintage_font,
        }

        self._layout()

    # ----------------------------------------------------------------------- #
    def _layout(self):
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        left  = tk.Frame(self, bg=PAPER_BG, bd=3, relief=tk.GROOVE)
        right = tk.Frame(self, bg=PAPER_BG, bd=3, relief=tk.GROOVE)
        left.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        right.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)

        CalculatorFrame(left, self).pack(expand=True, fill="both", padx=10, pady=10)
        CurrencyConverterFrame(right, self).pack(expand=True, fill="both", padx=10, pady=10)


# --------------------------------------------------------------------------- #
#  CALCULATOR                                                                 #
# --------------------------------------------------------------------------- #
class CalculatorFrame(tk.Frame):
    def __init__(self, parent, app: FinancialApp):
        super().__init__(parent, bg=PAPER_BG)
        self.app         = app
        self.expression  = ""
        self.current_tab = tk.StringVar(value="Simple Interest")
        self.mode        = tk.StringVar(value="Basic")
        self._header()
        self.container = tk.Frame(self, bg=PAPER_BG)
        self.container.pack(expand=True, fill="both", padx=10, pady=10)
        self._build_ui()

    # ----------------------------------------------------------------------- #
    def _header(self):
        bar = tk.Frame(self, bg=PAPER_BG)
        bar.pack(pady=10)

        tk.Label(bar, text="Calculator Type:", **self.app.label_opts).pack(side="left")

        menu_btn = ttk.Menubutton(
            bar,
            textvariable=self.mode,
            style="Vintage.TMenubutton",
            direction="below",
        )
        menu_btn.pack(side="left", padx=15)

        menu = tk.Menu(menu_btn, tearoff=0, bg="#8B5A2B", fg="white",
                       activebackground="#8B5A2B", activeforeground="white",
                       font=self.app.vintage_font)
        for m in ("Basic", "Scientific", "Financial"):
            menu.add_command(label=m, command=lambda v=m: self._switch_mode(v))
        menu_btn["menu"] = menu

    def _switch_mode(self, new_mode):
        self.mode.set(new_mode)
        self._build_ui()

    # ----------------------------------------------------------------------- #
    def _build_ui(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        self.expression = ""
        if self.mode.get() == "Financial":
            frame = self._financial_ui()
        else:
            frame = self._standard_ui(self.mode.get())
        frame.pack(expand=True, fill="both")

    # ----------  BASIC / SCIENTIFIC ---------------------------------------- #
    def _standard_ui(self, mode):
        frame = tk.Frame(self.container, bg=PAPER_BG)
        self.display_var = tk.StringVar()
        tk.Entry(
            frame,
            textvariable=self.display_var,
            state="readonly",
            justify="right",
            readonlybackground="#FFF8DC",
            fg=INK_DARK,
            font=self.app.vintage_font,
            bd=3,
            relief=tk.SUNKEN,
        ).grid(row=0, column=0, columnspan=5, sticky="nsew", pady=(0, 10), ipady=5)

        layouts = {
            "Basic": [
                ("7", "8", "9", "/"),
                ("4", "5", "6", "*"),
                ("1", "2", "3", "-"),
                ("0", ".", "=", "+"),
                ("Clear",),
            ],
            "Scientific": [
                ("sin", "cos", "tan", "^", "sqrt"),
                ("log", "ln", "(", ")", "π"),
                ("7", "8", "9", "/", "C"),
                ("4", "5", "6", "*"),
                ("1", "2", "3", "-"),
                ("0", ".", "=", "+"),
            ],
        }

        grid = layouts[mode]
        for r, row in enumerate(grid, 1):
            for c, char in enumerate(row):
                span = 4 if char in ("Clear", "C") and mode == "Basic" else 1
                ttk.Button(
                    frame,
                    text=char,
                    style="Vintage.TButton",
                    command=lambda ch=char: self._press(ch),
                ).grid(row=r, column=c, columnspan=span, sticky="nsew", padx=2, pady=2)

        cols = 5 if mode == "Scientific" else 4
        for i in range(cols):
            frame.grid_columnconfigure(i, weight=1)
        for i in range(len(grid) + 1):
            frame.grid_rowconfigure(i, weight=1)
        return frame

    def _press(self, char):
        if char in ("Clear", "C"):
            self.expression = ""
        elif char == "=":
            try:
                exp = (
                    self.expression.replace("^", "**").replace("π", str(math.pi))
                )
                for old, new in {
                    "sqrt": "math.sqrt",
                    "sin": "math.sin",
                    "cos": "math.cos",
                    "tan": "math.tan",
                    "log": "math.log10",
                    "ln": "math.log",
                }.items():
                    exp = exp.replace(f"{old}(", f"{new}(")
                self.expression = str(eval(exp, {"__builtins__": None, "math": math}))
            except Exception:
                self.expression = "Error"
        elif char in ("sin", "cos", "tan", "log", "ln", "sqrt"):
            self.expression += f"{char}("
        else:
            if self.expression == "Error":
                self.expression = ""
            self.expression += char
        self.display_var.set(self.expression)

    # ----------  FINANCIAL -------------------------------------------------- #
    def _financial_ui(self):
        frame = tk.Frame(self.container, bg=PAPER_BG)

        # Tabs
        tab_bar = tk.Frame(frame, bg=PAPER_BG)
        tab_bar.pack(fill="x", pady=(0, 10))
        for tab in ("Simple Interest", "Compound Interest", "Loan Calculator"):
            ttk.Button(
                tab_bar,
                text=tab,
                style=("Vintage.TButton" if tab == self.current_tab.get() else "Vintage.TButton"),
                command=lambda t=tab: self._switch_tab(t),
            ).pack(side="left", expand=True, fill="x", padx=2)

        self.content = tk.Frame(frame, bg=PAPER_BG)
        self.content.pack(expand=True, fill="both")
        self._load_financial_tab()
        return frame

    def _switch_tab(self, tab):
        self.current_tab.set(tab)
        self._build_ui()

    def _load_financial_tab(self):
        tab = self.current_tab.get()
        if tab in ("Simple Interest", "Compound Interest"):
            self._interest_ui(tab)
        else:
            self._loan_ui()

    # ----------  Simple / Compound ----------------------------------------- #
    def _interest_ui(self, calc_type):
        fields = ("Principal", "Rate % per year", "Time years")
        self.entries = {}
        for row, field in enumerate(fields):
            tk.Label(self.content, text=f"{field}:", **self.app.label_opts).grid(
                row=row, column=0, sticky="e", padx=10, pady=5
            )
            e = tk.Entry(self.content, **self.app.entry_opts, width=15)
            e.grid(row=row, column=1, sticky="w", padx=10, pady=5)
            self.entries[field] = e

        if calc_type == "Compound Interest":
            tk.Label(self.content, text="Compounds/year:", **self.app.label_opts).grid(
                row=3, column=0, sticky="e", padx=10, pady=5
            )
            e = tk.Entry(self.content, **self.app.entry_opts, width=15)
            e.grid(row=3, column=1, sticky="w", padx=10, pady=5)
            self.entries["Compounds"] = e

        ttk.Button(
            self.content,
            text="Calculate",
            style="Vintage.TButton",
            command=lambda: self._calc_interest(calc_type),
        ).grid(row=4, column=0, columnspan=2, sticky="ew", pady=10, padx=20)

        self.result_lbl = tk.Label(
            self.content, text="", **self.app.label_opts, wraplength=400
        )
        self.result_lbl.grid(row=5, column=0, columnspan=2, pady=20)

        for i in range(2):
            self.content.grid_columnconfigure(i, weight=1)

    def _calc_interest(self, calc_type):
        try:
            P = float(self.entries["Principal"].get())
            R = float(self.entries["Rate % per year"].get()) / 100
            T = float(self.entries["Time years"].get())
            if calc_type == "Simple Interest":
                si = P * R * T
                self.result_lbl.config(
                    text=f"Simple Interest: ${si:.2f}\nTotal Amount: ${P+si:.2f}",
                    fg=INK_DARK,
                )
            else:
                n = int(self.entries["Compounds"].get())
                amount = P * (1 + R / n) ** (n * T)
                self.result_lbl.config(
                    text=f"Compound Interest: ${amount-P:.2f}\nTotal Amount: ${amount:.2f}",
                    fg=INK_DARK,
                )
        except Exception:
            self.result_lbl.config(text="Error: Enter valid numbers", fg="red")

    # ----------  Loan EMI --------------------------------------------------- #
    def _loan_ui(self):
        fields = ("Loan Amount", "Rate % per year", "Term years")
        self.entries = {}
        for r, field in enumerate(fields):
            tk.Label(self.content, text=f"{field}:", **self.app.label_opts).grid(
                row=r, column=0, sticky="e", padx=10, pady=5
            )
            e = tk.Entry(self.content, **self.app.entry_opts, width=15)
            e.grid(row=r, column=1, sticky="w", padx=10, pady=5)
            self.entries[field] = e

        ttk.Button(
            self.content,
            text="Calculate EMI",
            style="Vintage.TButton",
            command=self._calc_loan,
        ).grid(row=3, column=0, columnspan=2, sticky="ew", pady=10, padx=20)

        self.result_lbl = tk.Label(self.content, text="", **self.app.label_opts)
        self.result_lbl.grid(row=4, column=0, columnspan=2, pady=20)

        for i in range(2):
            self.content.grid_columnconfigure(i, weight=1)

    def _calc_loan(self):
        try:
            P = float(self.entries["Loan Amount"].get())
            annual_rate = float(self.entries["Rate % per year"].get())
            years = int(self.entries["Term years"].get())
            r = (annual_rate / 100) / 12
            n = years * 12
            emi = P / n if r == 0 else P * (r * (1 + r) ** n) / ((1 + r) ** n - 1)
            self.result_lbl.config(text=f"Monthly EMI: ${emi:.2f}", fg=INK_DARK)
        except Exception:
            self.result_lbl.config(text="Error: Enter valid numbers", fg="red")


# --------------------------------------------------------------------------- #
#  CURRENCY CONVERTER                                                         #
# --------------------------------------------------------------------------- #
class CurrencyConverterFrame(tk.Frame):
    def __init__(self, parent, app: FinancialApp):
        super().__init__(parent, bg=PAPER_BG)
        self.app = app
        self.api_url = "https://api.exchangerate-api.com/v4/latest/"
        self.rates = {}
        self.currencies = sorted(
            [
                "USD", "EUR", "JPY", "GBP", "AUD", "CAD", "CHF", "CNY",
                "INR", "BRL", "RUB", "ZAR", "SGD", "NZD", "MXN", "KRW",
            ]
        )
        self._widgets()
        self._update_rates()

    # ----------------------------------------------------------------------- #
    def _widgets(self):
        tk.Label(self, text="Currency Converter", **self.app.label_opts).pack(pady=10)

        # Amount
        amt_frame = tk.Frame(self, bg=PAPER_BG)
        amt_frame.pack(pady=10, fill="x")
        tk.Label(amt_frame, text="Amount:", **self.app.label_opts).pack(side="left")
        self.amount_entry = tk.Entry(amt_frame, **self.app.entry_opts, width=12)
        self.amount_entry.pack(side="left", padx=10)

        # From currency
        self.from_var = tk.StringVar(value="USD")
        from_frame = tk.Frame(self, bg=PAPER_BG)
        from_frame.pack(pady=5, fill="x")
        tk.Label(from_frame, text="From:", **self.app.label_opts).pack(side="left")
        self.from_btn = ttk.Menubutton(
            from_frame,
            textvariable=self.from_var,
            style="Vintage.TMenubutton",
            direction="below",
        )
        self.from_btn.pack(side="left", padx=10)

        from_menu = tk.Menu(self.from_btn, tearoff=0, bg="#8B5A2B", fg="white",
                            activebackground="#8B5A2B", activeforeground="white",
                            font=self.app.vintage_font)
        for cur in self.currencies:
            from_menu.add_command(label=cur, command=lambda c=cur: self._set_from(c))
        self.from_btn["menu"] = from_menu

        # To currency
        self.to_var = tk.StringVar(value="INR")
        to_frame = tk.Frame(self, bg=PAPER_BG)
        to_frame.pack(pady=5, fill="x")
        tk.Label(to_frame, text="To:", **self.app.label_opts).pack(side="left")
        self.to_btn = ttk.Menubutton(
            to_frame,
            textvariable=self.to_var,
            style="Vintage.TMenubutton",
            direction="below",
        )
        self.to_btn.pack(side="left", padx=10)

        to_menu = tk.Menu(self.to_btn, tearoff=0, bg="#8B5A2B", fg="white",
                          activebackground="#8B5A2B", activeforeground="white",
                          font=self.app.vintage_font)
        for cur in self.currencies:
            to_menu.add_command(label=cur, command=lambda c=cur: self._set_to(c))
        self.to_btn["menu"] = to_menu

        # Action buttons
        ttk.Button(
            self,
            text="Convert",
            style="Vintage.TButton",
            command=self._convert,
        ).pack(fill="x", padx=20, pady=(20, 10))
        ttk.Button(
            self,
            text="Update Rates",
            style="Vintage.TButton",
            command=lambda: self._update_rates(show_msg=True),
        ).pack(fill="x", padx=20, pady=(0, 20))

        self.result_lbl  = tk.Label(self, text="", **self.app.label_opts)
        self.result_lbl.pack(pady=10)
        self.update_msg  = tk.Label(self, text="", bg=PAPER_BG,
                                    fg="#008000", font=self.app.small_font,
                                    wraplength=300)
        self.update_msg.pack(pady=5)
        self.status_lbl  = tk.Label(self, text="Fetching rates…", bg=PAPER_BG,
                                    fg=INK_DARK, font=self.app.small_font)
        self.status_lbl.pack(side="bottom", fill="x", pady=5)

    # ----------------------------------------------------------------------- #
    def _set_from(self, currency):
        self.from_var.set(currency)
        self._update_rates()

    def _set_to(self, currency):
        self.to_var.set(currency)

    # ----------------------------------------------------------------------- #
    def _update_rates(self, show_msg=False):
        base = self.from_var.get()
        self.status_lbl.config(text=f"Updating rates for {base}…")
        if show_msg:
            self.update_msg.config(text="")
        self.update_idletasks()
        try:
            data = requests.get(f"{self.api_url}{base}", timeout=10).json()
            self.rates = data.get("rates", {})
            self.status_lbl.config(text=f"Rates updated: {data.get('date', '')}")
            if show_msg:
                self.update_msg.config(text=f"✓ Updated rates for {base}!", fg="#008000")
                self.after(5000, lambda: self.update_msg.config(text=""))
        except Exception:
            self.status_lbl.config(text="Error updating rates")
            if show_msg:
                self.update_msg.config(text="✗ Failed to update rates", fg="#FF0000")

    # ----------------------------------------------------------------------- #
    def _convert(self):
        try:
            amount = float(self.amount_entry.get())
            rate   = self.rates.get(self.to_var.get())
            if rate is None:
                raise ValueError("Rate missing")
            result = amount * rate
            self.result_lbl.config(
                text=f"{amount:.2f} {self.from_var.get()} = {result:.2f} {self.to_var.get()}",
                fg=INK_DARK,
            )
        except Exception:
            self.result_lbl.config(text="Error: Check amount/rates", fg="red")


# --------------------------------------------------------------------------- #
#  MAIN LOOP                                                                  #
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    FinancialApp().mainloop()
