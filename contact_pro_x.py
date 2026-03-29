import customtkinter as ctk
import json
import os
import re
from datetime import datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

DATA_FILE = "contacts_enterprise.json"


# ================= STORAGE LAYER =================

class StorageManager:

    def __init__(self):
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, "w") as f:
                json.dump([], f)

    def load(self):
        with open(DATA_FILE, "r") as f:
            return json.load(f)

    def save(self, data):
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def generate_id(self, contacts):
        return max([c["id"] for c in contacts], default=0) + 1


# ================= VALIDATION LAYER =================

class Validator:

    @staticmethod
    def validate_phone(phone):
        return re.fullmatch(r"[6-9]\d{9}", phone)

    @staticmethod
    def validate_email(email):
        return re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email)


# ================= MAIN APP =================

class ContactManagerApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Contact Manager Enterprise (No SQL)")
        self.geometry("520x700")
        self.resizable(False, False)

        self.storage = StorageManager()
        self.contacts = self.storage.load()
        self.selected_id = None

        self.create_ui()
        self.render_contacts()

    # ================= UI =================

    def create_ui(self):

        ctk.CTkLabel(
            self,
            text="CONTACT MANAGER ENTERPRISE",
            font=("Segoe UI", 20, "bold"),
            text_color="#00ffff"
        ).pack(pady=15)

        self.name_entry = ctk.CTkEntry(self, placeholder_text="Full Name")
        self.name_entry.pack(padx=20, pady=5, fill="x")

        self.phone_entry = ctk.CTkEntry(self, placeholder_text="Phone (10 digits)")
        self.phone_entry.pack(padx=20, pady=5, fill="x")

        self.email_entry = ctk.CTkEntry(self, placeholder_text="Email")
        self.email_entry.pack(padx=20, pady=5, fill="x")

        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(padx=20, pady=10, fill="x")

        ctk.CTkButton(btn_frame, text="Add", command=self.add_contact)\
            .pack(side="left", expand=True, fill="x", padx=5)

        ctk.CTkButton(btn_frame, text="Update", command=self.update_contact)\
            .pack(side="left", expand=True, fill="x", padx=5)

        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.pack()

        self.search_entry = ctk.CTkEntry(self, placeholder_text="Search by name or phone")
        self.search_entry.pack(padx=20, pady=10, fill="x")
        self.search_entry.bind("<KeyRelease>", self.search_contacts)

        self.contact_list = ctk.CTkScrollableFrame(self, height=350)
        self.contact_list.pack(padx=20, pady=10, fill="both", expand=True)

    # ================= CORE LOGIC =================

    def add_contact(self):

        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()

        if not Validator.validate_phone(phone):
            self.show_status("Invalid Phone Number", "red")
            return

        if not Validator.validate_email(email):
            self.show_status("Invalid Email", "red")
            return

        if any(c["phone"] == phone for c in self.contacts):
            self.show_status("Phone Already Exists", "orange")
            return

        if any(c["email"] == email for c in self.contacts):
            self.show_status("Email Already Exists", "orange")
            return

        new_contact = {
            "id": self.storage.generate_id(self.contacts),
            "name": name,
            "phone": phone,
            "email": email,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

        self.contacts.append(new_contact)
        self.storage.save(self.contacts)

        self.show_status("Contact Added Successfully", "green")
        self.clear_fields()
        self.render_contacts()

    def update_contact(self):

        if not self.selected_id:
            self.show_status("Select Contact First", "orange")
            return

        for contact in self.contacts:
            if contact["id"] == self.selected_id:
                contact["name"] = self.name_entry.get().strip()
                contact["phone"] = self.phone_entry.get().strip()
                contact["email"] = self.email_entry.get().strip()

        self.storage.save(self.contacts)
        self.show_status("Contact Updated", "green")
        self.clear_fields()
        self.render_contacts()

    def delete_contact(self, contact_id):

        self.contacts = [c for c in self.contacts if c["id"] != contact_id]
        self.storage.save(self.contacts)

        self.show_status("Contact Deleted", "red")
        self.render_contacts()

    # ================= RENDER =================

    def render_contacts(self):

        for widget in self.contact_list.winfo_children():
            widget.destroy()

        sorted_contacts = sorted(
            self.contacts,
            key=lambda x: x["created_at"],
            reverse=True
        )

        for contact in sorted_contacts:
            self.render_card(contact)

    def render_card(self, contact):

        frame = ctk.CTkFrame(self.contact_list)
        frame.pack(fill="x", pady=5)

        info = f"{contact['name']} | {contact['phone']} | {contact['email']}"
        ctk.CTkLabel(frame, text=info).pack(side="left", padx=10)

        ctk.CTkButton(
            frame,
            text="Edit",
            width=50,
            command=lambda c=contact: self.select_contact(c)
        ).pack(side="right", padx=5)

        ctk.CTkButton(
            frame,
            text="Delete",
            width=60,
            fg_color="red",
            command=lambda: self.delete_contact(contact["id"])
        ).pack(side="right", padx=5)

    def select_contact(self, contact):

        self.selected_id = contact["id"]

        self.name_entry.delete(0, "end")
        self.phone_entry.delete(0, "end")
        self.email_entry.delete(0, "end")

        self.name_entry.insert(0, contact["name"])
        self.phone_entry.insert(0, contact["phone"])
        self.email_entry.insert(0, contact["email"])

    # ================= SEARCH =================

    def search_contacts(self, event):

        query = self.search_entry.get().lower()

        for widget in self.contact_list.winfo_children():
            widget.destroy()

        filtered = [
            c for c in self.contacts
            if query in c["name"].lower() or query in c["phone"]
        ]

        for contact in filtered:
            self.render_card(contact)

    # ================= HELPERS =================

    def show_status(self, message, color):
        self.status_label.configure(text=message, text_color=color)

    def clear_fields(self):
        self.name_entry.delete(0, "end")
        self.phone_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.selected_id = None


# ================= RUN =================

if __name__ == "__main__":
    app = ContactManagerApp()
    app.mainloop()