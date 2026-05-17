"""
CALC-9000 — Python GUI Calculator
Run: python calculator.py
"""

import tkinter as tk
import math

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


class CalcEngine:
    def __init__(self):
        self.reset()

    def reset(self):
        self.current             = "0"
        self.prev_value          = None
        self.operator            = None
        self.expression          = ""
        self.just_calculated     = False
        self.waiting_for_operand = False
        self.memory              = None
        self.history             = []

    def input_digit(self, digit):
        if self.just_calculated or self.waiting_for_operand:
            self.current             = digit
            if self.just_calculated:
                self.expression      = ""
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
        sym = {"+": "+", "-": "-", "*": "x", "/": "/", "**": "^", "%": "%"}
        self.expression = self._fmt(self.prev_value) + " " + sym.get(op, op)
        return None

    def calculate(self):
        if self.operator is None or self.prev_value is None:
            return None
        a      = float(self.prev_value)
        b      = float(self.current)
        result = self._compute(a, b, self.operator)
        if "error" in result:
            self.expression      = self.current + " -> " + result["error"]
            self.current         = result["error"]
            self.operator        = None
            self.prev_value      = None
            self.just_calculated = True
            return result["error"], True
        sym  = {"+": "+", "-": "-", "*": "x", "/": "/", "**": "^", "%": "%"}
        expr = self._fmt(self.prev_value) + " "