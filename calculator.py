"""
CALC-9000 — Python GUI Calculator
"""

import tkinter as tk
import math


# ── Color Palette ─────────────────────────────────────────────────────────────
BG        = "#0a0c0f"
PANEL     = "#111418"
BORDER    = "#1e2530"
GREEN     = "#00ff9d"
GREEN_DIM = "#00804e"
AMBER     = "#ffb300"
RED       = "#ff3c5a"
BLUE      = "#00aaff"
TEXT      = "#c8ffe0"
TEXT_DIM  = "#3a6650"
BTN_BG    = "#141a20"
BTN_HOVER = "#1c2830"
BTN_ACT   = "#0d1014"


# ── Calculator Logic ──────────────────────────────────────────────────────────
class CalcEngine:
    def __init__(self):
        self.reset()

    def reset(self):
        self.current              = "0"
        self.prev_value           = None
        self.operator             = None
        self.expression           = ""
        self.just_calculated      = False
        self.waiting_for_operand  = False
        self.memory               = None
        self.history              = []

    def input_digit(self, digit):
        if self.just_calculated or self.waiting_for_operand:
            self.current = digit
            if self.just_calculated:
                self.expression = ""
            self.just_calculated     = False
            self.waiting_for_operand = False
        elif self.current == "0" and digit != ".":
            self.current = digit
        elif len(self.current.replace(".", "").replace("-", "")) >= 12:
            return
        else:
            self.current += digit

    def input_decimal(self):
        if self.just_calculated or self.waiting_for_operand:
            self.current             = "0."
            self.just_calculated     = False
            self.waiting_for_operand = False
        elif "." not in self.current:
            self.current += "."

    def input_operator(self, op):
        if self.operator and not self.just_calculated and self.prev_value is not None:
            result = self._compute(float(self.prev_value), float(self.current), self.operator)
            if "error" in result:
                return result["error"]
            self.prev_value = str(result["value"])
            self.current    = str(result["value"])
        else:
            self.prev_value = self.current

        self.operator            = op
        self.just_calculated     = False
        self.waiting_for_operand = True
        sym = {"+": "+", "-": "−", "*": "×", "/": "÷", "**": "^", "%": "%"}
        self.expression = f"{self._fmt(self.prev_value)} {sym.get(op, op)}"
        return None

    def calculate(self):
        if self.operator is None or self.prev_value is None:
            return None
        a, b   = float(self.prev_value), float(self.current)
        result = self._compute(a, b, self.operator)

        if "error" in result:
            self.expression      = f"{self.current} → {result['error']}"
            self.current         = result["error"]
            self.operator        = None
            self.prev_value      = None
            self.just_calculated = True
            return result["error"], True

        sym  = {"+": "+", "-": "−", "*": "×", "/": "÷", "**": "^", "%": "%"}
        expr = f"{self._fmt(self.prev_value)} {sym.get(self.operator, self.operator)} {self._fmt(self.current)}"
        val  = float(f"{result['value']:.10g}")

        self.history.append({"expr": expr, "result": str(val)})
        self.expression      = f"{expr} ="
        self.current         = str(val)
        self.operator        = None
        self.prev_value      = None
        self.just_calculated = True
        return str(val), False

    def scientific(self, fn):
        try:
            val = float(self.current)
        except ValueError:
            return "ERROR", True

        to_rad = lambda v: v * math.pi / 180
        labels = {"sin": "SIN", "cos": "COS", "tan": "TAN", "sqrt": "√", "log": "LOG"}

        try:
            if fn == "sin":
                res = math.sin(to_rad(val))
            elif fn == "cos":
                res = math.cos(to_rad(val))
            elif fn == "tan":
                if abs(val % 180) == 90:
                    return "UNDEF", True
                res = math.tan(to_rad(val))
            elif fn == "sqrt":
                if val < 0:
                    return "DOMAIN", True
                res = math.sqrt(val)
            elif fn == "log":
                if val <= 0:
                    return "DOMAIN", True
                res = math.log10(val)
            else:
                return "ERROR", True
        except Exception:
            return "ERROR", True

        if not math.isfinite(res):
            return "OVERFLOW", True

        res_str = str(float(f"{res:.10g}"))
        self.expression      = f"{labels[fn]}({self._fmt(self.current)}) ="
        self.current         = res_str
        self.just_calculated = True
        self.history.append({"expr": f"{labels[fn]}({val})", "result": res_str})
        return res_str, False

    def toggle_sign(self):
        if self.current == "0":
            return
        self.current = self.current[1:] if self.current.startswith("-") else "-" + self.current

    def backspace(self):
        if self.just_calculated or len(self.current) <= 1:
            self.current = "0"
        else:
            self.current = self.current[:-1] or "0"

    def mem_store(self):
        try:
            self.memory = float(self.current)
        except ValueError:
            pass

    def mem_recall(self):
        if self.memory is not None:
            self.current         = str(self.memory)
            self.just_calculated = False

    def mem_clear(self):
        self.memory = None

    def _compute(self, a, b, op):
        try:
            if op == "+":    v = a + b
            elif op == "-":  v = a - b
            elif op == "*":  v = a * b
            elif op == "/":
                if b == 0:   return {"error": "DIV/0"}
                v = a / b
            elif op == "**": v = a ** b
            elif op == "%":  v = a % b
            else:            return {"error": "ERROR"}
            if not math.isfinite(v): return {"error": "OVERFLOW"}
            return {"value": v}
        except Exception:
            return {"error": "ERROR"}

    def _fmt(self, n):
        try:
            return str(float(f"{float(n):.8g}"))
        except Exception:
            return n

    def format_display(self, val):
        try:
            num = float(val)
            if abs(num) > 1e12 or (abs(num) < 1e-9 and num != 0):
                return f"{num:.4e}"
            return str(float(f"{num:.10g}"))
        except Exception:
            return val


# ── GUI ───────────────────────────────────────────────────────────────────────
class Calc9000(tk.Tk):
    def __init__(self):
        super().__init__()
        self.engine = CalcEngine()
        self.title("CALC-9000")
        self.resizable(False, False)
        self.configure(bg=BG)

        w, h = 360, 640
        self.update_idletasks()
        x = (self.winfo_screenwidth()  - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

        self._build_ui()
        self._bind_keys()
        self._refresh()

    def _build_ui(self):
        # Header
        hdr = tk.Frame(self, bg=PANEL, pady=10)
        hdr.pack(fill="x", padx=12, pady=(12, 0))
        tk.Label(hdr, text="CALC-9000", bg=PANEL, fg=GREEN,
                 font=("Courier", 12, "bold")).pack(side="left", padx=10)
        dots = tk.Frame(hdr, bg=PANEL)
        dots.pack(side="right", padx=10)
        for color in [RED, AMBER, GREEN]:
            tk.Label(dots, text="●", bg=PANEL, fg=color,
                     font=("Courier", 10)).pack(side="left", padx=2)

        # Display
        disp = tk.Frame(self, bg="#060809",
                        highlightbackground=BORDER, highlightthickness=1)
        disp.pack(fill="x", padx=12, pady=(8, 0))
        self.expr_var = tk.StringVar()
        tk.Label(disp, textvariable=self.expr_var, bg="#060809", fg=TEXT_DIM,
                 font=("Courier", 9), anchor="e").pack(fill="x", padx=12, pady=(8, 0))
        self.main_var = tk.StringVar(value="0")
        self.main_lbl = tk.Label(disp, textvariable=self.main_var,
                                  bg="#060809", fg=GREEN,
                                  font=("Courier", 28, "bold"), anchor="e")
        self.main_lbl.pack(fill="x", padx=12, pady=(0, 10))

        # Memory bar
        mbar =