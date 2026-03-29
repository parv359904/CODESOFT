import customtkinter as ctk
import math
import ast
import operator

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


# ================= SAFE EVAL =================

ops = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg
}

def safe_eval(expr):
    def eval_node(node):
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.BinOp):
            return ops[type(node.op)](
                eval_node(node.left),
                eval_node(node.right)
            )
        elif isinstance(node, ast.UnaryOp):
            return ops[type(node.op)](eval_node(node.operand))
        else:
            raise Exception("Invalid")

    return eval_node(ast.parse(expr, mode='eval').body)


# ================= FUTURISTIC APP =================

class FuturisticCalculator(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Neon Core Calculator")
        self.geometry("380x580")
        self.resizable(False, False)

        self.configure(fg_color="#0f0f1a")

        self.create_ui()
        self.bind_keys()

    # ================= UI =================

    def create_ui(self):

        self.display = ctk.CTkEntry(
            self,
            font=("Orbitron", 28),
            height=60,
            justify="right",
            text_color="#00ffff",
            fg_color="#141427",
            border_color="#00ffff",
            border_width=2
        )
        self.display.pack(padx=15, pady=(25,15), fill="x")

        self.create_buttons()

    def create_buttons(self):

        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(padx=10, pady=10)

        buttons = [
            ["AC", "±", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "x²", "="]
        ]

        for r, row in enumerate(buttons):
            for c, text in enumerate(row):

                neon_color = "#ff00ff" if text in ["÷","×","-","+","="] else "#1c1c3c"

                btn = ctk.CTkButton(
                    frame,
                    text=text,
                    width=75,
                    height=60,
                    corner_radius=18,
                    fg_color=neon_color,
                    hover_color="#00ffff",
                    text_color="white",
                    font=("Orbitron", 18),
                    command=lambda t=text: self.on_click(t)
                )

                btn.grid(row=r, column=c, padx=6, pady=6)

    # ================= LOGIC =================

    def on_click(self, value):

        if value == "AC":
            self.display.delete(0, "end")

        elif value == "=":
            self.calculate()

        elif value == "±":
            try:
                num = safe_eval(self.display.get())
                self.display.delete(0, "end")
                self.display.insert(0, str(-num))
            except:
                self.show_error()

        elif value == "%":
            try:
                num = safe_eval(self.display.get())
                self.display.delete(0, "end")
                self.display.insert(0, str(num/100))
            except:
                self.show_error()

        elif value == "x²":
            try:
                num = safe_eval(self.display.get())
                self.display.delete(0, "end")
                self.display.insert(0, str(num**2))
            except:
                self.show_error()

        elif value == "÷":
            self.display.insert("end", "/")

        elif value == "×":
            self.display.insert("end", "*")

        else:
            self.display.insert("end", value)

    def calculate(self):
        try:
            expr = self.display.get()
            result = safe_eval(expr)
            self.animate_success()
            self.display.delete(0, "end")
            self.display.insert(0, str(result))
        except:
            self.show_error()

    # ================= EFFECTS =================

    def animate_success(self):
        self.display.configure(border_color="#00ff88")
        self.after(200, lambda: self.display.configure(border_color="#00ffff"))

    def show_error(self):
        self.display.delete(0, "end")
        self.display.insert(0, "Error")
        self.display.configure(border_color="#ff0000")
        self.after(400, lambda: self.display.configure(border_color="#00ffff"))

    # ================= KEYBOARD =================

    def bind_keys(self):

        for key in "0123456789+-*/.":
            self.bind(key, lambda e, k=key: self.display.insert("end", k))

        self.bind("<Return>", lambda e: self.calculate())
        self.bind("<BackSpace>", lambda e: self.display.delete(len(self.display.get())-1, "end"))
        self.bind("<Escape>", lambda e: self.display.delete(0, "end"))


# ================= RUN =================

if __name__ == "__main__":
    app = FuturisticCalculator()
    app.mainloop()