
# probot_tax

A simple Python library to calculate [ProBot](https://probot.io) tax (5%) only — with full input validation and flexible output formatting.

---

## 📦 Installation

You can install the library via [PyPI](https://pypi.org/project/probot-tax):

```bash
pip install probot-tax
```

---

## 🚀 Features

- ✅ Calculates **only** ProBot 5% tax (no middleman tax).
- ✅ Input can be `int`, `float`, or `str` numbers.
- ✅ Output can be a simple number or a JSON-like dictionary.
- ✅ Includes full input validation and helpful error messages.
- ✅ Automatically rounds tax and totals to the nearest integer.

---

## 🧠 How it works

ProBot tax is 5% of the amount sent.  
This library calculates:
- `protax`: the 5% tax
- `total`: the amount + tax required to be sent

---

## 🧪 Basic Usage

```python
import probot_tax

# Default output: JSON
result = probot_tax.calculate_tax(1000)
print(result)
# Output: {'protax': 50, 'total': 1050}

# Output as number only (just the tax)
tax_only = probot_tax.calculate_tax("2000", output="number")
print(tax_only)
# Output: 100
```

---

## 🛠 Output Modes

| Output Mode | Description                        | Example                             |
|-------------|------------------------------------|-------------------------------------|
| `"json"`    | Returns dict with tax + total      | `{'protax': 25, 'total': 525}`      |
| `"number"`  | Returns only the tax as integer    | `25`                                |

---

## 🔒 Input Validation

This library will raise `ValueError` in the following cases:
- Input is not a number (e.g., string `"abc"`)
- Input is a negative number
- Output mode is not `"json"` or `"number"`

---

## 📤 Example Errors

```python
probot_tax.calculate_tax("abc")
# ValueError: Input must be a valid number

probot_tax.calculate_tax(-100)
# ValueError: Amount must be non-negative

probot_tax.calculate_tax(100, output="xml")
# ValueError: Invalid output format. Use 'json' or 'number'
```

---

## 📘 License

This project is licensed under the MIT License.

---

## 💬 Author

Made with ❤️ by **Adham Hamdy**  
Discord: `dewecat / 7teq`  
GitHub: [@Adham Hamdy](https://github.com/AdhamT1) | GitHub: [probot-tax](https://github.com/AdhamT1/probot-tax)
