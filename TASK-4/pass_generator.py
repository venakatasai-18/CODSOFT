import random
import string
import tkinter as tk
from tkinter import ttk, messagebox

def generate_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def generate_password_event():
    try:
        # Get the entered length from the input field
        length = int(length_entry.get())
        if length <= 0:
            result_label.config(text="Length must be a positive number.", fg="red")
            return

        # Generate password
        password = generate_password(length)

        # Get the selected output option
        output_option = output_var.get()
        
        if output_option == "Terminal":
            print(f"Generated Password: {password}")
            result_label.config(text="Password displayed in terminal.", fg="green")
        elif output_option == "Dialog Box":
            messagebox.showinfo("Generated Password", f"Password: {password}")
            result_label.config(text="Password displayed in dialog box.", fg="green")
        else:
            result_label.config(text="Please select an output method.", fg="red")

    except ValueError:
        result_label.config(text="Please enter a valid number.", fg="red")

# Create the main tkinter window
root = tk.Tk()
root.title("Password Generator")
root.geometry("500x350")
root.resizable(False, False)
root.configure(bg="#f9f9f9")

# Create a stylish header
header_label = tk.Label(root, text="🔒 Secure Password Generator", font=("Helvetica", 16, "bold"), bg="#f9f9f9", fg="#2c3e50")
header_label.pack(pady=15)

# Create a separator
separator = ttk.Separator(root, orient="horizontal")
separator.pack(fill="x", padx=20, pady=5)

# Create the input field for password length
length_label = tk.Label(root, text="Enter Password Length:", font=("Helvetica", 12), bg="#f9f9f9", fg="#34495e")
length_label.pack(pady=5)

length_entry = ttk.Entry(root, width=35)
length_entry.pack(pady=5)

# Create the dropdown menu to select output method
output_var = tk.StringVar(value="Select Output")
output_label = tk.Label(root, text="Select Output Method:", font=("Helvetica", 12), bg="#f9f9f9", fg="#34495e")
output_label.pack(pady=5)

output_menu = ttk.Combobox(root, textvariable=output_var, state="readonly", values=["Terminal", "Dialog Box"], width=32)
output_menu.pack(pady=5)

# Create the button to generate password
generate_button = ttk.Button(root, text="Generate Password", command=generate_password_event)
generate_button.pack(pady=20)

# Create the label to display the result
result_label = tk.Label(root, text="", font=("Helvetica", 10, "italic"), bg="#f9f9f9", wraplength=450, fg="#16a085")
result_label.pack(pady=10)

# Add a footer
footer_label = tk.Label(root, text="Your passwords are safe with us!", font=("Helvetica", 10, "italic"), bg="#f9f9f9", fg="#7f8c8d")
footer_label.pack(side="bottom", pady=10)

# Add a decorative border to the window
root.update_idletasks()
root.config(highlightbackground="#bdc3c7", highlightthickness=2)

# Run the tkinter event loop
root.mainloop()
