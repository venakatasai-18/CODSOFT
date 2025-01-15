import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
from tkcalendar import Calendar
import json
from datetime import datetime

# Task class to manage individual tasks
class Task:
    def __init__(self, title, description, date_time):
        self.title = title
        self.description = description
        self.date_time = date_time

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "date_time": self.date_time.strftime("%Y-%m-%d %H:%M")
        }

# Main Application class
class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")

        self.tasks = []
        

        # UI Components
        self.create_ui()
        self.load_tasks()

    def create_ui(self):
        # Task Input Panel
        input_frame = tk.Frame(self.root)
        input_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        tk.Label(input_frame, text="Task Title:").pack(anchor=tk.W)
        self.title_entry = tk.Entry(input_frame, width=30)
        self.title_entry.pack(anchor=tk.W, pady=5)

        tk.Label(input_frame, text="Task Description:").pack(anchor=tk.W)
        self.description_entry = tk.Entry(input_frame, width=30)
        self.description_entry.pack(anchor=tk.W, pady=5)

        tk.Label(input_frame, text="Task Date and Time:").pack(anchor=tk.W)
        self.calendar = Calendar(input_frame, selectmode='day', date_pattern='yyyy-mm-dd')
        self.calendar.pack(anchor=tk.W, pady=5)

        tk.Label(input_frame, text="Time (HH:MM):").pack(anchor=tk.W)
        self.time_entry = tk.Entry(input_frame, width=10)
        self.time_entry.pack(anchor=tk.W, pady=5)

        self.add_button = tk.Button(input_frame, text="Add Task", command=self.add_task)
        self.add_button.pack(anchor=tk.W, pady=10)

        # Task List
        self.tree = ttk.Treeview(self.root, columns=("Description", "Date"), show='headings')
        self.tree.heading("Description", text="Description")
        self.tree.heading("Date", text="Date")
        self.tree.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Buttons
        self.delete_button = tk.Button(self.root, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(side=tk.BOTTOM, padx=5, pady=5)

        self.track_button = tk.Button(self.root, text="Track Task", command=self.track_task)
        self.track_button.pack(side=tk.BOTTOM, padx=5, pady=5)

        self.edit_button = tk.Button(self.root, text="Edit Task", command=self.edit_task)
        self.edit_button.pack(side=tk.BOTTOM, padx=5, pady=5)

        self.mark_completed_button = tk.Button(self.root, text="Mark as Completed", command=self.mark_completed)
        self.mark_completed_button.pack(side=tk.BOTTOM, padx=5, pady=5)

    def add_task(self):
        title = self.title_entry.get().strip()
        description = self.description_entry.get().strip()
        date_str = self.calendar.get_date()
        time_str = self.time_entry.get().strip()

        if not title or not description or not time_str:
            messagebox.showwarning("Input Error", "All fields are required!")
            return

        try:
            date_time = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Input Error", "Invalid time format!")
            return

        task = Task(title, description, date_time)
        self.tasks.append(task)
        self.tree.insert("", "end", values=(description, date_time.strftime("%Y-%m-%d %H:%M")))
        self.save_tasks()
        self.clear_input_fields()
        messagebox.showinfo("Success", "Task added successfully!")

    def delete_task(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "No task selected!")
            return

        for item in selected_item:
            index = self.tree.index(item)
            del self.tasks[index]
            self.tree.delete(item)

        self.save_tasks()
        messagebox.showinfo("Success", "Task deleted successfully!")

    def track_task(self):
        now = datetime.now()
        upcoming_tasks = [task for task in self.tasks if task.date_time > now]

        if not upcoming_tasks:
            messagebox.showinfo("Track Task", "No upcoming tasks.")
            return

        message = "Upcoming Tasks:\n"
        for task in upcoming_tasks:
            message += f"{task.title}: {task.date_time.strftime('%Y-%m-%d %H:%M')}\n"

        messagebox.showinfo("Track Task", message)

    def edit_task(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "No task selected!")
            return

        index = self.tree.index(selected_item[0])
        task = self.tasks[index]

        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, task.title)
        self.description_entry.delete(0, tk.END)
        self.description_entry.insert(0, task.description)
        self.calendar.selection_set(task.date_time.strftime("%Y-%m-%d"))
        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, task.date_time.strftime("%H:%M"))

        self.delete_task()  # Remove the old task
        self.add_task()  # Add the updated task

    def mark_completed(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "No task selected!")
            return

        for item in selected_item:
            index = self.tree.index(item)
            task = self.tasks[index]
            task.description += " (Completed)"
            self.tree.item(item, values=(task.description, task.date_time.strftime("%Y-%m-%d %H:%M")))

        self.save_tasks()
        messagebox.showinfo("Success", "Task marked as completed!")

    def save_tasks(self):
        with open("tasks.json", "w") as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=4)

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                tasks_data = json.load(f)
                for task_data in tasks_data:
                    date_time = datetime.strptime(task_data["date_time"], "%Y-%m-%d %H:%M")
                    task = Task(task_data["title"], task_data["description"], date_time)
                    self.tasks.append(task)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

        for task in self.tasks:
            self.tree.insert("", "end", values=(task.description, task.date_time.strftime("%Y-%m-%d %H:%M")))

    def clear_input_fields(self):
        self.title_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)
        self.calendar.selection_clear()

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
