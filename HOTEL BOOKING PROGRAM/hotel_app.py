import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import date, datetime
class HotelManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Booking Management System")
        self.root.geometry("900x600")
        self.db_name = "hotel.db"
        self.setup_database()
        self.bg_color = "#f0f0f0"
        self.root.configure(bg=self.bg_color)
        style=ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", background=self.bg_color, font=("Arial", 10))
        style.configure("TButton", font=("Arial", 10, "bold"))
        style.configure("Accent.TButton", font=("Arial", 10, "bold"), background="#4CAF50", foreground="white")
        title_lbl=tk.Label(self.root, text="Hotel Booking System", font=("Arial", 20, "bold"), bg=self.bg_color, fg="#333")
        title_lbl.pack(pady=10)
        main_frame=tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        input_frame=tk.LabelFrame(main_frame, text="New Booking / Check-In", bg=self.bg_color, font=("Arial", 12, "bold"))
        input_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        self.guest_name_var=tk.StringVar()
        self.phone_var=tk.StringVar()
        self.days_var=tk.IntVar(value=1)
        self.selected_room_var=tk.StringVar()
        tk.Label(input_frame, text="Guest Name:", bg=self.bg_color).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(input_frame, textvariable=self.guest_name_var).grid(row=0, column=1, padx=5, pady=5)
        tk.Label(input_frame, text="Phone No:", bg=self.bg_color).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(input_frame, textvariable=self.phone_var).grid(row=1, column=1, padx=5, pady=5)
        tk.Label(input_frame, text="Available Rooms:", bg=self.bg_color).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.room_combo = ttk.Combobox(input_frame, textvariable=self.selected_room_var, state="readonly")
        self.room_combo.grid(row=2, column=1, padx=5, pady=5)
        tk.Label(input_frame, text="Stay Duration (Days):", bg=self.bg_color).grid(row=3, column=0, padx=5, pady=5, sticky="w")
        ttk.Spinbox(input_frame, from_=1, to=30, textvariable=self.days_var, width=5).grid(row=3, column=1, padx=5, pady=5, sticky="w")
        btn_frame = tk.Frame(input_frame, bg=self.bg_color)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)
        ttk.Button(btn_frame, text="Book Room", command=self.book_room).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear Form", command=self.clear_form).pack(side=tk.LEFT, padx=5)
        view_frame = tk.LabelFrame(main_frame, text="Current Bookings", bg=self.bg_color, font=("Arial", 12, "bold"))
        view_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        columns=("booking_id", "guest_name", "phone", "room_no", "check_in", "days")
        self.tree=ttk.Treeview(view_frame, columns=columns, show="headings")
        self.tree.heading("booking_id", text="ID")
        self.tree.heading("guest_name", text="Guest Name")
        self.tree.heading("phone", text="Phone")
        self.tree.heading("room_no", text="Room No")
        self.tree.heading("check_in", text="Check-In Date")
        self.tree.heading("days", text="Days")
        self.tree.column("booking_id", width=30, anchor="center")
        self.tree.column("guest_name", width=150)
        self.tree.column("phone", width=100)
        self.tree.column("room_no", width=70, anchor="center")
        self.tree.column("check_in", width=90, anchor="center")
        self.tree.column("days", width=50, anchor="center")
        scrollbar = ttk.Scrollbar(view_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)
        checkout_btn=ttk.Button(view_frame, text="Check Out Selected Guest", command=self.checkout_guest, style="Accent.TButton")
        checkout_btn.pack(pady=10, anchor="e")
        self.refresh_room_combo()
        self.view_bookings()
    def run_query(self, query, parameters=()):
        """Helper function to handle DB connections and execute single queries."""
        with sqlite3.connect(self.db_name) as conn:
            cursor=conn.cursor()
            cursor.execute(query, parameters) 
            conn.commit()
            return cursor
    def setup_database(self):
        """Creates tables if they don't exist and adds dummy rooms."""
        sql_rooms = """
            CREATE TABLE IF NOT EXISTS rooms (
                room_no INTEGER PRIMARY KEY,
                type TEXT NOT NULL,
                price REAL NOT NULL,
                status TEXT NOT NULL DEFAULT 'Available'
            )
        """
        sql_bookings = """
            CREATE TABLE IF NOT EXISTS bookings (
                booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
                guest_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                room_no INTEGER,
                check_in_date TEXT NOT NULL,
                stay_days INTEGER NOT NULL,
                FOREIGN KEY (room_no) REFERENCES rooms(room_no)
            )
        """
        self.run_query(sql_rooms)
        self.run_query(sql_bookings)
        cursor=self.run_query("SELECT count(*) FROM rooms")
        if cursor.fetchone()[0]==0:
            dummy_rooms=[
                (101, 'Single', 50.0, 'Available'),
                (102, 'Single', 50.0, 'Available'),
                (103, 'Double', 80.0, 'Available'),
                (201, 'Double', 85.0, 'Available'),
                (202, 'Deluxe', 120.0, 'Available'),
                (301, 'Suite', 200.0, 'Available'),
            ]
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.executemany("INSERT INTO rooms VALUES (?, ?, ?, ?)", dummy_rooms)
                conn.commit()
            print("Dummy rooms inserted.")
    def refresh_room_combo(self):
        """Updates the dropdown box with currently available rooms."""
        self.room_combo['values'] = []
        self.selected_room_var.set("")
        try:
            query="SELECT room_no, type, price FROM rooms WHERE status = 'Available'"
            rows=self.run_query(query).fetchall()
            room_list=[f"{r[0]} ({r[1]} - ${r[2]})" for r in rows]
            self.room_combo['values']=room_list
            if room_list:
                self.room_combo.current(0)
        except Exception as e:
             messagebox.showerror("DB Error", f"Could not fetch rooms: {e}")
    def clear_form(self):
        self.guest_name_var.set("")
        self.phone_var.set("")
        self.days_var.set(1)
        self.refresh_room_combo()
    def view_bookings(self):
        """Fetches current bookings and populates the Treeview."""
        records=self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        try:
            query = "SELECT booking_id, guest_name, phone, room_no, check_in_date, stay_days FROM bookings"
            rows = self.run_query(query).fetchall()
            for row in rows:
                self.tree.insert("", tk.END, values=row)
        except Exception as e:
             messagebox.showerror("DB Error", f"Could not fetch bookings: {e}")
    def book_room(self):
        name=self.guest_name_var.get()
        phone=self.phone_var.get()
        days=self.days_var.get()
        room_str = self.selected_room_var.get()
        if not name or not phone or not room_str:
            messagebox.showerror("Error", "Please fill all fields and select a room.")
            return
        room_no=int(room_str.split(" ")[0])
        today_date=date.today().strftime("%Y-%m-%d")
        try:
            query_booking="""INSERT INTO bookings 
                               (guest_name, phone, room_no, check_in_date, stay_days) 
                               VALUES (?, ?, ?, ?, ?)"""
            self.run_query(query_booking, (name, phone, room_no, today_date, days))
            query_room="UPDATE rooms SET status = 'Booked' WHERE room_no = ?"
            self.run_query(query_room, (room_no,))
            messagebox.showinfo("Success", f"Room {room_no} booked successfully for {name}!")
            self.clear_form()
            self.view_bookings() # Refresh the table view
            self.refresh_room_combo()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
    def checkout_guest(self):
        selected_item=self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a booking to check out.")
            return
        item_data=self.tree.item(selected_item[0])['values']
        booking_id=item_data[0]
        guest_name=item_data[1]
        room_no=item_data[3]
        days_stayed=item_data[5]
        if messagebox.askyesno("Confirm Checkout",f"Checkout {guest_name} from Room {room_no}?"):
            try:
                price_query = "SELECT price FROM rooms WHERE room_no=?"
                price = self.run_query(price_query, (room_no,)).fetchone()[0]
                total_bill=price * days_stayed
                self.run_query("DELETE FROM bookings WHERE booking_id=?", (booking_id,))
                self.run_query("UPDATE rooms SET status = 'Available' WHERE room_no=?",(room_no,))
                messagebox.showinfo("Checkout Complete", 
                                    f"Guest checked out.\nTotal Bill Amount: ${total_bill:.2f}")
                self.view_bookings()
                self.refresh_room_combo()
            except Exception as e:
                messagebox.showerror("Error", str(e))
if __name__=="__main__":
    root=tk.Tk()
    app=HotelManagementApp(root)
    root.mainloop()