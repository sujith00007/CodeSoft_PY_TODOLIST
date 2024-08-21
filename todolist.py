from tkinter import *
from tkinter import messagebox
import sqlite3 as sql

def add_task():
    task_string = task_field.get().strip()
    if not task_string:
        messagebox.showwarning('Input Error', 'Task field cannot be empty.')
        return
    if task_string in tasks:
        messagebox.showwarning('Duplicate Task', 'Task already exists in the list.')
        return
    tasks.append(task_string)
    the_cursor.execute('INSERT INTO tasks (title) VALUES (?)', (task_string,))
    list_update()
    task_field.delete(0, 'end')

def edit_task():
    try:
        selected_index = task_listbox.curselection()[0]
        old_task = task_listbox.get(selected_index)
        new_task = task_field.get().strip()
        if not new_task:
            messagebox.showwarning('Input Error', 'Task field cannot be empty.')
            return
        if new_task == old_task:
            messagebox.showinfo('No Change', 'The task is the same as before.')
            return
        if new_task in tasks:
            messagebox.showwarning('Duplicate Task', 'Task already exists in the list.')
            return
        tasks[selected_index] = new_task
        the_cursor.execute('UPDATE tasks SET title = ? WHERE title = ?', (new_task, old_task))
        list_update()
        task_field.delete(0, 'end')
    except IndexError:
        messagebox.showwarning('Selection Error', 'No task selected to edit.')

def delete_task():
    try:
        selected_index = task_listbox.curselection()[0]
        task_to_remove = task_listbox.get(selected_index)
        tasks.remove(task_to_remove)
        the_cursor.execute('DELETE FROM tasks WHERE title = ?', (task_to_remove,))
        list_update()
    except IndexError:
        messagebox.showwarning('Selection Error', 'No task selected to delete.')

def delete_all_tasks():
    if messagebox.askyesno('Confirm Deletion', 'Are you sure you want to delete all tasks?'):
        tasks.clear()
        the_cursor.execute('DELETE FROM tasks')
        list_update()

def clear_list():
    task_listbox.delete(0, 'end')

def list_update():
    clear_list()
    for task in tasks:
        task_listbox.insert('end', task)

def retrieve_database():
    tasks.clear()
    for row in the_cursor.execute('SELECT title FROM tasks'):
        tasks.append(row[0])

def close():
    the_connection.commit()
    the_cursor.close()
    the_connection.close()
    guiWindow.destroy()

if __name__ == "__main__":
    guiWindow = Tk()
    guiWindow.title("To-Do List")
    guiWindow.geometry("700x450")
    guiWindow.resizable(0, 0)
    guiWindow.configure(bg="#f5f5f5")

    the_connection = sql.connect('listOfTasks.db')
    the_cursor = the_connection.cursor()
    the_cursor.execute('CREATE TABLE IF NOT EXISTS tasks (title TEXT)')

    tasks = []

    functions_frame = Frame(guiWindow, bg="#f5f5f5")
    functions_frame.pack(side="top", expand=True, fill="both")

    task_label = Label(functions_frame, text="TO-DO LIST\nEnter Task Title:",
        font=("Arial", 14, "bold"),
        bg="#f5f5f5",
        fg="#333")
    task_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')

    task_field = Entry(functions_frame,
        font=("Arial", 14),
        width=40,
        bg="#fff",
        fg="#000")
    task_field.grid(row=0, column=1, padx=10, pady=10, columnspan=2)

    add_button = Button(functions_frame,
        text="Add Task",
        width=15,
        bg="#4CAF50",  # Green color for add button
        fg="#fff",
        font=("Arial", 12, "bold"),
        command=add_task)
    add_button.grid(row=1, column=0, padx=10, pady=10)

    edit_button = Button(functions_frame,
        text="Edit Task",
        width=15,
        bg="#FFC107",  # Amber color for edit button
        fg="#fff",
        font=("Arial", 12, "bold"),
        command=edit_task)
    edit_button.grid(row=1, column=1, padx=10, pady=10)

    del_button = Button(functions_frame,
        text="Remove Task",
        width=15,
        bg="#F44336",  # Red color for remove button
        fg="#fff",
        font=("Arial", 12, "bold"),
        command=delete_task)
    del_button.grid(row=1, column=2, padx=10, pady=10)

    del_all_button = Button(functions_frame,
        text="Clear All",
        width=15,
        bg="#FF5722",  # Deep Orange color for clear all button
        fg="#fff",
        font=("Arial", 12, "bold"),
        command=delete_all_tasks)
    del_all_button.grid(row=2, column=0, padx=10, pady=10)

    exit_button = Button(functions_frame,
        text="Exit",
        width=35,
        bg="#607D8B",  # Blue Grey color for exit button
        fg="#fff",
        font=("Arial", 12, "bold"),
        command=close)
    exit_button.grid(row=2, column=1, columnspan=2, padx=10, pady=10)

    task_listbox = Listbox(functions_frame,
        width=80,
        height=15,
        font=("Arial", 12),
        bg="#fff",
        fg="#000",
        selectmode='SINGLE',
        selectbackground="#FFC107",
        selectforeground="#000")
    task_listbox.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    retrieve_database()
    list_update()
    guiWindow.mainloop()
