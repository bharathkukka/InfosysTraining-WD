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
