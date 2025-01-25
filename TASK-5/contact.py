import json
import re
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font


class Contact:
    def __init__(self, name, phone, email, address):
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address

    def to_dict(self):
        return {
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "address": self.address,
        }

    @staticmethod
    def from_dict(data):
        return Contact(data["name"], data["phone"], data["email"], data["address"])


class ContactBook:
    def __init__(self, file_path="contacts.json"):
        self.file_path = file_path
        self.contacts = self.load_contacts()

    def load_contacts(self):
        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)
                return [Contact.from_dict(contact) for contact in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_contacts(self):
        with open(self.file_path, "w") as file:
            json.dump([contact.to_dict() for contact in self.contacts], file, indent=4)

    def add_contact(self, contact):
        self.contacts.append(contact)
        self.save_contacts()

    def delete_contact(self, name):
        for contact in self.contacts:
            if contact.name.lower() == name.lower():
                self.contacts.remove(contact)
                self.save_contacts()
                return True
        return False


class ContactBookApp:
    def __init__(self, root):
        self.contact_book = ContactBook()
        self.root = root
        self.root.title("Contact Notebook")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f4fa")
        self.custom_styles()
        self.create_notebook()

    def custom_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Button Styles
        style.configure(
            "RoundedButton.TButton",
            font=("Arial", 11),
            padding=6,
            relief="flat",
            background="#4CAF50",
            foreground="white",
        )
        style.map(
            "RoundedButton.TButton",
            background=[("active", "#45a049")],
            relief=[("pressed", "sunken")],
        )

        # Treeview Styles
        style.configure(
            "Treeview",
            font=("Arial", 10),
            rowheight=25,
            background="white",
            fieldbackground="white",
        )
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#e4e9f2")

    def create_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, pady=10, padx=10)

        self.create_home_tab()
        self.create_add_contact_tab()
        self.create_view_contacts_tab()

    def create_header(self, parent, text):
        header_frame = tk.Frame(parent, bg="#f7f9fc")
        header_frame.pack(fill="x", pady=5)
        header_label = tk.Label(
            header_frame,
            text=text,
            font=("Arial", 16, "bold"),
            bg="#f7f9fc",
            fg="#333",
        )
        header_label.pack(pady=10)

    def create_home_tab(self):
        home_frame = ttk.Frame(self.notebook)
        self.notebook.add(home_frame, text="Home")

        self.create_header(home_frame, "Welcome to Your Contact Notebook!")

        tk.Label(
            home_frame,
            text="Manage your contacts easily and efficiently.",
            font=("Arial", 12),
            bg="#f0f4fa",
        ).pack(pady=20)

    def create_add_contact_tab(self):
        add_frame = ttk.Frame(self.notebook)
        self.notebook.add(add_frame, text="Add Contact")

        self.create_header(add_frame, "Add a New Contact")

        form_frame = ttk.Frame(add_frame)
        form_frame.pack(pady=20)

        # Input Fields
        fields = [("Name:", "name_entry"), ("Phone:", "phone_entry"), ("Email:", "email_entry"), ("Address:", "address_entry")]
        for i, (label_text, var_name) in enumerate(fields):
            ttk.Label(form_frame, text=label_text, font=("Arial", 11)).grid(row=i, column=0, padx=10, pady=10, sticky="w")
            setattr(self, var_name, ttk.Entry(form_frame, width=40))
            getattr(self, var_name).grid(row=i, column=1, padx=10, pady=10)

        ttk.Button(
            add_frame,
            text="Add Contact",
            style="RoundedButton.TButton",
            command=self.add_contact,
        ).pack(pady=10)

    def create_view_contacts_tab(self):
        view_frame = ttk.Frame(self.notebook)
        self.notebook.add(view_frame, text="View Contacts")

        self.create_header(view_frame, "Your Contact List")

        self.tree = ttk.Treeview(view_frame, columns=("Name", "Phone", "Email", "Address"), show="headings", height=15)
        self.tree.heading("Name", text="Name")
        self.tree.heading("Phone", text="Phone")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Address", text="Address")
        self.tree.column("Name", width=150)
        self.tree.column("Phone", width=100)
        self.tree.column("Email", width=200)
        self.tree.column("Address", width=200)
        self.tree.tag_configure("odd", background="#f9f9f9")
        self.tree.tag_configure("even", background="#ffffff")
        self.tree.pack(pady=10, padx=10, fill="both", expand=True)

        ttk.Button(
            view_frame,
            text="Delete Selected",
            style="RoundedButton.TButton",
            command=self.delete_selected_contact,
        ).pack(pady=10)

        self.load_contacts_into_tree()

    def add_contact(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_entry.get().strip()

        if not name or not phone or not email:
            messagebox.showwarning("Input Error", "Name, Phone, and Email are required!")
            return

        if not re.fullmatch(r"\d{10}", phone):
            messagebox.showwarning("Input Error", "Phone must be a valid 10-digit number!")
            return

        if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showwarning("Input Error", "Email must be valid!")
            return

        contact = Contact(name, phone, email, address)
        self.contact_book.add_contact(contact)
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.load_contacts_into_tree()
        messagebox.showinfo("Success", "Contact added successfully!")

    def load_contacts_into_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for i, contact in enumerate(self.contact_book.contacts):
            tag = "odd" if i % 2 == 0 else "even"
            self.tree.insert("", "end", values=(contact.name, contact.phone, contact.email, contact.address), tags=(tag,))

    def delete_selected_contact(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "No contact selected!")
            return

        selected_contact = self.tree.item(selected_item)["values"]
        name = selected_contact[0]

        if self.contact_book.delete_contact(name):
            self.tree.delete(selected_item)
            messagebox.showinfo("Success", "Contact deleted successfully!")
        else:
            messagebox.showwarning("Error", "Failed to delete contact!")


if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBookApp(root)
    root.mainloop()
