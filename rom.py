import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

#DATABASE
CREATE TABLE IF NOT EXISTS person_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    city TEXT NOT NULL,
    age INTEGER NOT NULL,
    occupation TEXT NOT NULL
"")

conn.commit()

root = tk.Tk()
root.title("Person Profile Management System")
root.geometry("70x500")

title.label.pack(pady=10)

input_frame = tk.Frame(root)
input_frame.pack(pady=10)

#FULL NAME
tk.Label (
    input_frame,
    text = "Full Name:"
).grid(row = 1, column=0, padx=5, pady=5)
name_entry=tk.Entry(input_frame, width=30)
name_entry.grid(row=0, column=1, padx=5, pady=5)
    
#EMAIL ADDRESS
tk.Label (
    input_frame,
    text = "Email Address:"
).grid(row=1, column=0, padx=5, pady=5)
email_address_entry = tk.Entry(input_frame, width=30)
email_address.grid(row=1, column=1, padx=5, pady=5)
    
#PHONE NUMBER
tk.Label (
    input_frame,
    int = "Phone Number"
).grid(row=1, column=0, padx=5, pady=5)
phone_number_entry = tk.Entry(input_frame, width=30)
phone_number_entry.grid(row=1, column=1, padx=5, pady=5)
