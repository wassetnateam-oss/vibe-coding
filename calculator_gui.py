"""
GUI Calculator using Python's built-in tkinter module (no external libraries needed).
"""

import tkinter as tk

class CalculatorGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("320x420")
        self.root.resizable(False, False)
        self.root.configure(bg="#22252d")

        self.expression = ""

        # Display screen
        self.display_var = tk.StringVar(value="0")
        self._create_display()

        # Keypad buttons
        self._create_buttons()

    def _create_display(self):
        frame = tk.Frame(self.root, bg="#22252d", padx=10, pady=15)
        frame.pack(fill="x")

        display_label = tk.Label(
            frame,
            textvariable=self.display_var,
            font=("Arial", 28),
            bg="#292d36",
            fg="#ffffff",
            anchor="e",
            padx=15,
            pady=15,
            relief="flat"
        )
        display_label.pack(fill="x")

    def _create_buttons(self):
        buttons_layout = [
            [("C", self._clear, "#eb6666", "#ffffff"), ("^", lambda: self._append("**"), "#393e46", "#4eedb0"), ("%", lambda: self._append("%"), "#393e46", "#4eedb0"), ("/", lambda: self._append("/"), "#ff9500", "#ffffff")],
            [("7", lambda: self._append("7"), "#2a2d37", "#ffffff"), ("8", lambda: self._append("8"), "#2a2d37", "#ffffff"), ("9", lambda: self._append("9"), "#2a2d37", "#ffffff"), ("*", lambda: self._append("*"), "#ff9500", "#ffffff")],
            [("4", lambda: self._append("4"), "#2a2d37", "#ffffff"), ("5", lambda: self._append("5"), "#2a2d37", "#ffffff"), ("6", lambda: self._append("6"), "#2a2d37", "#ffffff"), ("-", lambda: self._append("-"), "#ff9500", "#ffffff")],
            [("1", lambda: self._append("1"), "#2a2d37", "#ffffff"), ("2", lambda: self._append("2"), "#2a2d37", "#ffffff"), ("3", lambda: self._append("3"), "#2a2d37", "#ffffff"), ("+", lambda: self._append("+"), "#ff9500", "#ffffff")],
            [("0", lambda: self._append("0"), "#2a2d37", "#ffffff"), (".", lambda: self._append("."), "#2a2d37", "#ffffff"), ("⌫", self._backspace, "#393e46", "#ffffff"), ("=", self._calculate, "#2ec4b6", "#ffffff")]
        ]

        pad_frame = tk.Frame(self.root, bg="#22252d", padx=10, pady=5)
        pad_frame.pack(fill="both", expand=True)

        for row_idx, row in enumerate(buttons_layout):
            pad_frame.rowconfigure(row_idx, weight=1)
            for col_idx, (text, command, bg_color, fg_color) in enumerate(row):
                pad_frame.columnconfigure(col_idx, weight=1)
                btn = tk.Button(
                    pad_frame,
                    text=text,
                    font=("Arial", 14, "bold"),
                    bg=bg_color,
                    fg=fg_color,
                    activebackground="#4f5665",
                    activeforeground="#ffffff",
                    relief="flat",
                    bd=0,
                    command=command
                )
                btn.grid(row=row_idx, column=col_idx, padx=4, pady=4, sticky="nsew")

    def _append(self, char: str):
        if self.expression == "" and char in ("+", "*", "/", "%", "^", "**"):
            return
        self.expression += char
        self._update_display(self.expression)

    def _clear(self):
        self.expression = ""
        self._update_display("0")

    def _backspace(self):
        if self.expression:
            if self.expression.endswith("**"):
                self.expression = self.expression[:-2]
            else:
                self.expression = self.expression[:-1]
            self._update_display(self.expression if self.expression else "0")

    def _update_display(self, text: str):
        # Format display text for power operator
        shown_text = text.replace("**", "^")
        self.display_var.set(shown_text)

    def _calculate(self):
        if not self.expression:
            return

        # Safe evaluation checking: only allow math characters and numbers
        allowed_chars = set("0123456789+-*/%.() ")
        # Check tokens
        test_expr = self.expression.replace("**", "")
        if not set(test_expr).issubset(allowed_chars):
            self.display_var.set("Error")
            self.expression = ""
            return

        try:
            result = eval(self.expression, {"__builtins__": None}, {})
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            self.expression = str(result)
            self._update_display(self.expression)
        except ZeroDivisionError:
            self.display_var.set("Cannot divide by 0")
            self.expression = ""
        except Exception:
            self.display_var.set("Error")
            self.expression = ""

def main():
    root = tk.Tk()
    CalculatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

