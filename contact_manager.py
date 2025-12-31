import tkinter as tk
from tkinter import messagebox
import json
import os

FILE = "contacts.json"


def load_contacts():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return []


def save_contacts():
    with open(FILE, "w") as f:
        json.dump(contact_list, f, indent=4)


def refresh_contacts():
    contact_box.delete(0, tk.END)
    for contact in contact_list:
        contact_box.insert(tk.END, contact["name"])


def clear_inputs():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)


def add_contact():
    name = name_entry.get().strip()
    phone = phone_entry.get().strip()
    email = email_entry.get().strip()

    if not name or not phone or not email:
        messagebox.showerror("Error", "Please fill all fields")
        return

    contact_list.append({
        "name": name,
        "phone": phone,
        "email": email
    })

    save_contacts()
    refresh_contacts()
    clear_inputs()


def select_contact(event):
    if not contact_box.curselection():
        return

    index = contact_box.curselection()[0]
    contact = contact_list[index]

    clear_inputs()
    name_entry.insert(0, contact["name"])
    phone_entry.insert(0, contact["phone"])
    email_entry.insert(0, contact["email"])


def update_contact():
    if not contact_box.curselection():
        messagebox.showerror("Error", "Select a contact to update")
        return

    index = contact_box.curselection()[0]

    contact_list[index]["name"] = name_entry.get()
    contact_list[index]["phone"] = phone_entry.get()
    contact_list[index]["email"] = email_entry.get()

    save_contacts()
    refresh_contacts()


def delete_contact():
    if not contact_box.curselection():
        messagebox.showerror("Error", "Select a contact to delete")
        return

    index = contact_box.curselection()[0]
    contact_list.pop(index)

    save_contacts()
    refresh_contacts()
    clear_inputs()


# ---------------- GUI ----------------

window = tk.Tk()
window.title("Contact Manager")
window.geometry("780x460")
window.resizable(False, False)
window.configure(bg="#0f172a")

# main card
card = tk.Frame(window, bg="#020617", padx=25, pady=25)
card.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(
    card,
    text="📇 Contact Management System",
    font=("Segoe UI", 20, "bold"),
    bg="#020617",
    fg="white"
).grid(row=0, column=0, columnspan=3, pady=(0, 15))

# input section
tk.Label(card, text="Name", bg="#020617", fg="#94a3b8").grid(row=1, column=0, sticky="w")
name_entry = tk.Entry(card, width=30)
name_entry.grid(row=1, column=1, pady=5)

tk.Label(card, text="Phone", bg="#020617", fg="#94a3b8").grid(row=2, column=0, sticky="w")
phone_entry = tk.Entry(card, width=30)
phone_entry.grid(row=2, column=1, pady=5)

tk.Label(card, text="Email", bg="#020617", fg="#94a3b8").grid(row=3, column=0, sticky="w")
email_entry = tk.Entry(card, width=30)
email_entry.grid(row=3, column=1, pady=5)

# buttons
btn_frame = tk.Frame(card, bg="#020617")
btn_frame.grid(row=4, column=0, columnspan=2, pady=12)

def ui_button(text, cmd, color):
    return tk.Button(
        btn_frame,
        text=text,
        command=cmd,
        bg=color,
        fg="white",
        width=10,
        relief="flat",
        cursor="hand2"
    )

ui_button("Add", add_contact, "#2563eb").grid(row=0, column=0, padx=5)
ui_button("Update", update_contact, "#16a34a").grid(row=0, column=1, padx=5)
ui_button("Delete", delete_contact, "#dc2626").grid(row=0, column=2, padx=5)

# contact list section
tk.Label(
    card,
    text="Saved Contacts",
    bg="#020617",
    fg="#94a3b8",
    font=("Segoe UI", 11)
).grid(row=1, column=2, sticky="w", padx=20)

contact_box = tk.Listbox(
    card,
    width=35,
    height=12,
    font=("Segoe UI", 10)
)
contact_box.grid(row=2, column=2, rowspan=3, padx=20)
contact_box.bind("<<ListboxSelect>>", select_contact)

# load existing contacts
contact_list = load_contacts()
refresh_contacts()

window.mainloop()
