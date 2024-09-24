import random
import string
import tkinter as tk
from tkinter import messagebox

def generate_password():
    length = password_length.get()
    if length <= 0:
        messagebox.showerror("Error", "Password length must be greater than 0")
        return
    
    characters = ''
    if var_letters.get():
        characters += string.ascii_letters
    if var_numbers.get():
        characters += string.digits
    if var_symbols.get():
        characters += string.punctuation

    if not characters:
        messagebox.showerror("Error", "Select at least one character type")
        return
    
    password = ''.join(random.choice(characters) for i in range(length))
    password_display.delete(0, tk.END)
    password_display.insert(0, password)
    
    # Copy password to clipboard
    root.clipboard_clear()
    root.clipboard_append(password)

def validate_length(new_value):
    try:
        return new_value.isdigit() or new_value == ""
    except ValueError:
        return False

# GUI setup
root = tk.Tk()
root.title("Random Password Generator")

tk.Label(root, text="Password Length:").grid(row=0, column=0)
password_length = tk.IntVar()
password_length_entry = tk.Entry(root, textvariable=password_length, validate="key", validatecommand=(root.register(validate_length), "%P"))
password_length_entry.grid(row=0, column=1)

var_letters = tk.BooleanVar(value=True)
var_numbers = tk.BooleanVar(value=True)
var_symbols = tk.BooleanVar(value=True)

tk.Checkbutton(root, text="Include Letters", variable=var_letters).grid(row=1, column=0)
tk.Checkbutton(root, text="Include Numbers", variable=var_numbers).grid(row=1, column=1)
tk.Checkbutton(root, text="Include Symbols", variable=var_symbols).grid(row=2, column=0)

tk.Button(root, text="Generate Password", command=generate_password).grid(row=3, column=0, columnspan=2)

password_display = tk.Entry(root, width=30)
password_display.grid(row=4, column=0, columnspan=2)

root.mainloop()
