# probot_tax

A one‑file Python library to calculate ProBot tax (5%) only, with full input handling.

> By Adham Hmady  
> Discord: Dewecat / 7teq  

---

## Features

- Calculates a fixed 5% “ProBot” tax on any amount  
- Accepts `int`, `float`, or numeric `str` inputs  
- Rounds amounts to the nearest integer before computing tax  
- Raises a clear `InvalidAmountError` if the input is invalid or negative  

---

## Installation

After publishing to PyPI under the name **probot‑tax**, install with:

```bash
pip install probot‑tax
