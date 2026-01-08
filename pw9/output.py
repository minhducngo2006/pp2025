import tkinter as tk
from tkinter import ttk, messagebox


def displayStudents(parent, manager, title="Students"):
    dialog = tk.Toplevel(parent)
    dialog.title(title)
    dialog.geometry("600x400")
    dialog.transient(parent)
    dialog.grab_set()

    frame = ttk.Frame(dialog, padding="10")
    frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(frame, text=title, font=("Arial", 14, "bold")).pack(pady=5)

    if not manager.students:
        ttk.Label(frame, text="No students yet").pack(pady=20)
        ttk.Button(frame, text="Close", command=dialog.destroy).pack(pady=10)
        return

    columns = ("ID", "Name", "DOB", "GPA")
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=20)

    tree.heading("ID", text="Student ID")
    tree.heading("Name", text="Name")
    tree.heading("DOB", text="Date of Birth")
    tree.heading("GPA", text="GPA")

    tree.column("ID", width=100)
    tree.column("Name", width=200)
    tree.column("DOB", width=100)
    tree.column("GPA", width=80)

    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    for s in manager.students:
        tree.insert("", tk.END, values=(
            s.getID(),
            s.getName(),
            s.getDOB(),
            f"{s.getGPA():.2f}"
        ))

    ttk.Button(frame, text="Close", command=dialog.destroy).pack(pady=10)


def displayCourses(parent, manager):
    dialog = tk.Toplevel(parent)
    dialog.title("Courses")
    dialog.geometry("500x400")
    dialog.transient(parent)
    dialog.grab_set()

    frame = ttk.Frame(dialog, padding="10")
    frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(frame, text="Courses", font=("Arial", 14, "bold")).pack(pady=5)

    if not manager.courses:
        ttk.Label(frame, text="No courses yet").pack(pady=20)
        ttk.Button(frame, text="Close", command=dialog.destroy).pack(pady=10)
        return

    columns = ("ID", "Name", "Credits")
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=20)

    tree.heading("ID", text="Course ID")
    tree.heading("Name", text="Course Name")
    tree.heading("Credits", text="Credits")

    tree.column("ID", width=100)
    tree.column("Name", width=250)
    tree.column("Credits", width=80)

    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    for c in manager.courses:
        tree.insert("", tk.END, values=(
            c.getCID(),
            c.getCNAME(),
            c.getCredit()
        ))

    ttk.Button(frame, text="Close", command=dialog.destroy).pack(pady=10)


def displayMarks(parent, manager):
    dialog = tk.Toplevel(parent)
    dialog.title("Course Marks")
    dialog.geometry("500x400")
    dialog.transient(parent)
    dialog.grab_set()

    frame = ttk.Frame(dialog, padding="10")
    frame.pack(fill=tk.BOTH, expand=True)

    if not manager.courses:
        ttk.Label(frame, text="No courses available").pack(pady=20)
        ttk.Button(frame, text="Close", command=dialog.destroy).pack(pady=10)
        return

    course_frame = ttk.Frame(frame)
    course_frame.pack(fill=tk.X, pady=5)

    ttk.Label(course_frame, text="Select Course:").pack(side=tk.LEFT, padx=5)

    course_var = tk.StringVar()
    course_combo = ttk.Combobox(course_frame, textvariable=course_var, state="readonly")
    course_combo['values'] = [f"{c.getCID()} - {c.getCNAME()}" for c in manager.courses]
    course_combo.current(0)
    course_combo.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

    columns = ("Student", "ID", "Mark")
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=20)

    tree.heading("Student", text="Student Name")
    tree.heading("ID", text="Student ID")
    tree.heading("Mark", text="Mark (0-20)")

    tree.column("Student", width=200)
    tree.column("ID", width=100)
    tree.column("Mark", width=80)

    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def update_marks(event=None):
        for item in tree.get_children():
            tree.delete(item)

        cid = course_var.get().split(" - ")[0] if " - " in course_var.get() else course_var.get()
        cm = manager.mark.getMark()

        if cid not in cm:
            return

        for s in manager.students:
            if s.getID() in cm[cid]:
                tree.insert("", tk.END, values=(
                    s.getName(),
                    s.getID(),
                    f"{cm[cid][s.getID()]:.1f}"
                ))

    course_combo.bind("<<ComboboxSelected>>", update_marks)
    update_marks()

    ttk.Button(frame, text="Close", command=dialog.destroy).pack(pady=10)


def displayGPA(parent, manager, title="Students by GPA"):
    dialog = tk.Toplevel(parent)
    dialog.title(title)
    dialog.geometry("600x400")
    dialog.transient(parent)
    dialog.grab_set()

    frame = ttk.Frame(dialog, padding="10")
    frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(frame, text=title, font=("Arial", 14, "bold")).pack(pady=5)

    if not manager.students:
        ttk.Label(frame, text="No students yet").pack(pady=20)
        ttk.Button(frame, text="Close", command=dialog.destroy).pack(pady=10)
        return

    columns = ("ID", "Name", "DOB", "GPA")
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=20)

    tree.heading("ID", text="Student ID")
    tree.heading("Name", text="Name")
    tree.heading("DOB", text="Date of Birth")
    tree.heading("GPA", text="GPA")

    tree.column("ID", width=100)
    tree.column("Name", width=200)
    tree.column("DOB", width=100)
    tree.column("GPA", width=80)

    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    for s in manager.students:
        tree.insert("", tk.END, values=(
            s.getID(),
            s.getName(),
            s.getDOB(),
            f"{s.getGPA():.2f}"
        ))

    ttk.Button(frame, text="Close", command=dialog.destroy).pack(pady=10)
