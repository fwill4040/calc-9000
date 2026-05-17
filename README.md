# CALC-9000

A simple Python GUI calculator built with tkinter.

---

## Requirements

- Python 3.x
- tkinter (included with Python by default on Windows)

---

## How to Run

```bash
python calculator.py
```

---

## Features

- Addition, subtraction, multiplication, and division
- Chained operations without needing to press = each time
- Decimal point support
- Backspace to delete the last digit
- Clear button to reset everything
- Division by zero protection — displays an error instead of crashing
- Full keyboard support

---

## Keyboard Shortcuts

| Key              | Action            |
|------------------|-------------------|
| 0 - 9            | Input digit       |
| + - * /          | Operators         |
| .                | Decimal point     |
| Enter            | Calculate result  |
| Backspace        | Delete last digit |
| Escape           | Clear all         |

---

## Error Handling

| Display        | Meaning                        |
|----------------|--------------------------------|
| Error: Div/0   | Division by zero attempted     |
| Error          | Unexpected calculation failure |

---

## Project Structure

```
calc-9000/
├── calculator.py   # Full application
└── README.md       # You're reading it
```

---

## Author

Built as part of a software development coursework project.

---

## License

MIT — free to use, modify, and distribute.
