import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
import json
import os
from datetime import datetime


# File used to save the activities
DATA_FILE = "daily_activities.json"


class DailyPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("MPHA'S DAILY ACTIVITY PLANNER")
        self.root.geometry("800x500")

        self.activities = []
        self.load_activities()

        self.setup_style()
        self.create_interface()
        self.display_activities()

    # -----------------------------
    # SET UP THE APPEARANCE
    # -----------------------------
    def setup_style(self):
        style = ttk.Style()

        style.configure(
            "Treeview",
            rowheight=35,
            font=("Arial", 11)
        )

        style.configure(
            "Treeview.Heading",
            font=("Bradley Hand ITC", 12, "bold")
        )

    # -----------------------------
    # CREATE THE INTERFACE
    # -----------------------------
    def create_interface(self):

        # Title
        self.title_label = tk.Label(
            self.root,
            text="My Daily Activity Planner",
            font=("Arial", 22, "bold")
        )
        self.title_label.pack(pady=15)

        # Date
        self.date_label = tk.Label(
            self.root,
            text=datetime.now().strftime("%A, %d %B %Y"),
            font=("Arial", 12)
        )
        self.date_label.pack()

        # Input section
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=20)

        tk.Label(
            input_frame,
            text="Activity:"
        ).grid(row=0, column=0, padx=5)

        self.activity_entry = tk.Entry(
            input_frame,
            width=30
        )
        self.activity_entry.grid(row=0, column=1, padx=5)

        tk.Label(
            input_frame,
            text="Time:"
        ).grid(row=0, column=2, padx=5)

        self.time_entry = tk.Entry(
            input_frame,
            width=10
        )
        self.time_entry.grid(row=0, column=3, padx=5)

        add_button = tk.Button(
            input_frame,
            text="Add Activity",
            command=self.add_activity
        )
        add_button.grid(row=0, column=4, padx=10)

        # Table
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=20)

        columns = (
            "Activity",
            "Time",
            "Completed"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        self.table.heading(
            "Activity",
            text="Activity"
        )

        self.table.heading(
            "Time",
            text="Time"
        )

        self.table.heading(
            "Completed",
            text="Completed"
        )

        self.table.column(
            "Activity",
            width=450
        )

        self.table.column(
            "Time",
            width=150,
            anchor="center"
        )

        self.table.column(
            "Completed",
            width=300,
            anchor="center"
        )

        self.table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=self.table.yview
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.table.configure(
            yscrollcommand=scrollbar.set
        )

        # Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=15)

        complete_button = tk.Button(
            button_frame,
            text="Mark Complete",
            command=self.mark_complete
        )
        complete_button.grid(
            row=0,
            column=0,
            padx=5
        )

        delete_button = tk.Button(
            button_frame,
            text="Delete Activity",
            command=self.delete_activity
        )
        delete_button.grid(
            row=0,
            column=1,
            padx=5
        )

        customize_button = tk.Button(
            button_frame,
            text="Customize",
            command=self.customize
        )
        customize_button.grid(
            row=0,
            column=2,
            padx=5
        )

        # Progress
        self.progress_label = tk.Label(
            self.root,
            text="Completed: 0/0",
            font=("Arial", 12, "bold")
        )
        self.progress_label.pack(pady=5)

    # -----------------------------
    # ADD AN ACTIVITY
    # -----------------------------
    def add_activity(self):

        activity = self.activity_entry.get().strip()
        time = self.time_entry.get().strip()

        if activity == "":
            messagebox.showwarning(
                "Missing Activity",
                "Please enter an activity."
            )
            return

        if time == "":
            messagebox.showwarning(
                "Missing Time",
                "Please enter a time."
            )
            return

        new_activity = {
            "activity": activity,
            "time": time,
            "completed": False
        }

        self.activities.append(new_activity)

        self.save_activities()
        self.display_activities()

        self.activity_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)

    # -----------------------------
    # DISPLAY ACTIVITIES
    # -----------------------------
    def display_activities(self):

        # Remove old table entries
        for item in self.table.get_children():
            self.table.delete(item)

        # Add activities to table
        for activity in self.activities:

            completed = "Yes" if activity["completed"] else "No"

            self.table.insert(
                "",
                "end",
                values=(
                    activity["activity"],
                    activity["time"],
                    completed
                )
            )

        self.update_progress()

    # -----------------------------
    # MARK ACTIVITY AS COMPLETE
    # -----------------------------
    def mark_complete(self):

        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "No Activity Selected",
                "Please select an activity."
            )
            return

        item = selected[0]

        index = self.table.index(item)

        self.activities[index]["completed"] = True

        self.save_activities()
        self.display_activities()

    # -----------------------------
    # DELETE ACTIVITY
    # -----------------------------
    def delete_activity(self):

        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "No Activity Selected",
                "Please select an activity."
            )
            return

        item = selected[0]

        index = self.table.index(item)

        del self.activities[index]

        self.save_activities()
        self.display_activities()

    # -----------------------------
    # UPDATE PROGRESS
    # -----------------------------
    def update_progress(self):

        total = len(self.activities)

        completed = sum(
            1 for activity in self.activities
            if activity["completed"]
        )

        self.progress_label.config(
            text=f"Completed: {completed}/{total}"
        )

    # -----------------------------
    # CUSTOMIZATION
    # -----------------------------
    def customize(self):

        color = colorchooser.askcolor(
            title="Choose Background Color"
        )

        if color[1]:
            self.root.configure(
                bg=color[1]
            )

            self.title_label.configure(
                bg=color[1]
            )

            self.date_label.configure(
                bg=color[1]
            )

            self.progress_label.configure(
                bg=color[1]
            )

    # -----------------------------
    # SAVE ACTIVITIES
    # -----------------------------
    def save_activities(self):

        with open(
            DATA_FILE,
            "w"
        ) as file:

            json.dump(
                self.activities,
                file,
                indent=4
            )

    # -----------------------------
    # LOAD ACTIVITIES
    # -----------------------------
    def load_activities(self):

        if os.path.exists(DATA_FILE):

            try:
                with open(
                    DATA_FILE,
                    "r"
                ) as file:

                    self.activities = json.load(file)

            except:
                self.activities = []


# ---------------------------------
# START THE PROGRAM
# ---------------------------------

root = tk.Tk()

app = DailyPlanner(root)

root.mainloop()