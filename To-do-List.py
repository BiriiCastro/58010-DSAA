from tkinter import *
from tkinter.ttk import Treeview
import messagebox
from datetime import datetime
from PIL import Image, ImageTk


class Task:
    def __init__(self, task_description, priority):
        self.task_description = task_description
        self.priority = priority
        self.next_task = None
        self.prev_task = None
        self.date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class ChomusukeTaskTracker:
    def __init__(self, root):
        # Window Title and Icon
        self.root = root
        self.root.geometry("810x410+350+150")
        self.root.resizable(width=False, height=False)
        self.root.title("Chomusuke Task Tracker")

        image = Image.open('Chomusuke.png')
        icon = ImageTk.PhotoImage(image)
        self.root.iconphoto(True, icon)

        # Main Background
        background_image = Image.open('chom.jpg')
        background_image = ImageTk.PhotoImage(background_image)
        self.background_label = Label(self.root, image=background_image)
        self.background_label.image = background_image
        self.background_label.place(relwidth=1, relheight=1)

        self.tasks = []

        self.task_tracker = LinkedList()

        self.mainWindow = Frame(root)
        self.mainWindow.grid(row=0, column=0, padx=20, pady=20)
        self.mainWindow.configure(background="white")

        background_image = Image.open('chom.jpg')
        background_image = ImageTk.PhotoImage(background_image)
        self.background_label = Label(self.mainWindow, image=background_image)
        self.background_label.image = background_image
        self.background_label.place(relwidth=1, relheight=1)

        self.search_entry = Entry(self.mainWindow, font=("Arial", 12))
        self.search_entry.bind("<KeyRelease>", lambda event: self.search_task())
        self.search_entry.grid(row=0, column=0, pady=15)

        self.add_button = Button(self.mainWindow, text="Add Task", border=1, font=("Arial", 12, "bold"),
                                 bg="#000000", fg="#DAA520", activebackground="#808080", activeforeground="#DAA520",
                                 command=self.add_task_window)
        self.add_button.grid(row=0, column=1, pady=15)

        self.edit_button = Button(self.mainWindow, text="Edit Task", border=1, font=("Arial", 12, "bold"),
                                  bg="#000000", fg="#DAA520", activebackground="#808080", activeforeground="#DAA520",
                                  command=self.edit_task_window)
        self.edit_button.grid(row=0, column=2, pady=15)

        self.delete_button = Button(self.mainWindow, text="Delete Task", border=1, font=("Arial", 12, "bold"),
                                    bg="#000000", fg="#DAA520", activebackground="#808080", activeforeground="#DAA520",
                                    command=self.remove_selected_task)
        self.delete_button.grid(row=0, column=3, pady=15)

        self.clear_button = Button(self.mainWindow, text="Clear All", border=1, font=("Arial", 12, "bold"),
                                   bg="#000000", fg="#FF3030", activebackground="#808080", activeforeground="#FF3030",
                                   command=self.remove_all_tasks)
        self.clear_button.grid(row=0, column=4, pady=15)

        # Creating a Treeview
        self.tree = Treeview(self.mainWindow, columns=("Priority", "Task Description", "Date"), show="headings",
                             height=14)
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Task Description", text="Task Descriptions")
        self.tree.heading("Date", text="Date")
        self.tree.column("Priority", width=50)
        self.tree.column("Task Description", width=500)
        self.tree.column("Date", width=200)

        # Creating a scrollbar
        scrollbar = Scrollbar(self.mainWindow, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=2, column=6, sticky="ns")

        self.tree.grid(row=2, column=0, columnspan=5, sticky="nsew")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.update_treeview()

    def add_task_window(self):
        addFrame = Toplevel(self.mainWindow)
        addFrame.geometry("380x320+580+210")
        addFrame.resizable(width=False, height=False)
        addFrame.title("Add Task")
        addFrame.grab_set()

        background_image = Image.open('chocho.jpg')
        background_image = ImageTk.PhotoImage(background_image)
        self.background_label = Label(addFrame, image=background_image)
        self.background_label.image = background_image
        self.background_label.place(relwidth=1, relheight=1)

        self.priority_label = Label(addFrame, text="Priority:", font=("Arial", 14, "bold"), bg="#000000", fg="#FFFFFF")
        self.priority_label.place(x=50, y=50)

        self.priority_entry = Spinbox(addFrame, from_=1, to=5, state="readonly", font=("Arial", 14, "bold"), width=3)
        self.priority_entry.place(x=150, y=50)

        self.task_label = Label(addFrame, text="Task:", font=("Arial", 14, "bold"), bg="#000000", fg="#FFFFFF")
        self.task_label.place(x=50, y=135)

        self.task_entry = Entry(addFrame, width=17, font=("Arial", 14, "bold"))
        self.task_entry.place(x=150, y=135)

        confirm_button = Button(addFrame, text="Confirm", font=("Arial", 12, "bold"),
                                bg="#000000", fg="#DAA520", activebackground="#808080", activeforeground="#DAA520",
                                command=lambda: self.add_task(addFrame))
        confirm_button.place(x=150, y=240)

    def add_task(self, addFrame):
        task_description = self.task_entry.get()
        priority = int(self.priority_entry.get())

        if task_description:
            self.task_tracker.llist_add_task(task_description, priority)
            self.update_treeview()
            self.task_entry.delete(0, END)
            addFrame.destroy()
        else:
            messagebox.showwarning("Input Error", "Please enter a task description.")

    def edit_task_window(self):
        selected_task_index = self.tree.selection()

        if not selected_task_index:
            return messagebox.showwarning("No Task Selected", "Please select a task to EDIT.")

        selected_task_item = self.tree.item(selected_task_index)
        selected_task_description = selected_task_item['values'][1]

        selected_task = None
        for task in self.task_tracker.get_tasks():
            if task.task_description == selected_task_description:
                selected_task = task
                break

        if not selected_task:
            messagebox.showerror("Error", "Task not found for editing.")

        editFrame = Toplevel(self.mainWindow)
        editFrame.geometry("380x320+580+210")
        editFrame.resizable(width=False, height=False)
        editFrame.title("Edit Task")
        editFrame.grab_set()

        background_image = Image.open('chocho.jpg')
        background_image = ImageTk.PhotoImage(background_image)
        self.background_label = Label(editFrame, image=background_image)
        self.background_label.image = background_image
        self.background_label.place(relwidth=1, relheight=1)

        edit_priority_var = IntVar()
        edit_priority_var.set(selected_task.priority)

        self.priority_label = Label(editFrame, text="Priority:", font=("Arial", 14, "bold"), bg="#000000", fg="#FFFFFF")
        self.priority_label.place(x=50, y=50)

        self.edit_priority_entry = Spinbox(editFrame, from_=1, to=5, state="readonly", font=("Arial", 14, "bold"),
                                           width=3, textvariable=edit_priority_var)
        self.edit_priority_entry.place(x=150, y=50)

        self.task_label = Label(editFrame, text="Task:", font=("Arial", 14, "bold"), bg="#000000", fg="#FFFFFF")
        self.task_label.place(x=50, y=135)

        self.edit_task_entry = Entry(editFrame, width=17, font=("Arial", 14, "bold"))
        self.edit_task_entry.place(x=150, y=135)
        self.edit_task_entry.insert(END, selected_task.task_description)

        confirm_button = Button(editFrame, text="Confirm", font=("Arial", 12, "bold"),
                                bg="#000000", fg="#DAA520", activebackground="#808080", activeforeground="#DAA520",
                                command=lambda: self.edit_task(selected_task, editFrame))
        confirm_button.place(x=150, y=240)

    def edit_task(self, task_to_edit, editFrame):
        new_task_description = self.edit_task_entry.get()
        new_priority = int(self.edit_priority_entry.get())

        if not new_task_description:
            messagebox.showwarning("Input Error", "Please enter a new task description.")

        self.task_tracker.llist_edit_task(task_to_edit, new_task_description, new_priority)
        self.update_treeview()
        self.edit_task_entry.delete(0, END)
        editFrame.destroy()

    def remove_selected_task(self):
        selected_task_index = self.tree.selection()

        if not selected_task_index:
            return messagebox.showwarning("No Task Selected", "Please select a task to DELETE.")

        selected_task_item = self.tree.item(selected_task_index)
        selected_task_description = selected_task_item['values'][1]

        confirmed = messagebox.askyesno("Delete Task", "Are you sure you want to DELETE SELECTED task?")
        if confirmed:
            self.task_tracker.llist_remove_task(selected_task_description)
            self.update_treeview()

    def remove_all_tasks(self):
        if not self.task_tracker.get_tasks():
            return messagebox.showwarning("No Tasks", "There are no tasks to DELETE.")

        confirmed = messagebox.askyesno("Delete All Task", "Are you sure you want to DELETE ALL tasks?")
        if confirmed:
            self.task_tracker.llist_remove_all_tasks()
            self.update_treeview()

    def search_task(self):
        query = self.search_entry.get().lower()
        tasks = self.task_tracker.get_tasks()

        if not query:
            self.update_treeview()

        # Linear Search
        matching_tasks = [task for task in tasks if query in task.task_description.lower()]

        self.tree.delete(*self.tree.get_children())
        matching_tasks.sort(key=lambda task: task.date, reverse=True)
        for task in matching_tasks:
            self.tree.insert("", "end", values=(task.priority, task.task_description, task.date))

    def update_treeview(self):
        self.tree.delete(*self.tree.get_children())

        tasks = self.task_tracker.get_tasks()
        tasks.sort(key=lambda task: (int(task.priority), task.date), reverse=True)
        for task in tasks:
            self.tree.insert("", "end", values=(task.priority, task.task_description, task.date))


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def llist_add_task(self, task_description, priority):
        new_task = Task(task_description, int(priority))
        if not self.head:
            self.head = new_task
            self.tail = new_task
        else:
            new_task.prev_task = self.tail
            self.tail.next_task = new_task
            self.tail = new_task

    def llist_edit_task(self, old_task, new_task_description, new_priority):
        current_task = self.head
        while current_task:
            if current_task == old_task:
                current_task.task_description = new_task_description
                current_task.date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                break
            current_task = current_task.next_task
        current_task.priority = new_priority

    def llist_remove_task(self, task_description):
        current_task = self.head
        while current_task:
            if current_task.task_description == task_description:
                if current_task.prev_task:
                    current_task.prev_task.next_task = current_task.next_task
                else:
                    self.head = current_task.next_task

                if current_task.next_task:
                    current_task.next_task.prev_task = current_task.prev_task
                else:
                    self.tail = current_task.prev_task

                break
            current_task = current_task.next_task

    def llist_remove_all_tasks(self):
        self.head = None
        self.tail = None

    def get_tasks(self):
        tasks = []
        current_task = self.head
        while current_task:
            tasks.append(current_task)
            current_task = current_task.next_task
        return tasks


if __name__ == "__main__":
    win = Tk()
    mainWindow = ChomusukeTaskTracker(win)
    win.mainloop()
