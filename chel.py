import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# ==========================================
# DATABASE CONFIGURATION
# ==========================================

DB_NAME = "reservations.db"


def connect_db():
    return sqlite3.connect(DB_NAME)


def create_table():
    with connect_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS reservations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                reservation_date TEXT NOT NULL,
                reservation_time TEXT NOT NULL,
                guests INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'Pending',
                notes TEXT
            )
        """)


# ==========================================
# RESERVATION SYSTEM
# ==========================================

class ReservationSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Reservation Management System")
        self.root.geometry("1150x700")
        self.root.minsize(950, 600)

        self.selected_id = None

        self.create_widgets()
        self.load_reservations()

    # --------------------------------------
    # CREATE GUI
    # --------------------------------------

    def create_widgets(self):
        title = tk.Label(
            self.root,
            text="RESERVATION MANAGEMENT SYSTEM",
            font=("Arial", 20, "bold"),
            bg="#1F4E78",
            fg="white",
            pady=15
        )
        title.pack(fill="x")

        # Input form
        form = ttk.LabelFrame(
            self.root, text="Reservation Details", padding=12
        )
        form.pack(fill="x", padx=15, pady=10)

        ttk.Label(form, text="Customer Name:").grid(
            row=0, column=0, sticky="w", padx=5, pady=5
        )
        self.name_entry = ttk.Entry(form, width=28)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form, text="Phone Number:").grid(
            row=0, column=2, sticky="w", padx=5, pady=5
        )
        self.phone_entry = ttk.Entry(form, width=25)
        self.phone_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form, text="Date (YYYY-MM-DD):").grid(
            row=1, column=0, sticky="w", padx=5, pady=5
        )
        self.date_entry = ttk.Entry(form, width=28)
        self.date_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form, text="Time (HH:MM, 24-hour):").grid(
            row=1, column=2, sticky="w", padx=5, pady=5
        )
        self.time_entry = ttk.Entry(form, width=25)
        self.time_entry.grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(form, text="Number of Guests:").grid(
            row=2, column=0, sticky="w", padx=5, pady=5
        )
        self.guests_entry = ttk.Entry(form, width=28)
        self.guests_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form, text="Status:").grid(
            row=2, column=2, sticky="w", padx=5, pady=5
        )
        self.status_box = ttk.Combobox(
            form,
            values=["Pending", "Confirmed", "Cancelled", "Completed"],
            state="readonly",
            width=22
        )
        self.status_box.grid(row=2, column=3, padx=5, pady=5)
        self.status_box.set("Pending")

        ttk.Label(form, text="Notes:").grid(
            row=3, column=0, sticky="w", padx=5, pady=5
        )
        self.notes_entry = ttk.Entry(form, width=75)
        self.notes_entry.grid(
            row=3, column=1, columnspan=3,
            sticky="ew", padx=5, pady=5
        )

        # Buttons
        buttons = ttk.Frame(self.root)
        buttons.pack(fill="x", padx=15, pady=5)

        ttk.Button(
            buttons, text="Add Reservation",
            command=self.add_reservation
        ).pack(side="left", padx=4)

        ttk.Button(
            buttons, text="Update Selected",
            command=self.update_reservation
        ).pack(side="left", padx=4)

        ttk.Button(
            buttons, text="Delete Selected",
            command=self.delete_reservation
        ).pack(side="left", padx=4)

        ttk.Button(
            buttons, text="Clear Form",
            command=self.clear_form
        ).pack(side="left", padx=4)

        # Search
        search_frame = ttk.LabelFrame(
            self.root, text="Search Reservations", padding=10
        )
        search_frame.pack(fill="x", padx=15, pady=8)

        ttk.Label(
            search_frame, text="Name or Reservation ID:"
        ).pack(side="left", padx=5)

        self.search_entry = ttk.Entry(search_frame, width=35)
        self.search_entry.pack(side="left", padx=5)

        ttk.Button(
            search_frame, text="Search",
            command=self.search_reservations
        ).pack(side="left", padx=4)

        ttk.Button(
            search_frame, text="Show All",
            command=self.load_reservations
        ).pack(side="left", padx=4)

        # Reservation table
        table_frame = ttk.LabelFrame(
            self.root, text="Reservation Records", padding=10
        )
        table_frame.pack(
            fill="both", expand=True, padx=15, pady=(0, 12)
        )

        columns = (
            "id", "name", "phone", "date",
            "time", "guests", "status", "notes"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=12
        )

        headings = {
            "id": "ID",
            "name": "Customer Name",
            "phone": "Phone",
            "date": "Date",
            "time": "Time",
            "guests": "Guests",
            "status": "Status",
            "notes": "Notes"
        }

        widths = {
            "id": 45, "name": 160, "phone": 110,
            "date": 100, "time": 75, "guests": 60,
            "status": 95, "notes": 200
        }

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(
                col, width=widths[col], anchor="center"
            )

        scrollbar_y = ttk.Scrollbar(
            table_frame, orient="vertical",
            command=self.tree.yview
        )
        scrollbar_x = ttk.Scrollbar(
            table_frame, orient="horizontal",
            command=self.tree.xview
        )

        self.tree.configure(
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        self.tree.bind(
            "<<TreeviewSelect>>", self.select_reservation
        )

        self.count_label = ttk.Label(
            self.root, text="Total reservations: 0"
        )
        self.count_label.pack(anchor="w", padx=20, pady=(0, 8))

    # --------------------------------------
    # VALIDATE INPUT
    # --------------------------------------

    def get_form_data(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        date = self.date_entry.get().strip()
        time = self.time_entry.get().strip()
        guests_text = self.guests_entry.get().strip()
        status = self.status_box.get()
        notes = self.notes_entry.get().strip()

        if not name or not phone or not date or not time:
            messagebox.showwarning(
                "Missing Information",
                "Please complete the name, phone, date, and time."
            )
            return None

        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror(
                "Invalid Date",
                "Enter a valid date in YYYY-MM-DD format."
            )
            return None

        try:
            datetime.strptime(time, "%H:%M")
        except ValueError:
            messagebox.showerror(
                "Invalid Time",
                "Enter a valid time in 24-hour HH:MM format."
            )
            return None

        try:
            guests = int(guests_text)
            if guests < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Invalid Guests",
                "Number of guests must be a positive integer."
            )
            return None

        return (
            name, phone, date, time, guests, status, notes
        )

    # --------------------------------------
    # ADD RESERVATION
    # --------------------------------------

    def add_reservation(self):
        data = self.get_form_data()
        if data is None:
            return

        try:
            with connect_db() as conn:
                conn.execute("""
                    INSERT INTO reservations
                    (customer_name, phone, reservation_date,
                     reservation_time, guests, status, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, data)

            messagebox.showinfo(
                "Success", "Reservation added successfully."
            )
            self.clear_form()
            self.load_reservations()

        except sqlite3.Error as error:
            messagebox.showerror("Database Error", str(error))

    # --------------------------------------
    # DISPLAY RESERVATIONS
    # --------------------------------------

    def load_reservations(self):
        self.display_records()

    def display_records(self, query=None, params=()):
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            with connect_db() as conn:
                if query:
                    rows = conn.execute(
                        query, params
                    ).fetchall()
                else:
                    rows = conn.execute("""
                        SELECT id, customer_name, phone,
                               reservation_date, reservation_time,
                               guests, status, notes
                        FROM reservations
                        ORDER BY reservation_date, reservation_time
                    """).fetchall()

            for row in rows:
                self.tree.insert("", "end", values=row)

            self.count_label.config(
                text=f"Total reservations: {len(rows)}"
            )

        except sqlite3.Error as error:
            messagebox.showerror("Database Error", str(error))

    # --------------------------------------
    # SEARCH RESERVATIONS
    # --------------------------------------

    def search_reservations(self):
        keyword = self.search_entry.get().strip()

        if not keyword:
            self.load_reservations()
            return

        if keyword.isdigit():
            query = """
                SELECT id, customer_name, phone,
                       reservation_date, reservation_time,
                       guests, status, notes
                FROM reservations
                WHERE customer_name LIKE ? OR id = ?
                ORDER BY reservation_date, reservation_time
            """
            params = (f"%{keyword}%", int(keyword))
        else:
            query = """
                SELECT id, customer_name, phone,
                       reservation_date, reservation_time,
                       guests, status, notes
                FROM reservations
                WHERE customer_name LIKE ?
                ORDER BY reservation_date, reservation_time
            """
            params = (f"%{keyword}%",)

        self.display_records(query, params)

    # --------------------------------------
    # SELECT RECORD
    # --------------------------------------

    def select_reservation(self, event=None):
        selected = self.tree.selection()

        if not selected:
            return

        values = self.tree.item(selected[0], "values")
        self.selected_id = int(values[0])

        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, values[1])

        self.phone_entry.delete(0, tk.END)
        self.phone_entry.insert(0, values[2])

        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, values[3])

        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, values[4])

        self.guests_entry.delete(0, tk.END)
        self.guests_entry.insert(0, values[5])

        self.status_box.set(values[6])

        self.notes_entry.delete(0, tk.END)
        self.notes_entry.insert(0, values[7] or "")

    # --------------------------------------
    # UPDATE RESERVATION
    # --------------------------------------

    def update_reservation(self):
        if self.selected_id is None:
            messagebox.showwarning(
                "No Selection",
                "Select a reservation from the table first."
            )
            return

        data = self.get_form_data()
        if data is None:
            return

        if not messagebox.askyesno(
            "Confirm Update",
            "Do you want to update this reservation?"
        ):
            return

        try:
            with connect_db() as conn:
                conn.execute("""
                    UPDATE reservations
                    SET customer_name = ?,
                        phone = ?,
                        reservation_date = ?,
                        reservation_time = ?,
                        guests = ?,
                        status = ?,
                        notes = ?
                    WHERE id = ?
                """, data + (self.selected_id,))

            messagebox.showinfo(
                "Success", "Reservation updated successfully."
            )
            self.clear_form()
            self.load_reservations()

        except sqlite3.Error as error:
            messagebox.showerror("Database Error", str(error))

    # --------------------------------------
    # DELETE RESERVATION
    # --------------------------------------

    def delete_reservation(self):
        if self.selected_id is None:
            messagebox.showwarning(
                "No Selection",
                "Select a reservation from the table first."
            )
            return

        if not messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this reservation?"
        ):
            return

        try:
            with connect_db() as conn:
                conn.execute(
                    "DELETE FROM reservations WHERE id = ?",
                    (self.selected_id,)
                )

            messagebox.showinfo(
                "Success", "Reservation deleted successfully."
            )
            self.clear_form()
            self.load_reservations()

        except sqlite3.Error as error:
            messagebox.showerror("Database Error", str(error))

    # --------------------------------------
    # CLEAR FORM
    # --------------------------------------

    def clear_form(self):
        self.selected_id = None

        for entry in (
            self.name_entry,
            self.phone_entry,
            self.date_entry,
            self.time_entry,
            self.guests_entry,
            self.notes_entry,
            self.search_entry
        ):
            entry.delete(0, tk.END)

        self.status_box.set("Pending")

        for item in self.tree.selection():
            self.tree.selection_remove(item)


# ==========================================
# START APPLICATION
# ==========================================

if __name__ == "__main__":
    create_table()

    root = tk.Tk()
    app = ReservationSystem(root)
    root.mainloop()
