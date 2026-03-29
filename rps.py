import tkinter as tk
import random
import time
import math
import json
from datetime import datetime
from enum import Enum

# --- Professional Constants ---
THEME = {
    "bg": "#020205",
    "primary": "#00D4FF",
    "secondary": "#FF0055",
    "accent": "#00FF9F",
    "text_dim": "#444466"
}

class Move(Enum):
    ROCK = ("ROCK", "🪨")
    PAPER = ("PAPER", "📄")
    SCISSORS = ("SCISSORS", "✂️")

# --- Logic & Data Persistence ---
class GameController:
    """Handles the back-end logic and JSON data logging."""
    @staticmethod
    def get_outcome(u: Move, c: Move):
        if u == c: return "TIE"
        win_conditions = {Move.ROCK: Move.SCISSORS, Move.PAPER: Move.ROCK, Move.SCISSORS: Move.PAPER}
        return "WIN" if win_conditions[u] == c else "LOSS"

    @staticmethod
    def save_session_data(data):
        """Saves session stats to a JSON file for professional data tracking."""
        try:
            with open("session_audit.json", "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Log Error: {e}")

# --- High-Performance Graphics ---
class VisualEffect:
    """Manages physics-based particles with gravity and fade-out."""
    def __init__(self, canvas, x, y, color):
        self.canvas = canvas
        self.id = canvas.create_oval(x, y, x+5, y+5, fill=color, outline="")
        self.vx = random.uniform(-10, 10)
        self.vy = random.uniform(-10, 10)
        self.life = 1.0

    def update(self):
        self.vy += 0.5  # Gravity
        self.canvas.move(self.id, self.vx, self.vy)
        self.life -= 0.04
        if self.life <= 0:
            self.canvas.delete(self.id)
            return False
        return True

# --- Main Application (Apex Version) ---
class ApexRPS:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("APEX_PROTOCOL // RPS_CORE_V4")
        self.window.geometry("1100x750")
        self.window.configure(bg=THEME["bg"])

        self.canvas = tk.Canvas(self.window, bg=THEME["bg"], highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Session Metrics
        self.metrics = {"wins": 0, "losses": 0, "ties": 0, "timestamp": str(datetime.now())}
        self.particles = []
        self.is_busy = False
        
        self._build_interface()
        self._run_core_loop()
        self.window.mainloop()

    def _build_interface(self):
        """Creates a high-tech HUD (Heads-Up Display)."""
        # HUD Elements
        self.hud_title = self.canvas.create_text(550, 60, text="NEON_SYSTEM_ACTIVE", fill=THEME["accent"], font=("Fixedsys", 20))
        self.hud_stats = self.canvas.create_text(550, 120, text="W: 0 | L: 0", fill="white", font=("Consolas", 40, "bold"))
        
        # Player Platforms
        self.canvas.create_rectangle(150, 450, 400, 460, fill=THEME["primary"])
        self.canvas.create_rectangle(700, 450, 950, 460, fill=THEME["secondary"])
        
        self.user_view = self.canvas.create_text(275, 350, text="IDLE", fill="white", font=("Arial", 90))
        self.comp_view = self.canvas.create_text(825, 350, text="IDLE", fill="white", font=("Arial", 90))

        # Control Panel
        self._add_cyber_button("ROCK", 275, 650, Move.ROCK)
        self._add_cyber_button("PAPER", 550, 650, Move.PAPER)
        self._add_cyber_button("SCISSORS", 825, 650, Move.SCISSORS)

    def _add_cyber_button(self, txt, x, y, move):
        frame = tk.Frame(self.window, bg=THEME["primary"], padx=2, pady=2)
        btn = tk.Button(frame, text=txt, bg=THEME["bg"], fg=THEME["primary"], activebackground=THEME["accent"],
                        font=("Impact", 15), bd=0, padx=30, pady=10, command=lambda: self.execute_round(move))
        btn.pack()
        self.canvas.create_window(x, y, window=frame)

    def execute_round(self, user_move):
        if self.is_busy: return
        self.is_busy = True
        self._animate_rng(user_move, 0)

    def _animate_rng(self, user_move, frame):
        if frame < 20:
            self.canvas.itemconfig(self.user_view, text=user_move.value[1], fill=THEME["primary"])
            self.canvas.itemconfig(self.comp_view, text=random.choice(list(Move)).value[1], fill=THEME["secondary"])
            self.canvas.itemconfig(self.hud_title, text="[ ANALYZING QUANTUM STATE ]", fill="orange")
            self.window.after(50, lambda: self._animate_rng(user_move, frame + 1))
        else:
            self._finalize(user_move)

    def _finalize(self, user_move):
        comp_move = random.choice(list(Move))
        result = GameController.get_outcome(user_move, comp_move)
        
        self.canvas.itemconfig(self.comp_view, text=comp_move.value[1])
        
        if result == "WIN":
            self.metrics["wins"] += 1
            self._trigger_vfx(275, 350, THEME["accent"])
            self.canvas.itemconfig(self.hud_title, text="SYSTEM OVERRIDE: SUCCESS", fill=THEME["accent"])
        elif result == "LOSS":
            self.metrics["losses"] += 1
            self._trigger_vfx(825, 350, THEME["secondary"])
            self.canvas.itemconfig(self.hud_title, text="CRITICAL FAILURE: CPU DOMINANT", fill=THEME["secondary"])
        else:
            self.metrics["ties"] += 1
            self.canvas.itemconfig(self.hud_title, text="SYNCHRONIZED STATE: TIE", fill="white")

        self.canvas.itemconfig(self.hud_stats, text=f"W: {self.metrics['wins']} | L: {self.metrics['losses']}")
        GameController.save_session_data(self.metrics)
        self.is_busy = False

    def _trigger_vfx(self, x, y, color):
        for _ in range(50):
            self.particles.append(VisualEffect(self.canvas, x, y, color))

    def _run_core_loop(self):
        """The 60FPS engine loop for smooth visuals."""
        self.particles = [p for p in self.particles if p.update()]
        
        # Add a subtle 'breathing' glow to the HUD
        glow = abs(math.sin(time.time() * 2)) * 0.5 + 0.5
        self.canvas.itemconfig(self.hud_stats, fill=f"#{int(255*glow):02x}{int(255*glow):02x}{int(255*glow):02x}")
        
        self.window.after(16, self._run_core_loop)

if __name__ == "__main__":
    ApexRPS()