import tkinter as tk
from tkinter import messagebox

def terminal_calculator():
    print("Welcome to the Terminal Calculator!")
    try:
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
        print("Choose an operation:")
        print("1. Addition (+)")
        print("2. Subtraction (-)")
        print("3. Multiplication (*)")
        print("4. Division (/)")
        operation = input("Enter your choice (1/2/3/4): ")

        if operation == '1':
            result = num1 + num2
            print(f"The result is: {result}")
        elif operation == '2':
            result = num1 - num2
            print(f"The result is: {result}")
        elif operation == '3':
            result = num1 * num2
            print(f"The result is: {result}")
        elif operation == '4':
            if num2 != 0:
                result = num1 / num2
                print(f"The result is: {result}")
            else:
                print("Error: Division by zero is not allowed!")
        else:
            print("Invalid operation choice!")
    except ValueError:
        print("Error: Please enter valid numbers.")

def dialogbox_calculator():
    def press_key(key):
        """Handle button clicks."""
        if key == "C":
            entry_var.set("")
        elif key == "=":
            try:
                expression = entry_var.get()
                result = eval(expression)
                entry_var.set(result)
            except Exception:
                messagebox.showerror("Error", "Invalid Expression!")
        else:
            entry_var.set(entry_var.get() + key)

    # Create a Tkinter window
    root = tk.Tk()
    root.title("Calculator")
    root.geometry("250x300")  # Adjust the size of the window

    # Entry widget for display
    entry_var = tk.StringVar()
    entry = tk.Entry(
        root, textvariable=entry_var, font=("Arial", 14), bd=5, justify='right'
    )
    entry.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")

    # Button layout
    buttons = [
        ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
        ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
        ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
        ('C', 4, 0), ('0', 4, 1), ('=', 4, 2), ('+', 4, 3),
    ]

    # Add buttons to the grid
    for (text, row, col) in buttons:
        tk.Button(
            root, text=text, font=("Arial", 12), width=5, height=2,
            command=lambda t=text: press_key(t)
        ).grid(row=row, column=col, padx=2, pady=2)

    # Adjust grid layout
    for i in range(5):
        root.grid_rowconfigure(i, weight=1)
        root.grid_columnconfigure(i, weight=1)

    root.mainloop()

def main():
    print("Welcome! Choose your calculator mode:")
    print("1. Terminal")
    print("2. Dialog Box (Tkinter)")
    mode = input("Enter your choice (1/2): ")

    if mode == '1':
        terminal_calculator()
    elif mode == '2':
        dialogbox_calculator()
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
