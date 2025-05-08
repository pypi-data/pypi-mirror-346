# probot_tax/__init__.py

def calculate_tax(amount):
    if isinstance(amount, str):
        amount = amount.strip()
        if not amount.replace('.', '', 1).isdigit():
            raise ValueError("Invalid input: amount must be a number.")
        amount = float(amount)
    elif isinstance(amount, (int, float)):
        amount = float(amount)
    else:
        raise TypeError("Amount must be a number (int, float) or a numeric string.")
    
    if amount < 0:
        raise ValueError("Amount cannot be negative.")

    amount = round(amount)
    tax = round(amount * 0.05)
    total = amount + tax

    return {
        "amount": amount,
        "tax": tax,
        "total": total
    }
