import customtkinter as ctk
import json
import os
from datetime import datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

DATA_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

class TodoApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Todo Pro X")
        self.geometry("900x600")

        self.tasks = load_tasks()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_main_area()

        self.refresh_tasks()

    # ================= SIDEBAR =================

    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        ctk.CTkLabel(self.sidebar,
                     text="Todo Pro X",
                     font=("Arial", 20, "bold")).pack(pady=30)

        ctk.CTkButton(self.sidebar,
                      text="All Tasks",
                      command=self.refresh_tasks).pack(pady=10, fill="x", padx=20)

        ctk.CTkButton(self.sidebar,
                      text="Completed",
                      command=lambda: self.filter_tasks("Completed")
                      ).pack(pady=10, fill="x", padx=20)

        ctk.CTkButton(self.sidebar,
                      text="Pending",
                      command=lambda: self.filter_tasks("Pending")
                      ).pack(pady=10, fill="x", padx=20)

    # ================= MAIN AREA =================

    def create_main_area(self):
        self.main = ctk.CTkFrame(self)
        self.main.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.task_entry = ctk.CTkEntry(self.main,
                                       placeholder_text="Enter task...")
        self.task_entry.pack(pady=10, fill="x")

        self.priority_option = ctk.CTkOptionMenu(
            self.main,
            values=["Low", "Medium", "High"]
        )
        self.priority_option.pack(pady=10)

        ctk.CTkButton(self.main,
                      text="Add Task",
                      command=self.add_task).pack(pady=10)

        self.task_container = ctk.CTkScrollableFrame(self.main)
        self.task_container.pack(fill="both", expand=True, pady=10)

    # ================= LOGIC =================

    def refresh_tasks(self):
        for widget in self.task_container.winfo_children():
            widget.destroy()

        for task in self.tasks:
            self.create_task_widget(task)

    def filter_tasks(self, status):
        for widget in self.task_container.winfo_children():
            widget.destroy()

        for task in self.tasks:
            if task["status"] == status:
                self.create_task_widget(task)

    def create_task_widget(self, task):
        frame = ctk.CTkFrame(self.task_container)
        frame.pack(fill="x", pady=5)

        color = "green" if task["status"] == "Completed" else "orange"

        label = ctk.CTkLabel(frame,
                             text=f"{task['title']} | {task['priority']} | {task['created']}",
                             text_color=color)
        label.pack(side="left", padx=10)

        complete_btn = ctk.CTkButton(frame,
                                     text="✔",
                                     width=40,
                                     command=lambda: self.mark_complete(task))
        complete_btn.pack(side="right", padx=5)

        delete_btn = ctk.CTkButton(frame,
                                   text="✖",
                                   width=40,
                                   fg_color="red",
                                   command=lambda: self.delete_task(task))
        delete_btn.pack(side="right")

    def add_task(self):
        title = self.task_entry.get().strip()
        priority = self.priority_option.get()

        if not title:
            return

        new_task = {
            "title": title,
            "priority": priority,
            "status": "Pending",
            "created": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

        self.tasks.append(new_task)
        save_tasks(self.tasks)

        self.task_entry.delete(0, "end")
        self.refresh_tasks()

    def mark_complete(self, task):
        task["status"] = "Completed"
        save_tasks(self.tasks)
        self.refresh_tasks()

    def delete_task(self, task):
        self.tasks.remove(task)
        save_tasks(self.tasks)
        self.refresh_tasks()


if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()