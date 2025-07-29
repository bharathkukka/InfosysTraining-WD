# Calculator and Currency Converter 

A financial calculator and currency converter application built with Python's Tkinter library

## 🎨 Features   

### Calculator Modes
- **Basic Calculator**: Standard arithmetic operations with a clean vintage interface
- **Scientific Calculator**: Advanced mathematical functions including trigonometry, logarithms, and constants
- **Financial Calculator**: Specialized tools for financial calculations
  - Simple Interest Calculator
  - Compound Interest Calculator  
  - Loan EMI Calculator

### Currency Converter
- Real-time currency conversion using live exchange rates
- Support for 16 major world currencies (USD, EUR, JPY, GBP, INR, etc.)
- Automatic rate updates with manual refresh option
- Clean, intuitive interface with dropdown currency selection

## 🎯 Design Philosophy

The application features a distinctive vintage aesthetic with:
- **Comic Sans MS** font for a handwritten feel
- **Cream and paper** color scheme (#FAF3E0, #F5E6C4)
- **Dark ink** styling (#5B4636) for text
- Groove borders and classic button styling

## 📋 Requirements

- Python 3.6+
- Required packages:
  ```
  tkinter (usually comes with Python)
  requests
  math (built-in)
  ```

## 🚀 Installation

1. **Clone or download** the repository
2. **Install dependencies**:
   ```bash
   pip install requests
   ```
3. **Run the application**:
   ```bash
   python financial_app.py
   ```

## 💡 Usage

### Calculator
1. **Select calculator type** from the dropdown menu (Basic/Scientific/Financial)
2. **Basic/Scientific**: Click buttons to input expressions, press "=" to calculate
3. **Financial**: 
   - Choose between Simple Interest, Compound Interest, or Loan Calculator tabs
   - Fill in the required fields (Principal, Rate, Time, etc.)
   - Click "Calculate" to get results

### Currency Converter
1. **Enter amount** in the input field
2. **Select source currency** from the "From" dropdown
3. **Select target currency** from the "To" dropdown  
4. **Click "Convert"** to see the result
5. **Update rates** manually using the "Update Rates" button

## 🌐 API Information

The currency converter uses the **ExchangeRate-API** service:
- **Endpoint**: `https://api.exchangerate-api.com/v4/latest/`
- **No API key required** for basic usage
- **Rate limits**: Check API documentation for current limits
- **Supported currencies**: USD, EUR, JPY, GBP, AUD, CAD, CHF, CNY, INR, BRL, RUB, ZAR, SGD, NZD, MXN, KRW

## Results 

![Calculator and Currency Converter](https://github.com/bhaarath22/WebDev-AI-Projects/blob/3baefc92cb5715aa79e98a1011eedb6f51bfb85a/Calculator-CurrencyConverter/Data/BC.png)

![Calculator and Currency Converter](https://github.com/bhaarath22/WebDev-AI-Projects/blob/cfee272c1f8cebf3bdab01efeb4053d668ad3237/Calculator-CurrencyConverter/Data/SC.png)

![Calculator and Currency Converter](https://github.com/bhaarath22/WebDev-AI-Projects/blob/cfee272c1f8cebf3bdab01efeb4053d668ad3237/Calculator-CurrencyConverter/Data/LC.png)  
---
### ***Issue**

### 🐛 Issue: Invisible Button Text on macOS

While testing the Project on macOS, I ran into a critical UI issue: all `tkinter` button labels were invisible. The buttons themselves were clickable and functional—but without visible text, the interface became unusable.

![Calculator and Currency Converter]([Calculator-CurrencyConverter/Data/Fail.png](https://github.com/bhaarath22/WebDev-AI-Projects/blob/cfee272c1f8cebf3bdab01efeb4053d668ad3237/Calculator-CurrencyConverter/Data/Fail.png))

![Calculator and Currency Converter]([Calculator-CurrencyConverter/Data/Fail1.png](https://github.com/bhaarath22/WebDev-AI-Projects/blob/cfee272c1f8cebf3bdab01efeb4053d668ad3237/Calculator-CurrencyConverter/Data/Fail1.png))
---
### 🔍 Root Cause

This issue stems from macOS shipping with an outdated version of **Tcl/Tk (v8.5)**, which has known rendering bugs with standard `tkinter` widgets—especially buttons.

---

### ✅ Solution: Switch to `ttk.Button`

The fix was simple but effective: replace `tk.Button` with `ttk.Button`, the themed widget from `tkinter.ttk`, which supports modern OS styling and works correctly with macOS.

#### 🔧 Before (Buggy on macOS):

```python
import tkinter as tk

my_button = tk.Button(root, text="Click Me")
```

#### ✔️ After (Works Everywhere):

```python
from tkinter import ttk

my_button = ttk.Button(root, text="Click Me")
```

This small change restored button labels on macOS and improved the overall UI consistency across platforms.

---


## 🔧 Technical Details

### File Structure
```
financial_app.py          # Main application file
├── FinancialApp          # Main window class
├── CalculatorFrame       # Calculator component
└── CurrencyConverterFrame # Currency converter component
```

### Key Classes
- **FinancialApp**: Main application window and styling setup
- **CalculatorFrame**: Handles all calculator modes and computations
- **CurrencyConverterFrame**: Manages currency conversion and API calls

## 🎨 Customization

You can easily customize the vintage theme by modifying these constants:
```python
HANDWRITTEN = "Comic Sans MS"    # Font family
CREAM_BG = "#FAF3E0"            # Background color
PAPER_BG = "#F5E6C4"            # Paper background
INK_DARK = "#5B4636"            # Text color
```

## 🐛 Known Issues

- **Internet connection required** for currency conversion
- **Font fallback**: If Comic Sans MS is not available, system will use default font
- **Cross-platform styling**: Some styling may vary between operating systems

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source. Feel free to use, modify, and distribute according to your needs.

## 🔮 Future Enhancements

- [ ] Add more currencies
- [ ] Implement currency rate history charts
- [ ] Add investment calculators (ROI, NPV, IRR)
- [ ] Save/load calculation history
- [ ] Export results to CSV/PDF
- [ ] Add unit converter functionality
- [ ] Implement custom themes
