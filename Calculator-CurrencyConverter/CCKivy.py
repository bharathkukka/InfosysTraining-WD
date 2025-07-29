kivy_app_code = '''"""
Vintage-Styled Financial Toolkit - Kivy Version
Converted from tkinter to Kivy for cross-platform compatibility
"""
import math
import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.core.window import Window

# Global vintage color settings
CREAM_BG = (0.98, 0.95, 0.88, 1)      # #FAF3E0
PAPER_BG = (0.96, 0.90, 0.77, 1)      # #F5E6C4  
INK_DARK = (0.36, 0.27, 0.21, 1)      # #5B4636
BUTTON_BG = (0.55, 0.35, 0.17, 1)     # #8B5A2B
INPUT_BG = (1.0, 0.97, 0.86, 1)       # #FFF8DC

class FinancialApp(App):
    def build(self):
        self.title = "Python Multi-Tool – Vintage Edition"
        # Set initial window size (will be responsive)
        Window.size = (800, 600)
        Window.clearcolor = CREAM_BG

        # Create main layout
        main_layout = BoxLayout(orientation='horizontal', padding=dp(15), spacing=dp(15))

        # Create left and right panels
        left_panel = BoxLayout(orientation='vertical', size_hint=(0.5, 1))
        right_panel = BoxLayout(orientation='vertical', size_hint=(0.5, 1))

        # Add calculator and currency converter
        self.calculator = CalculatorWidget()
        self.currency_converter = CurrencyConverterWidget()

        left_panel.add_widget(self.calculator)
        right_panel.add_widget(self.currency_converter)

        main_layout.add_widget(left_panel)
        main_layout.add_widget(right_panel)

        return main_layout

class VintageButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = BUTTON_BG
        self.color = (1, 1, 1, 1)  # White text
        self.font_size = sp(16)
        self.font_name = 'Roboto'  # Fallback font
        self.bold = True

class VintageLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = INK_DARK
        self.font_size = sp(16)
        self.font_name = 'Roboto'
        self.bold = True

class VintageTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = INPUT_BG
        self.foreground_color = INK_DARK
        self.font_size = sp(16)
        self.font_name = 'Roboto'
        self.multiline = False
        self.size_hint_y = None
        self.height = dp(40)

class CalculatorWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(10)
        self.spacing = dp(10)

        # Calculator state
        self.expression = ""
        self.current_mode = "Basic"
        self.current_tab = "Simple Interest"
        self.entries = {}

        self.build_ui()

    def build_ui(self):
        self.clear_widgets()

        # Header with mode selector
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        header.add_widget(VintageLabel(text="Calculator Type:", size_hint_x=None, width=dp(120)))

        # Mode selector button (replaces Menubutton)
        self.mode_btn = VintageButton(text=self.current_mode, size_hint_x=None, width=dp(120))
        self.mode_btn.bind(on_release=self.show_mode_dropdown)
        header.add_widget(self.mode_btn)

        self.add_widget(header)

        # Main content area
        if self.current_mode == "Financial":
            self.build_financial_ui()
        else:
            self.build_standard_ui()

    def show_mode_dropdown(self, instance):
        dropdown = DropDown()
        for mode in ["Basic", "Scientific", "Financial"]:
            btn = VintageButton(text=mode, size_hint_y=None, height=dp(40))
            btn.bind(on_release=lambda x, mode=mode: self.select_mode(mode, dropdown))
            dropdown.add_widget(btn)
        dropdown.open(instance)

    def select_mode(self, mode, dropdown):
        self.current_mode = mode
        self.mode_btn.text = mode
        dropdown.dismiss()
        self.build_ui()

    def build_standard_ui(self):
        # Display
        self.display_input = VintageTextInput(
            text="", 
            readonly=True, 
            size_hint_y=None, 
            height=dp(50),
            halign="right"
        )
        self.add_widget(self.display_input)

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

        grid = layouts[self.current_mode]
        button_grid = GridLayout(
            cols=5 if self.current_mode == "Scientific" else 4,
            spacing=dp(5),
            size_hint_y=None
        )
        button_grid.bind(minimum_height=button_grid.setter('height'))

        for row in grid:
            for char in row:
                btn = VintageButton(
                    text=char,
                    size_hint_y=None,
                    height=dp(50)
                )
                if char in ("Clear", "C") and self.current_mode == "Basic":
                    btn.size_hint_x = 4  # Span across all columns
                btn.bind(on_release=lambda x, ch=char: self.press_button(ch))
                button_grid.add_widget(btn)

        self.add_widget(button_grid)

    def press_button(self, char):
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

        self.display_input.text = self.expression

    def build_financial_ui(self):
        # Tab selector
        tab_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=dp(5))
        tabs = ["Simple Interest", "Compound Interest", "Loan Calculator"]

        for tab in tabs:
            btn = VintageButton(text=tab, size_hint_x=1/len(tabs))
            if tab == self.current_tab:
                btn.background_color = (0.7, 0.4, 0.2, 1)  # Darker for active tab
            btn.bind(on_release=lambda x, t=tab: self.select_tab(t))
            tab_layout.add_widget(btn)

        self.add_widget(tab_layout)

        # Content area
        content = BoxLayout(orientation='vertical', spacing=dp(10))

        if self.current_tab in ("Simple Interest", "Compound Interest"):
            self.build_interest_ui(content)
        else:
            self.build_loan_ui(content)

        self.add_widget(content)

    def select_tab(self, tab):
        self.current_tab = tab
        self.build_ui()

    def build_interest_ui(self, container):
        form_layout = GridLayout(cols=2, spacing=dp(10), size_hint_y=None)
        form_layout.bind(minimum_height=form_layout.setter('height'))

        fields = ["Principal", "Rate % per year", "Time years"]
        self.entries = {}

        for field in fields:
            form_layout.add_widget(VintageLabel(text=f"{field}:", size_hint_y=None, height=dp(40)))
            entry = VintageTextInput()
            self.entries[field] = entry
            form_layout.add_widget(entry)

        if self.current_tab == "Compound Interest":
            form_layout.add_widget(VintageLabel(text="Compounds/year:", size_hint_y=None, height=dp(40)))
            entry = VintageTextInput()
            self.entries["Compounds"] = entry
            form_layout.add_widget(entry)

        container.add_widget(form_layout)

        # Calculate button
        calc_btn = VintageButton(
            text="Calculate",
            size_hint_y=None,
            height=dp(50)
        )
        calc_btn.bind(on_release=lambda x: self.calculate_interest())
        container.add_widget(calc_btn)

        # Result label
        self.result_label = VintageLabel(
            text="",
            size_hint_y=None,
            height=dp(80),
            text_size=(None, None),
            halign="center"
        )
        container.add_widget(self.result_label)

    def calculate_interest(self):
        try:
            P = float(self.entries["Principal"].text)
            R = float(self.entries["Rate % per year"].text) / 100
            T = float(self.entries["Time years"].text)

            if self.current_tab == "Simple Interest":
                si = P * R * T
                self.result_label.text = f"Simple Interest: ${si:.2f}\\nTotal Amount: ${P+si:.2f}"
            else:
                n = int(self.entries["Compounds"].text)
                amount = P * (1 + R / n) ** (n * T)
                self.result_label.text = f"Compound Interest: ${amount-P:.2f}\\nTotal Amount: ${amount:.2f}"
        except Exception:
            self.result_label.text = "Error: Enter valid numbers"
            self.result_label.color = (1, 0, 0, 1)  # Red for error

    def build_loan_ui(self, container):
        form_layout = GridLayout(cols=2, spacing=dp(10), size_hint_y=None)
        form_layout.bind(minimum_height=form_layout.setter('height'))

        fields = ["Loan Amount", "Rate % per year", "Term years"]
        self.entries = {}

        for field in fields:
            form_layout.add_widget(VintageLabel(text=f"{field}:", size_hint_y=None, height=dp(40)))
            entry = VintageTextInput()
            self.entries[field] = entry
            form_layout.add_widget(entry)

        container.add_widget(form_layout)

        # Calculate button
        calc_btn = VintageButton(
            text="Calculate EMI",
            size_hint_y=None,
            height=dp(50)
        )
        calc_btn.bind(on_release=lambda x: self.calculate_loan())
        container.add_widget(calc_btn)

        # Result label
        self.result_label = VintageLabel(
            text="",
            size_hint_y=None,
            height=dp(60),
            halign="center"
        )
        container.add_widget(self.result_label)

    def calculate_loan(self):
        try:
            P = float(self.entries["Loan Amount"].text)
            annual_rate = float(self.entries["Rate % per year"].text)
            years = int(self.entries["Term years"].text)
            r = (annual_rate / 100) / 12
            n = years * 12
            emi = P / n if r == 0 else P * (r * (1 + r) ** n) / ((1 + r) ** n - 1)
            self.result_label.text = f"Monthly EMI: ${emi:.2f}"
        except Exception:
            self.result_label.text = "Error: Enter valid numbers"
            self.result_label.color = (1, 0, 0, 1)

class CurrencyConverterWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(10)
        self.spacing = dp(10)

        self.api_url = "https://api.exchangerate-api.com/v4/latest/"
        self.rates = {}
        self.currencies = sorted([
            "USD", "EUR", "JPY", "GBP", "AUD", "CAD", "CHF", "CNY",
            "INR", "BRL", "RUB", "ZAR", "SGD", "NZD", "MXN", "KRW",
        ])
        self.from_currency = "USD"
        self.to_currency = "INR"

        self.build_ui()
        # Schedule rate update
        Clock.schedule_once(lambda dt: self.update_rates(), 1)

    def build_ui(self):
        # Title
        self.add_widget(VintageLabel(
            text="Currency Converter",
            size_hint_y=None,
            height=dp(40),
            font_size=sp(20),
            halign="center"
        ))

        # Amount input
        amount_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        amount_layout.add_widget(VintageLabel(text="Amount:", size_hint_x=None, width=dp(80)))
        self.amount_input = VintageTextInput(text="1.0")
        amount_layout.add_widget(self.amount_input)
        self.add_widget(amount_layout)

        # From currency
        from_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        from_layout.add_widget(VintageLabel(text="From:", size_hint_x=None, width=dp(80)))
        self.from_btn = VintageButton(text=self.from_currency, size_hint_x=None, width=dp(120))
        self.from_btn.bind(on_release=self.show_from_dropdown)
        from_layout.add_widget(self.from_btn)
        self.add_widget(from_layout)

        # To currency
        to_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        to_layout.add_widget(VintageLabel(text="To:", size_hint_x=None, width=dp(80)))
        self.to_btn = VintageButton(text=self.to_currency, size_hint_x=None, width=dp(120))
        self.to_btn.bind(on_release=self.show_to_dropdown)
        to_layout.add_widget(self.to_btn)
        self.add_widget(to_layout)

        # Action buttons
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=dp(10))

        convert_btn = VintageButton(text="Convert")
        convert_btn.bind(on_release=lambda x: self.convert_currency())
        button_layout.add_widget(convert_btn)

        update_btn = VintageButton(text="Update Rates")
        update_btn.bind(on_release=lambda x: self.update_rates(True))
        button_layout.add_widget(update_btn)

        self.add_widget(button_layout)

        # Result display
        self.result_label = VintageLabel(
            text="",
            size_hint_y=None,
            height=dp(60),
            halign="center"
        )
        self.add_widget(self.result_label)

        # Status messages
        self.status_label = VintageLabel(
            text="Fetching rates...",
            size_hint_y=None,
            height=dp(40),
            font_size=sp(12),
            halign="center"
        )
        self.add_widget(self.status_label)

        self.update_msg = VintageLabel(
            text="",
            size_hint_y=None,
            height=dp(40),
            font_size=sp(12),
            halign="center"
        )
        self.add_widget(self.update_msg)

    def show_from_dropdown(self, instance):
        self.show_currency_dropdown(instance, True)

    def show_to_dropdown(self, instance):
        self.show_currency_dropdown(instance, False)

    def show_currency_dropdown(self, instance, is_from):
        dropdown = DropDown()
        for currency in self.currencies:
            btn = VintageButton(text=currency, size_hint_y=None, height=dp(40))
            btn.bind(on_release=lambda x, curr=currency: self.select_currency(curr, is_from, dropdown))
            dropdown.add_widget(btn)
        dropdown.open(instance)

    def select_currency(self, currency, is_from, dropdown):
        if is_from:
            self.from_currency = currency
            self.from_btn.text = currency
            # Update rates when base currency changes
            Clock.schedule_once(lambda dt: self.update_rates(), 0.1)
        else:
            self.to_currency = currency
            self.to_btn.text = currency
        dropdown.dismiss()

    def update_rates(self, show_msg=False):
        self.status_label.text = f"Updating rates for {self.from_currency}..."
        if show_msg:
            self.update_msg.text = ""

        try:
            import threading
            thread = threading.Thread(target=self._fetch_rates, args=(show_msg,))
            thread.daemon = True
            thread.start()
        except Exception:
            self.status_label.text = "Error updating rates"
            if show_msg:
                self.update_msg.text = "✗ Failed to update rates"
                self.update_msg.color = (1, 0, 0, 1)

    def _fetch_rates(self, show_msg):
        try:
            data = requests.get(f"{self.api_url}{self.from_currency}", timeout=10).json()
            self.rates = data.get("rates", {})
            Clock.schedule_once(lambda dt: self._update_ui_after_fetch(data, show_msg), 0)
        except Exception:
            Clock.schedule_once(lambda dt: self._update_ui_error(show_msg), 0)

    def _update_ui_after_fetch(self, data, show_msg):
        self.status_label.text = f"Rates updated: {data.get('date', '')}"
        if show_msg:
            self.update_msg.text = f"✓ Updated rates for {self.from_currency}!"
            self.update_msg.color = (0, 0.5, 0, 1)  # Green
            Clock.schedule_once(lambda dt: setattr(self.update_msg, 'text', ''), 5)

    def _update_ui_error(self, show_msg):
        self.status_label.text = "Error updating rates"
        if show_msg:
            self.update_msg.text = "✗ Failed to update rates"
            self.update_msg.color = (1, 0, 0, 1)  # Red

    def convert_currency(self):
        try:
            amount = float(self.amount_input.text)
            rate = self.rates.get(self.to_currency)
            if rate is None:
                raise ValueError("Rate missing")
            result = amount * rate
            self.result_label.text = f"{amount:.2f} {self.from_currency} = {result:.2f} {self.to_currency}"
            self.result_label.color = INK_DARK
        except Exception:
            self.result_label.text = "Error: Check amount/rates"
            self.result_label.color = (1, 0, 0, 1)

if __name__ == "__main__":
    FinancialApp().run()
'''

# Save main application file
with open("CalculatorCurrencyKivy.py", "w") as f:
    f.write(kivy_app_code)

print("Created financial_app_kivy.py - Main Kivy application file")
