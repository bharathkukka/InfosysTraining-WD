
import tkinter as tk
from tkinter import font as tkFont
import math
import requests

# ------------ ENHANCED VINTAGE COLOR PALETTE --------------------------------
HANDWRITTEN = "Comic Sans MS"
CREAM_BG = "#FAF3E0"  # Main background
PAPER_BG = "#F5E6C4"  # Frame backgrounds
INK_DARK = "#3C2E26"  # Dark text (darker for better contrast)
BUTTON_BG = "#8B4513"  # Saddle brown (darker for better contrast)
BUTTON_HOVER = "#A0522D"  # Sienna (lighter brown for hover)
BUTTON_TEXT = "#FFFBF0"  # Ivory (better contrast than previous)
ENTRY_BG = "#FFF8DC"  # Cornsilk
ERROR_COLOR = "#B22222"  # Fire brick red
SUCCESS_COLOR = "#228B22"  # Forest green


class FinancialApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Python Multi-Tool - Vintage Edition")
        self.geometry("1000x600")
        self.configure(bg=CREAM_BG)

        # Create consistent fonts
        self.vintage_font = tkFont.Font(family=HANDWRITTEN, size=20, weight="bold")
        self.small_font = tkFont.Font(family=HANDWRITTEN, size=14, weight="bold")

        # Enhanced button style with stable colors for macOS
        self.button_style = {
            "bg": BUTTON_BG,
            "fg": BUTTON_TEXT,
            "activebackground": BUTTON_BG,  # Same as normal bg
            "activeforeground": BUTTON_TEXT,  # Same as normal fg
            "font": self.vintage_font,
            "bd": 3,  # Slightly thicker border
            "relief": tk.RAISED,
            "cursor": "hand2",
            "highlightthickness": 0,  # Remove focus highlight
            "borderwidth": 3,
            "padx": 5,
            "pady": 3,
        }

        # Menubutton style (for dropdowns)
        self.menubutton_style = {
            "bg": BUTTON_BG,
            "fg": BUTTON_TEXT,
            "activebackground": BUTTON_BG,
            "activeforeground": BUTTON_TEXT,
            "font": self.vintage_font,
            "bd": 3,
            "relief": tk.RAISED,
            "cursor": "hand2",
            "highlightthickness": 0,
            "borderwidth": 3,
            "padx": 5,
            "pady": 3,
        }

        # Entry style
        self.entry_style = {
            "bg": ENTRY_BG,
            "fg": INK_DARK,
            "font": self.vintage_font,
            "bd": 2,
            "relief": tk.GROOVE,
            "insertbackground": INK_DARK,
            "selectbackground": BUTTON_BG,
            "selectforeground": BUTTON_TEXT,
        }

        # Label style
        self.label_style = {"bg": PAPER_BG, "fg": INK_DARK, "font": self.vintage_font}

        self.setup_layout()

    def create_stable_button(self, parent, text, command=None, **kwargs):
        """Create a button with stable colors that don't change on interaction"""
        # Merge with default button style
        button_config = {**self.button_style, **kwargs}

        btn = tk.Button(parent, text=text, command=command, **button_config)

        # Bind hover effects manually for better control
        def on_enter(e):
            btn.config(bg=BUTTON_HOVER, activebackground=BUTTON_HOVER)

        def on_leave(e):
            btn.config(
                bg=button_config.get("bg", BUTTON_BG),
                activebackground=button_config.get("bg", BUTTON_BG),
            )

        def on_press(e):
            btn.config(relief=tk.SUNKEN)

        def on_release(e):
            btn.config(relief=tk.RAISED)

        # Bind events for consistent behavior
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        btn.bind("<Button-1>", on_press)
        btn.bind("<ButtonRelease-1>", on_release)

        return btn

    def create_stable_menubutton(self, parent, text, **kwargs):
        """Create a menubutton with stable colors"""
        # Merge with default menubutton style
        menubutton_config = {**self.menubutton_style, **kwargs}

        btn = tk.Menubutton(parent, text=text, **menubutton_config)

        # Bind hover effects
        def on_enter(e):
            btn.config(bg=BUTTON_HOVER, activebackground=BUTTON_HOVER)

        def on_leave(e):
            btn.config(
                bg=menubutton_config.get("bg", BUTTON_BG),
                activebackground=menubutton_config.get("bg", BUTTON_BG),
            )

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

        return btn

    def setup_layout(self):
        # Main layout
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Left frame for calculator
        left_frame = tk.Frame(self, bg=PAPER_BG, bd=3, relief=tk.GROOVE)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)

        # Right frame for currency converter
        right_frame = tk.Frame(self, bg=PAPER_BG, bd=3, relief=tk.GROOVE)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)

        # Add components
        self.calculator = CalculatorFrame(left_frame, self)
        self.calculator.pack(expand=True, fill="both", padx=10, pady=10)

        self.converter = CurrencyConverterFrame(right_frame, self)
        self.converter.pack(expand=True, fill="both", padx=10, pady=10)


class CalculatorFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=PAPER_BG)
        self.app = app
        self.expression = ""
        self.current_frame = None

        self.create_header()
        self.container = tk.Frame(self, bg=PAPER_BG)
        self.container.pack(expand=True, fill="both", padx=10, pady=10)
        self.build_ui()

    def create_header(self):
        header = tk.Frame(self, bg=PAPER_BG)
        header.pack(pady=10)

        tk.Label(header, text="Calculator Type:", **self.app.label_style).pack(
            side="left"
        )

        self.mode = tk.StringVar(value="Basic")

        # Use stable menubutton (FIXED!)
        self.mode_button = self.app.create_stable_menubutton(header, "Basic")
        self.mode_button.pack(side="left", padx=15)

        mode_menu = tk.Menu(
            self.mode_button,
            tearoff=0,
            bg=BUTTON_BG,
            fg=BUTTON_TEXT,
            activebackground=BUTTON_HOVER,
            activeforeground=BUTTON_TEXT,
            font=self.app.vintage_font,
            bd=2,
        )

        for mode in ["Basic", "Scientific", "Financial"]:
            mode_menu.add_command(
                label=mode, command=lambda m=mode: self.change_mode(m)
            )

        self.mode_button.config(menu=mode_menu)  # Now this works!

    def change_mode(self, new_mode):
        self.mode.set(new_mode)
        self.mode_button.config(text=new_mode)
        self.build_ui()

    def build_ui(self):
        if self.current_frame:
            self.current_frame.destroy()

        mode = self.mode.get()
        self.expression = ""

        if mode == "Financial":
            self.current_frame = self.create_financial_ui()
        else:
            self.current_frame = self.create_standard_ui(mode)

        self.current_frame.pack(expand=True, fill="both")

    def create_standard_ui(self, mode):
        frame = tk.Frame(self.container, bg=PAPER_BG)

        # Display with better contrast
        self.display_var = tk.StringVar()
        display = tk.Entry(
            frame,
            textvariable=self.display_var,
            state="readonly",
            justify="right",
            readonlybackground=ENTRY_BG,
            fg=INK_DARK,
            font=self.app.vintage_font,
            bd=3,
            relief=tk.SUNKEN,
            highlightthickness=0,
        )
        display.grid(
            row=0, column=0, columnspan=5, sticky="nsew", pady=(0, 10), ipady=8
        )

        # Button layouts
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

        layout = layouts[mode]

        for r, row in enumerate(layout, 1):
            for c, char in enumerate(row):
                colspan = 4 if char == "Clear" and mode == "Basic" else 1

                # Use the stable button creation method
                btn = self.app.create_stable_button(
                    frame, char, command=lambda ch=char: self.button_press(ch)
                )
                btn.grid(
                    row=r,
                    column=c,
                    columnspan=colspan,
                    sticky="nsew",
                    padx=2,
                    pady=2,
                    ipadx=5,
                    ipady=5,
                )

        # Configure grid
        cols = 5 if mode == "Scientific" else 4
        for i in range(cols):
            frame.grid_columnconfigure(i, weight=1)
        for i in range(len(layout) + 1):
            frame.grid_rowconfigure(i, weight=1)

        return frame

    def button_press(self, char):
        if char in ("Clear", "C"):
            self.expression = ""
        elif char == "=":
            try:
                exp = self.expression.replace("^", "**").replace("π", str(math.pi))
                for old, new in {
                    "sqrt": "math.sqrt",
                    "sin": "math.sin",
                    "cos": "math.cos",
                    "tan": "math.tan",
                    "log": "math.log10",
                    "ln": "math.log",
                }.items():
                    exp = exp.replace(f"{old}(", f"{new}(")
                self.expression = str(eval(exp, {"__builtins__": None}, {"math": math}))
            except:
                self.expression = "Error"
        elif char in ("sin", "cos", "tan", "log", "ln", "sqrt"):
            self.expression += f"{char}("
        else:
            if self.expression == "Error":
                self.expression = ""
            self.expression += char

        self.display_var.set(self.expression)

    def create_financial_ui(self):
        frame = tk.Frame(self.container, bg=PAPER_BG)

        # Create tab buttons
        tab_frame = tk.Frame(frame, bg=PAPER_BG)
        tab_frame.pack(fill="x", pady=(0, 10))

        self.current_tab = tk.StringVar(value="Simple Interest")
        tabs = ["Simple Interest", "Compound Interest", "Loan Calculator"]

        self.tab_buttons = []
        for tab in tabs:
            # Use stable button with special styling for tabs
            is_active = tab == self.current_tab.get()
            btn = self.app.create_stable_button(
                tab_frame,
                tab,
                command=lambda t=tab: self.switch_tab(t),
                bg=BUTTON_BG if is_active else PAPER_BG,
                fg=BUTTON_TEXT if is_active else INK_DARK,
                activebackground=BUTTON_BG if is_active else PAPER_BG,
                activeforeground=BUTTON_TEXT if is_active else INK_DARK,
                font=self.app.small_font,
            )
            btn.pack(side="left", padx=2, fill="x", expand=True)
            self.tab_buttons.append((btn, tab))

        # Content area
        self.content_frame = tk.Frame(frame, bg=PAPER_BG)
        self.content_frame.pack(expand=True, fill="both")

        self.load_tab_content()
        return frame

    def switch_tab(self, tab):
        self.current_tab.set(tab)

        # Update tab button styles
        for btn, tab_name in self.tab_buttons:
            is_active = tab_name == tab
            btn.config(
                bg=BUTTON_BG if is_active else PAPER_BG,
                fg=BUTTON_TEXT if is_active else INK_DARK,
                activebackground=BUTTON_BG if is_active else PAPER_BG,
                activeforeground=BUTTON_TEXT if is_active else INK_DARK,
            )

        # Clear and reload content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.load_tab_content()

    def load_tab_content(self):
        tab = self.current_tab.get()

        if tab in ["Simple Interest", "Compound Interest"]:
            self.create_interest_tab(tab)
        else:
            self.create_loan_tab()

    def create_interest_tab(self, tab_type):
        fields = ["Principal", "Rate % per year", "Time years"]
        self.entries = {}

        for i, field in enumerate(fields):
            tk.Label(self.content_frame, text=f"{field}:", **self.app.label_style).grid(
                row=i, column=0, sticky="e", padx=10, pady=5
            )
            entry = tk.Entry(self.content_frame, **self.app.entry_style, width=15)
            entry.grid(row=i, column=1, sticky="w", padx=10, pady=5)
            self.entries[field] = entry

        if tab_type == "Compound Interest":
            tk.Label(
                self.content_frame, text="Compounds/year:", **self.app.label_style
            ).grid(row=3, column=0, sticky="e", padx=10, pady=5)
            entry = tk.Entry(self.content_frame, **self.app.entry_style, width=15)
            entry.grid(row=3, column=1, sticky="w", padx=10, pady=5)
            self.entries["Compounds"] = entry

        self.result_label = tk.Label(
            self.content_frame, text="", **self.app.label_style, wraplength=400
        )
        self.result_label.grid(row=5, column=0, columnspan=2, pady=20)

        # Use stable button
        calc_btn = self.app.create_stable_button(
            self.content_frame,
            "Calculate",
            command=lambda: self.calculate_interest(tab_type),
        )
        calc_btn.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")

        for i in range(2):
            self.content_frame.grid_columnconfigure(i, weight=1)

    def calculate_interest(self, calc_type):
        try:
            P = float(self.entries["Principal"].get())
            R = float(self.entries["Rate % per year"].get()) / 100
            T = float(self.entries["Time years"].get())

            if calc_type == "Simple Interest":
                si = P * R * T
                total = P + si
                self.result_label.config(
                    text=f"Simple Interest: ${si:.2f}\nTotal Amount: ${total:.2f}",
                    fg=SUCCESS_COLOR,
                )
            else:
                n = int(self.entries["Compounds"].get())
                amount = P * (1 + R / n) ** (n * T)
                ci = amount - P
                self.result_label.config(
                    text=f"Compound Interest: ${ci:.2f}\nTotal Amount: ${amount:.2f}",
                    fg=SUCCESS_COLOR,
                )
        except:
            self.result_label.config(
                text="Error: Please enter valid numbers", fg=ERROR_COLOR
            )

    def create_loan_tab(self):
        fields = ["Loan Amount", "Rate % per year", "Term years"]
        self.entries = {}

        for i, field in enumerate(fields):
            tk.Label(self.content_frame, text=f"{field}:", **self.app.label_style).grid(
                row=i, column=0, sticky="e", padx=10, pady=5
            )
            entry = tk.Entry(self.content_frame, **self.app.entry_style, width=15)
            entry.grid(row=i, column=1, sticky="w", padx=10, pady=5)
            self.entries[field] = entry

        self.result_label = tk.Label(
            self.content_frame, text="", **self.app.label_style
        )
        self.result_label.grid(row=4, column=0, columnspan=2, pady=20)

        # Use stable button
        calc_btn = self.app.create_stable_button(
            self.content_frame, "Calculate EMI", command=self.calculate_loan
        )
        calc_btn.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

        for i in range(2):
            self.content_frame.grid_columnconfigure(i, weight=1)

    def calculate_loan(self):
        try:
            P = float(self.entries["Loan Amount"].get())
            annual_rate = float(self.entries["Rate % per year"].get())
            term_years = int(self.entries["Term years"].get())

            r = (annual_rate / 100) / 12
            n = term_years * 12

            if r == 0:
                emi = P / n
            else:
                emi = P * (r * (1 + r) ** n) / ((1 + r) ** n - 1)

            self.result_label.config(text=f"Monthly EMI: ${emi:.2f}", fg=SUCCESS_COLOR)
        except:
            self.result_label.config(
                text="Error: Please enter valid numbers", fg=ERROR_COLOR
            )


class CurrencyConverterFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=PAPER_BG)
        self.app = app
        self.api_url = "https://api.exchangerate-api.com/v4/latest/"
        self.rates = {}
        self.currencies = sorted(
            [
                "USD",
                "EUR",
                "JPY",
                "GBP",
                "AUD",
                "CAD",
                "CHF",
                "CNY",
                "INR",
                "BRL",
                "RUB",
                "ZAR",
                "SGD",
                "NZD",
                "MXN",
                "KRW",
                "NOK",
                "SEK",
                "DKK",
                "PLN",
                "HUF",
                "CZK",
                "ILS",
                "PHP",
                "THB",
                "MYR",
                "IDR",
                "HKD",
                "ISK",
                "HRK",
                "BGN",
                "RON",
                "TRY",
            ]
        )
        self.create_widgets()
        self.update_rates()

    def create_widgets(self):
        # Title
        tk.Label(self, text="Currency Converter", **self.app.label_style).pack(pady=10)

        # Amount input
        amount_frame = tk.Frame(self, bg=PAPER_BG)
        amount_frame.pack(pady=10, fill="x")
        tk.Label(amount_frame, text="Amount:", **self.app.label_style).pack(side="left")
        self.amount_entry = tk.Entry(amount_frame, **self.app.entry_style, width=12)
        self.amount_entry.pack(side="left", padx=10)

        # From currency (FIXED to use menubutton)
        from_frame = tk.Frame(self, bg=PAPER_BG)
        from_frame.pack(pady=5, fill="x")
        tk.Label(from_frame, text="From:", **self.app.label_style).pack(side="left")

        self.from_var = tk.StringVar(value="USD")
        self.from_button = self.app.create_stable_menubutton(from_frame, "USD")
        self.from_button.pack(side="left", padx=10)

        from_menu = tk.Menu(
            self.from_button,
            tearoff=0,
            bg=BUTTON_BG,
            fg=BUTTON_TEXT,
            activebackground=BUTTON_HOVER,
            activeforeground=BUTTON_TEXT,
            font=self.app.vintage_font,
            bd=2,
        )

        for currency in self.currencies:
            from_menu.add_command(
                label=currency, command=lambda c=currency: self.change_from_currency(c)
            )

        self.from_button.config(menu=from_menu)

        # To currency (FIXED to use menubutton)
        to_frame = tk.Frame(self, bg=PAPER_BG)
        to_frame.pack(pady=5, fill="x")
        tk.Label(to_frame, text="To:", **self.app.label_style).pack(side="left")

        self.to_var = tk.StringVar(value="INR")
        self.to_button = self.app.create_stable_menubutton(to_frame, "INR")
        self.to_button.pack(side="left", padx=10)

        to_menu = tk.Menu(
            self.to_button,
            tearoff=0,
            bg=BUTTON_BG,
            fg=BUTTON_TEXT,
            activebackground=BUTTON_HOVER,
            activeforeground=BUTTON_TEXT,
            font=self.app.vintage_font,
            bd=2,
        )

        for currency in self.currencies:
            to_menu.add_command(
                label=currency, command=lambda c=currency: self.change_to_currency(c)
            )

        self.to_button.config(menu=to_menu)

        # Convert button
        convert_btn = self.app.create_stable_button(
            self, "Convert", command=self.convert
        )
        convert_btn.pack(fill="x", padx=20, pady=(20, 10))

        # Update Rates button
        update_btn = self.app.create_stable_button(
            self, "Update Rates", command=self.manual_update_rates
        )
        update_btn.pack(fill="x", padx=20, pady=(0, 20))

        # Result display
        self.result_label = tk.Label(self, text="", **self.app.label_style)
        self.result_label.pack(pady=10)

        # Update message display
        self.update_message = tk.Label(
            self,
            text="",
            bg=PAPER_BG,
            fg=SUCCESS_COLOR,
            font=self.app.small_font,
            wraplength=300,
        )
        self.update_message.pack(pady=5)

        # Status display
        self.status_label = tk.Label(
            self,
            text="Fetching rates...",
            bg=PAPER_BG,
            fg=INK_DARK,
            font=self.app.small_font,
        )
        self.status_label.pack(side="bottom", fill="x", pady=5)

    def change_from_currency(self, currency):
        self.from_var.set(currency)
        self.from_button.config(text=currency)
        self.update_rates()

    def change_to_currency(self, currency):
        self.to_var.set(currency)
        self.to_button.config(text=currency)

    def update_rates(self, show_message=False):
        base = self.from_var.get()
        self.status_label.config(text=f"Updating rates for {base}...")

        if show_message:
            self.update_message.config(text="")

        self.update_idletasks()

        try:
            response = requests.get(f"{self.api_url}{base}")
            response.raise_for_status()
            data = response.json()
            self.rates = data.get("rates", {})

            self.status_label.config(
                text=f"Rates updated: {data.get('date', 'Unknown date')}"
            )

            if show_message:
                rate_count = len(self.rates)
                self.update_message.config(
                    text=f"✓ Successfully updated {rate_count} exchange rates for {base}!",
                    fg=SUCCESS_COLOR,
                )
                self.after(5000, lambda: self.update_message.config(text=""))

        except requests.exceptions.RequestException:
            self.status_label.config(
                text="Error: Network issue - Could not fetch rates"
            )
            if show_message:
                self.update_message.config(
                    text="✗ Failed to update rates. Please check your internet connection.",
                    fg=ERROR_COLOR,
                )
        except Exception:
            self.status_label.config(text="Error: Could not fetch rates")
            if show_message:
                self.update_message.config(
                    text="✗ An error occurred while updating rates. Please try again.",
                    fg=ERROR_COLOR,
                )

    def manual_update_rates(self):
        self.update_rates(show_message=True)

    def convert(self):
        try:
            amount = float(self.amount_entry.get())
            from_curr = self.from_var.get()
            to_curr = self.to_var.get()

            if not self.rates:
                self.result_label.config(
                    text="Error: No rates available", fg=ERROR_COLOR
                )
                return

            rate = self.rates.get(to_curr)
            if rate is None:
                self.result_label.config(text="Error: Rate not found", fg=ERROR_COLOR)
                return

            converted = amount * rate
            self.result_label.config(
                text=f"{amount:.2f} {from_curr} = {converted:.2f} {to_curr}",
                fg=SUCCESS_COLOR,
            )

        except ValueError:
            self.result_label.config(
                text="Error: Please enter a valid amount", fg=ERROR_COLOR
            )
        except:
            self.result_label.config(text="Error: Conversion failed", fg=ERROR_COLOR)


if __name__ == "__main__":
    app = FinancialApp()
    app.mainloop()
