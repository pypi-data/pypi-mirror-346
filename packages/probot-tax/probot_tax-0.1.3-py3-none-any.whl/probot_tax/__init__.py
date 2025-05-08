# probot_tax/core.py

def calculate_tax(amount, output="json"):
    try:
        amount = float(amount)
    except (ValueError, TypeError):
        raise ValueError("Input must be a valid number")

    if amount < 0:
        raise ValueError("Amount must be non-negative")

    protax = round(amount * 0.05)
    total = round(amount + protax)

    if output == "json":
        return {
            "protax": protax,
            "total": total
        }
    elif output == "number":
        return protax
    else:
        raise ValueError("Invalid output format. Use 'json' or 'number'")
