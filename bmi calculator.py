import tkinter as tk
from tkinter import messagebox
import mysql.connector
import matplotlib.pyplot as plt

# BMI calculator functions

def calculate_bmi(weight, height):
    return weight / height**2

def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi <= 24.9:
        return "Normal weight"
    elif 25 <= bmi <= 29.9:
        return "Overweight"
    else:
        return "Obese"

# Database connection setup
def setup_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  
            password="soyamsidh#121603",  
            database="bmi_database"
        )
        cursor = conn.cursor()
        # Ensure the table exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bmi_records (
                id INT AUTO_INCREMENT PRIMARY KEY,
                weight FLOAT NOT NULL,
                height FLOAT NOT NULL,
                bmi FLOAT NOT NULL,
                category VARCHAR(50)
            )
        ''')
        conn.commit()
        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error connecting to MySQL: {err}")

# Store data in the MySQL database
def store_data(weight, height, bmi, category):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  
            password="soyamsidh#121603",  
            database="bmi_database"
        )
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO bmi_records (weight, height, bmi, category)
            VALUES (%s, %s, %s, %s)
        ''', (weight, height, bmi, category))
        conn.commit()
        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Failed to store data: {err}")


def show_history():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  
            password="soyamsidh#121603",  
            database="bmi_database"
        )
        cursor = conn.cursor()
        cursor.execute('SELECT id, bmi, category FROM bmi_records')
        data = cursor.fetchall()
        conn.close()
        
        if not data:
            messagebox.showinfo("No Data", "No BMI records found.")
            return
        
        # Plot BMI history
        ids = [record[0] for record in data]
        bmis = [record[1] for record in data]
        categories = [record[2] for record in data]
        
        plt.figure(figsize=(10, 5))
        plt.plot(ids, bmis, marker='o')
        plt.title("BMI History")
        plt.xlabel("Entry ID")
        plt.ylabel("BMI")
        for i, category in enumerate(categories):
            plt.text(ids[i], bmis[i], category, fontsize=9)
        
        plt.grid(True)
        plt.show()

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Failed to retrieve data: {err}")

# Main function for calculating and displaying BMI
def calculate_and_display():
    try:
        weight = float(entry_weight.get())
        height = float(entry_height.get())
        
        if weight <= 0 or height <= 0:
            messagebox.showerror("Error", "Weight and Height cannot be negative or zero.")
            return
        
        bmi = calculate_bmi(weight, height)
        category = classify_bmi(bmi)
        
        result_label.config(text=f"BMI: {bmi:.2f}\nCategory: {category}")
        
        store_data(weight, height, bmi, category)
        messagebox.showinfo("Success", "BMI data stored successfully!")
    
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values for weight and height.")

# GUI setup
root = tk.Tk()
root.title("BMI Calculator")

tk.Label(root, text="Enter your weight (kg):").grid(row=0, column=0)
entry_weight = tk.Entry(root)
entry_weight.grid(row=0, column=1)

tk.Label(root, text="Enter your height (m):").grid(row=1, column=0)
entry_height = tk.Entry(root)
entry_height.grid(row=1, column=1)

# Calculate BMI button
calculate_button = tk.Button(root, text="Calculate BMI", command=calculate_and_display)
calculate_button.grid(row=2, column=0, columnspan=2)

# Label for displaying result
result_label = tk.Label(root, text="")
result_label.grid(row=3, column=0, columnspan=2)

# History button to show historical BMI data
history_button = tk.Button(root, text="Show History", command=show_history)
history_button.grid(row=4, column=0, columnspan=2)

# Setup the database on start
setup_database()

# Start the GUI
root.mainloop()
