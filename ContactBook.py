import tkinter as tk
from tkinter import messagebox
import json

class Contact:
    def __init__(self, name, phone_number, email, address):
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.address = address

    def __str__(self):
        return f"{self.name} - {self.phone_number}"

class ContactManager:
    def __init__(self):
        self.contacts = []
        self.load_contacts()

    def add_contact(self, contact):
        self.contacts.append(contact)
        self.save_contacts()

    def view_contacts(self):
        return self.contacts

    def search_contact(self, search_term):
        return [contact for contact in self.contacts if search_term.lower() in contact.name.lower() or search_term in contact.phone_number]

    def update_contact(self, old_name, new_contact):
        for i, contact in enumerate(self.contacts):
            if contact.name == old_name:
                self.contacts[i] = new_contact
                self.save_contacts()
                return True
        return False

    def delete_contact(self, name):
        self.contacts = [contact for contact in self.contacts if contact.name != name]
        self.save_contacts()

    def save_contacts(self):
        with open('contacts.json', 'w') as f:
            json.dump([contact.__dict__ for contact in self.contacts], f)

    def load_contacts(self):
        try:
            with open('contacts.json', 'r') as f:
                contacts_data = json.load(f)
                self.contacts = [Contact(**data) for data in contacts_data]
        except FileNotFoundError:
            self.contacts = []

class ContactApp:
    def __init__(self, root):
        self.manager = ContactManager()
        self.root = root
        self.root.title("Contact Manager")
        
        self.create_widgets()

    def create_widgets(self):
        # Add Contact
        self.add_frame = tk.Frame(self.root)
        self.add_frame.pack(pady=10)

        tk.Label(self.add_frame, text="Name").grid(row=0, column=0)
        tk.Label(self.add_frame, text="Phone").grid(row=1, column=0)
        tk.Label(self.add_frame, text="Email").grid(row=2, column=0)
        tk.Label(self.add_frame, text="Address").grid(row=3, column=0)

        self.name_entry = tk.Entry(self.add_frame)
        self.phone_entry = tk.Entry(self.add_frame)
        self.email_entry = tk.Entry(self.add_frame)
        self.address_entry = tk.Entry(self.add_frame)

        self.name_entry.grid(row=0, column=1)
        self.phone_entry.grid(row=1, column=1)
        self.email_entry.grid(row=2, column=1)
        self.address_entry.grid(row=3, column=1)

        self.add_button = tk.Button(self.add_frame, text="Add Contact", command=self.add_contact)
        self.add_button.grid(row=4, column=1, pady=5)

        # View Contacts
        self.view_frame = tk.Frame(self.root)
        self.view_frame.pack(pady=10)

        self.contact_listbox = tk.Listbox(self.view_frame, width=50, height=10)
        self.contact_listbox.pack()

        self.load_contacts()

        # Search Contact
        self.search_frame = tk.Frame(self.root)
        self.search_frame.pack(pady=10)

        tk.Label(self.search_frame, text="Search").grid(row=0, column=0)
        self.search_entry = tk.Entry(self.search_frame)
        self.search_entry.grid(row=0, column=1)

        self.search_button = tk.Button(self.search_frame, text="Search", command=self.search_contact)
        self.search_button.grid(row=0, column=2)

        # Update Contact
        self.update_frame = tk.Frame(self.root)
        self.update_frame.pack(pady=10)

        tk.Label(self.update_frame, text="Old Name").grid(row=0, column=0)
        self.old_name_entry = tk.Entry(self.update_frame)
        self.old_name_entry.grid(row=0, column=1)

        tk.Label(self.update_frame, text="New Name").grid(row=1, column=0)
        self.new_name_entry = tk.Entry(self.update_frame)
        self.new_name_entry.grid(row=1, column=1)
        tk.Label(self.update_frame, text="New Phone").grid(row=2, column=0)
        self.new_phone_entry = tk.Entry(self.update_frame)
        self.new_phone_entry.grid(row=2, column=1)
        tk.Label(self.update_frame, text="New Email").grid(row=3, column=0)
        self.new_email_entry = tk.Entry(self.update_frame)
        self.new_email_entry.grid(row=3, column=1)
        tk.Label(self.update_frame, text="New Address").grid(row=4, column=0)
        self.new_address_entry = tk.Entry(self.update_frame)
        self.new_address_entry.grid(row=4, column=1)

        self.update_button = tk.Button(self.update_frame, text="Update Contact", command=self.update_contact)
        self.update_button.grid(row=5, column=1, pady=5)

        # Delete Contact
        self.delete_frame = tk.Frame(self.root)
        self.delete_frame.pack(pady=10)

        tk.Label(self.delete_frame, text="Name to Delete").grid(row=0, column=0)
        self.delete_name_entry = tk.Entry(self.delete_frame)
        self.delete_name_entry.grid(row=0, column=1)

        self.delete_button = tk.Button(self.delete_frame, text="Delete Contact", command=self.delete_contact)
        self.delete_button.grid(row=0, column=2)

    def add_contact(self):
        name = self.name_entry.get()
        phone_number = self.phone_entry.get()
        email = self.email_entry.get()
        address = self.address_entry.get()

        if not name or not phone_number or not email or not address:
            messagebox.showwarning("Input Error", "All fields are required")
            return

        contact = Contact(name, phone_number, email, address)
        self.manager.add_contact(contact)
        self.clear_entries()
        self.load_contacts()

    def search_contact(self):
        search_term = self.search_entry.get()
        results = self.manager.search_contact(search_term)
        self.contact_listbox.delete(0, tk.END)
        for contact in results:
            self.contact_listbox.insert(tk.END, contact)

    def update_contact(self):
        old_name = self.old_name_entry.get()
        new_name = self.new_name_entry.get()
        new_phone_number = self.new_phone_entry.get()
        new_email = self.new_email_entry.get()
        new_address = self.new_address_entry.get()

        if not old_name or not new_name or not new_phone_number or not new_email or not new_address:
            messagebox.showwarning("Input Error", "All fields are required")
            return

        new_contact = Contact(new_name, new_phone_number, new_email, new_address)
        if self.manager.update_contact(old_name, new_contact):
            messagebox.showinfo("Success", "Contact updated successfully")
        else:
            messagebox.showerror("Error", "Contact not found")
        self.clear_entries()
        self.load_contacts()

    def delete_contact(self):
        name = self.delete_name_entry.get()
        if not name:
            messagebox.showwarning("Input Error", "Name is required")
            return
        self.manager.delete_contact(name)
        self.load_contacts()

    def load_contacts(self):
        self.contact_listbox.delete(0, tk.END)
        for contact in self.manager.view_contacts():
            self.contact_listbox.insert(tk.END, contact)

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.old_name_entry.delete(0, tk.END)
        self.new_name_entry.delete(0, tk.END)
        self.new_phone_entry.delete(0, tk.END)
        self.new_email_entry.delete(0, tk.END)
        self.new_address_entry.delete(0, tk.END)
        self.delete_name_entry.delete(0, tk.END)
        self.search_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactApp(root)
    root.mainloop()
