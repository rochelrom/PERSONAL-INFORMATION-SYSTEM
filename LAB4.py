import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Connect to database
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Create students table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        course TEXT NOT NULL
    )
""")

conn.commit()


# Clear input fields
def clear_fields():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)


# Add student
def add_student():
    name = name_entry.get().strip()
    age = age_entry.get().strip()
    course = course_entry.get().strip()

    if name == "" or age == "" or course == "":
        messagebox.showwarning(
            "Warning",
            "Please fill in all fields."
        )
        return

    try:
        age = int(age)
        if age <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror(
            "Error",
            "Age must be a positive number."
        )
        return

    cursor.execute(
        "INSERT INTO students (name, age, course) VALUES (?, ?, ?)",
        (name, age, course)
    )

    conn.commit()

    messagebox.showinfo(
        "Success",
        "Student added successfully."
    )

    clear_fields()
    display_students()


# Display students
def display_students():
    for item in tree.get_children():
        tree.delete(item)

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    for student in students:
        tree.insert("", tk.END, values=student)


# Update student
def update_student():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select a student to update."
        )
        return

    student_id = tree.item(selected[0])["values"][0]

    name = name_entry.get().strip()
    age = age_entry.get().strip()
    course = course_entry.get().strip()

    if name == "" or age == "" or course == "":
        messagebox.showwarning(
            "Warning",
            "Please fill in all fields."
        )
        return

    try:
        age = int(age)
        if age <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror(
            "Error",
            "Age must be a positive number."
        )
        return

    cursor.execute("""
        UPDATE students
        SET name = ?, age = ?, course = ?
        WHERE id = ?
    """, (name, age, course, student_id))

    conn.commit()

    messagebox.showinfo(
        "Success",
        "Student updated successfully."
    )

    clear_fields()
    display_students()


# Delete student
def delete_student():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select a student to delete."
        )
        return

    student_id = tree.item(selected[0])["values"][0]

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this student?"
    )

    if confirm:
        cursor.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,)
        )

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Student deleted successfully."
        )

        clear_fields()
        display_students()


# Select student from table
def select_student(event):
    selected = tree.selection()

    if selected:
        student = tree.item(selected[0])["values"]

        clear_fields()

        name_entry.insert(0, student[1])
        age_entry.insert(0, student[2])
        course_entry.insert(0, student[3])


# Close application properly
def close_app():
    conn.close()
    root.destroy()


# Main window
root = tk.Tk()
root.title("Student Management System")
root.geometry("650x500")
root.configure(bg="#C9DCEB")

# Title
title_label = tk.Label(
    root,
    text="Student Management System",
    font=("Arial", 18, "bold")
)
title_label.pack(pady=15)

# Input frame
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

# Name
tk.Label(
    input_frame,
    text="Name:"
).grid(row=0, column=0, padx=5, pady=5)

name_entry = tk.Entry(input_frame, width=30)
name_entry.grid(row=0, column=1, padx=5, pady=5)

# Age
tk.Label(
    input_frame,
    text="Age:"
).grid(row=1, column=0, padx=5, pady=5)

age_entry = tk.Entry(input_frame, width=30)
age_entry.grid(row=1, column=1, padx=5, pady=5)

# Course
tk.Label(
    input_frame,
    text="Course:"
).grid(row=2, column=0, padx=5, pady=5)

course_entry = tk.Entry(input_frame, width=30)
course_entry.grid(row=2, column=1, padx=5, pady=5)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(
    button_frame,
    text="Add Student",
    command=add_student,
    width=12
).grid(row=0, column=0, padx=5)

tk.Button(
    button_frame,
    text="Update",
    command=update_student,
    width=12
).grid(row=0, column=1, padx=5)

tk.Button(
    button_frame,
    text="Delete",
    command=delete_student,
    width=12
).grid(row=0, column=2, padx=5)

tk.Button(
    button_frame,
    text="Clear",
    command=clear_fields,
    width=12
).grid(row=0, column=3, padx=5)

# Student table
table_frame = tk.Frame(root)
table_frame.pack(pady=10)

tree = ttk.Treeview(
    table_frame,
    columns=("ID", "Name", "Age", "Course"),
    show="headings",
    height=10
)

tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Age", text="Age")
tree.heading("Course", text="Course")

tree.column("ID", width=50)
tree.column("Name", width=180)
tree.column("Age", width=80)
tree.column("Course", width=180)

tree.pack()

# Bind table selection
tree.bind("<ButtonRelease-1>", select_student)

# Display existing records
display_students()

# Handle window closing
root.protocol("WM_DELETE_WINDOW", close_app)

# Run application
root.mainloop()
