import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        self.root.geometry("500x400")

        self.tasks = []
        self.load_tasks()

        self.create_widgets()

    def load_tasks(self):
        try:
            with open('tasks.txt', 'r') as file:
                self.tasks = [line.strip().split(',') for line in file.readlines()]
        except FileNotFoundError:
            self.tasks = []

    def save_tasks(self):
        with open('tasks.txt', 'w') as file:
            for task in self.tasks:
                file.write(','.join(task) + '\n')

    def create_widgets(self):
        # Styling
        style = ttk.Style()
        style.configure("Treeview", font=('Helvetica', 12), rowheight=25)
        style.map("Treeview", background=[('selected', '#F5F5F5')])

        # Task Entry
        self.task_entry = tk.Entry(self.root, font=('Helvetica', 12), width=30)
        self.task_entry.grid(row=0, column=0, padx=10, pady=10)

        # Deadline Entry
        self.deadline_entry = tk.Entry(self.root, font=('Helvetica', 12), width=15)
        self.deadline_entry.grid(row=0, column=1, padx=10, pady=10)

        # Add Task Button
        add_button = tk.Button(self.root, text="Add Task", font=('Helvetica', 12), command=self.add_task)
        add_button.grid(row=0, column=2, padx=10, pady=10)

        # Task List
        self.task_list = ttk.Treeview(self.root, columns=('Task', 'Deadline', 'Status'), show='headings')
        self.task_list.heading('Task', text='Task')
        self.task_list.heading('Deadline', text='Deadline')
        self.task_list.heading('Status', text='Status')
        self.task_list.column('Task', width=200)
        self.task_list.column('Deadline', width=100)
        self.task_list.column('Status', width=100)
        self.task_list.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')

        # Load tasks into the list
        self.load_task_list()

        # Mark as Completed Button
        mark_button = tk.Button(self.root, text="Mark as Completed", font=('Helvetica', 12), command=self.mark_task)
        mark_button.grid(row=2, column=0, padx=10, pady=10)

        # Remove Task Button
        remove_button = tk.Button(self.root, text="Remove Task", font=('Helvetica', 12), command=self.remove_task)
        remove_button.grid(row=2, column=1, padx=10, pady=10)

        # Exit Button
        exit_button = tk.Button(self.root, text="Exit", font=('Helvetica', 12), command=self.root.destroy)
        exit_button.grid(row=2, column=2, padx=10, pady=10)

    def load_task_list(self):
        self.task_list.delete(*self.task_list.get_children())
        for i, task in enumerate(self.tasks, start=1):
            self.task_list.insert('', 'end', values=(task[0], task[1], task[2]))

    def add_task(self):
        title = self.task_entry.get()
        deadline = self.deadline_entry.get()

        if title and deadline:
            new_task = [title, deadline, 'Incomplete']
            self.tasks.append(new_task)
            self.save_tasks()
            self.load_task_list()
            self.task_entry.delete(0, 'end')
            self.deadline_entry.delete(0, 'end')
        else:
            messagebox.showwarning("Input Error", "Please enter both task title and deadline.")

    def mark_task(self):
        selected_item = self.task_list.selection()
        if selected_item:
            index = int(selected_item[0][1:]) - 1
            self.tasks[index][2] = 'Completed'
            self.save_tasks()
            self.load_task_list()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to mark as completed.")

    def remove_task(self):
        selected_item = self.task_list.selection()
        if selected_item:
            index = int(selected_item[0][1:]) - 1
            removed_task = self.tasks.pop(index)
            self.save_tasks()
            self.load_task_list()
            messagebox.showinfo("Task Removed", f"Task '{removed_task[0]}' removed successfully.")
        else:
            messagebox.showwarning("Selection Error", "Please select a task to remove.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()