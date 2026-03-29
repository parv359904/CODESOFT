import customtkinter as ctk
import random
import string
import math

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

words = [
    "Tiger", "Moon", "Matrix", "Vision", "Quantum",
    "Phoenix", "Dragon", "Galaxy", "Storm", "Shadow",
    "Falcon", "Neon", "Cyber", "Nova", "Blaze"
]

symbols = "!@#$%^&*"


class SmartPass(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("SmartPass AI")
        self.geometry("420x600")
        self.resizable(False, False)

        self.create_ui()

    def create_ui(self):

        ctk.CTkLabel(self,
                     text="SMARTPASS AI",
                     font=("Segoe UI", 22, "bold"),
                     text_color="#00ffff").pack(pady=15)

        self.password_entry = ctk.CTkEntry(
            self,
            height=55,
            font=("Consolas", 20),
            justify="center"
        )
        self.password_entry.pack(padx=20, pady=10, fill="x")

        self.custom_word = ctk.CTkEntry(
            self,
            placeholder_text="Optional: Enter your word (e.g. Delhi)"
        )
        self.custom_word.pack(padx=20, pady=10, fill="x")

        self.strength_label = ctk.CTkLabel(self, text="")
        self.strength_label.pack(pady=5)

        ctk.CTkButton(
            self,
            text="Generate Smart Password",
            command=self.generate_smart
        ).pack(pady=10, padx=20, fill="x")

        ctk.CTkButton(
            self,
            text="Mnemonic Mode",
            fg_color="#ff00ff",
            command=self.generate_mnemonic
        ).pack(pady=5, padx=20, fill="x")

    # ================= SMART MODE =================

    def generate_smart(self):

        base_word = self.custom_word.get()

        if not base_word:
            base_word = random.choice(words)

        word2 = random.choice(words)
        number = str(random.randint(10, 99))
        symbol = random.choice(symbols)

        password = base_word.capitalize() + word2 + symbol + number

        self.password_entry.delete(0, "end")
        self.password_entry.insert(0, password)

        self.check_strength(password)

    # ================= MNEMONIC MODE =================

    def generate_mnemonic(self):

        sentence = self.custom_word.get()

        if not sentence:
            return

        words_split = sentence.split()
        mnemonic = ''.join(word[0].upper() for word in words_split)

        number = str(random.randint(100, 999))
        symbol = random.choice(symbols)

        password = mnemonic + number + symbol

        self.password_entry.delete(0, "end")
        self.password_entry.insert(0, password)

        self.check_strength(password)

    # ================= STRENGTH =================

    def check_strength(self, password):

        pool = 26 + 26 + 10 + len(symbols)
        entropy = len(password) * math.log2(pool)

        if entropy < 40:
            strength = "Weak"
            color = "red"
        elif entropy < 70:
            strength = "Moderate"
            color = "orange"
        else:
            strength = "Strong"
            color = "green"

        self.strength_label.configure(
            text=f"Strength: {strength}",
            text_color=color
        )


if __name__ == "__main__":
    app = SmartPass()
    app.mainloop()