import tkinter as tk
from tkinter import ttk, messagebox


def addStudentsDialog(parent, manager, on_save=None):
    dialog = tk.Toplevel(parent)
    dialog.title("Add Students")
    dialog.geometry("400x500")
    dialog.transient(parent)
    dialog.grab_set()

    input_frame = ttk.Frame(dialog, padding="10")
    input_frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(input_frame, text="Add Students (leave ID blank to finish)", font=("Arial", 12, "bold")).pack(pady=5)

    canvas = tk.Canvas(input_frame)
    scrollbar = ttk.Scrollbar(input_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    student_entries = []

    def add_student_row():
        frame = ttk.Frame(scrollable_frame, padding="5")
        frame.pack(fill=tk.X, pady=2)

        ttk.Label(frame, text="ID:").grid(row=0, column=0, padx=2)
        sid = ttk.Entry(frame, width=10)
        sid.grid(row=0, column=1, padx=2)

        ttk.Label(frame, text="Name:").grid(row=0, column=2, padx=2)
        sname = ttk.Entry(frame, width=15)
        sname.grid(row=0, column=3, padx=2)

        ttk.Label(frame, text="DOB:").grid(row=0, column=4, padx=2)
        sdob = ttk.Entry(frame, width=10)
        sdob.grid(row=0, column=5, padx=2)

        student_entries.append((sid, sname, sdob))

    for _ in range(5):
        add_student_row()

    def add_more():
        for _ in range(3):
            add_student_row()

    ttk.Button(input_frame, text="Add More Rows", command=add_more).pack(pady=5)

    button_frame = ttk.Frame(dialog, padding="10")
    button_frame.pack(fill=tk.X)

    def save_students():
        count = 0
        for sid, sname, sdob in student_entries:
            if sid.get().strip():
                ok = manager.addStudent(sid.get().strip(), sname.get().strip(), sdob.get().strip())
                if ok:
                    count += 1
        if on_save:
            on_save()
        messagebox.showinfo("Success", f"Added {count} student(s)", parent=dialog)
        dialog.destroy()

    ttk.Button(button_frame, text="Save", command=save_students).pack(side=tk.RIGHT, padx=5)
    ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)


def addCoursesDialog(parent, manager, on_save=None):
    dialog = tk.Toplevel(parent)
    dialog.title("Add Courses")
    dialog.geometry("400x400")
    dialog.transient(parent)
    dialog.grab_set()

    input_frame = ttk.Frame(dialog, padding="10")
    input_frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(input_frame, text="Add Courses (leave ID blank to finish)", font=("Arial", 12, "bold")).pack(pady=5)

    canvas = tk.Canvas(input_frame)
    scrollbar = ttk.Scrollbar(input_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    course_entries = []

    def add_course_row():
        frame = ttk.Frame(scrollable_frame, padding="5")
        frame.pack(fill=tk.X, pady=2)

        ttk.Label(frame, text="ID:").grid(row=0, column=0, padx=2)
        cid = ttk.Entry(frame, width=10)
        cid.grid(row=0, column=1, padx=2)

        ttk.Label(frame, text="Name:").grid(row=0, column=2, padx=2)
        cname = ttk.Entry(frame, width=20)
        cname.grid(row=0, column=3, padx=2)

        ttk.Label(frame, text="Credit:").grid(row=0, column=4, padx=2)
        credit = ttk.Entry(frame, width=5)
        credit.grid(row=0, column=5, padx=2)

        course_entries.append((cid, cname, credit))

    for _ in range(4):
        add_course_row()

    def add_more():
        for _ in range(2):
            add_course_row()

    ttk.Button(input_frame, text="Add More Rows", command=add_more).pack(pady=5)

    button_frame = ttk.Frame(dialog, padding="10")
    button_frame.pack(fill=tk.X)

    def save_courses():
        count = 0
        for cid, cname, credit in course_entries:
            if cid.get().strip():
                try:
                    ok = manager.addCourse(cid.get().strip(), cname.get().strip(), int(credit.get()))
                    if ok:
                        count += 1
                except ValueError:
                    pass
        if on_save:
            on_save()
        messagebox.showinfo("Success", f"Added {count} course(s)", parent=dialog)
        dialog.destroy()

    ttk.Button(button_frame, text="Save", command=save_courses).pack(side=tk.RIGHT, padx=5)
    ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)


def inputMarksDialog(parent, manager, on_save=None):
    dialog = tk.Toplevel(parent)
    dialog.title("Input Marks")
    dialog.geometry("500x500")
    dialog.transient(parent)
    dialog.grab_set()

    input_frame = ttk.Frame(dialog, padding="10")
    input_frame.pack(fill=tk.BOTH, expand=True)

    course_frame = ttk.LabelFrame(input_frame, text="Select Course", padding="10")
    course_frame.pack(fill=tk.X, pady=5)

    if not manager.courses:
        ttk.Label(course_frame, text="No courses available. Please add courses first.").pack()
        ttk.Button(course_frame, text="Close", command=dialog.destroy).pack(pady=5)
        return

    course_var = tk.StringVar()
    course_combo = ttk.Combobox(course_frame, textvariable=course_var, state="readonly")
    course_combo['values'] = [f"{c.getCID()} - {c.getCNAME()}" for c in manager.courses]
    course_combo.current(0)
    course_combo.pack(fill=tk.X, pady=5)

    marks_frame = ttk.LabelFrame(input_frame, text="Enter Marks (0-20)", padding="10")
    marks_frame.pack(fill=tk.BOTH, expand=True, pady=5)

    marks_entries = {}

    def update_student_list(event=None):
        for widget in marks_frame.winfo_children():
            widget.destroy()

        cid = course_var.get().split(" - ")[0] if " - " in course_var.get() else course_var.get()
        course = manager.findCourse(cid)

        if not course:
            return

        ttk.Label(marks_frame, text=f"Entering marks for: {cid} - {course.getCNAME()}").pack(anchor=tk.W)

        canvas = tk.Canvas(marks_frame)
        scrollbar = ttk.Scrollbar(marks_frame, orient="vertical", command=canvas.yview)
        marks_scrollable = ttk.Frame(canvas)

        marks_scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=marks_scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill=tk.BOTH, expand=True)
        scrollbar.pack(side="right", fill=tk.Y)

        marks_entries.clear()
        for i, s in enumerate(manager.students):
            row = ttk.Frame(marks_scrollable, padding="2")
            row.pack(fill=tk.X)

            ttk.Label(row, text=f"{s.getName()} (ID: {s.getID()})", width=30).pack(side=tk.LEFT)
            entry = ttk.Entry(row, width=10)
            entry.pack(side=tk.LEFT, padx=5)
            marks_entries[s.getID()] = entry
            ttk.Label(row, text="/ 20").pack(side=tk.LEFT)

    course_combo.bind("<<ComboboxSelected>>", update_student_list)
    update_student_list()

    button_frame = ttk.Frame(dialog, padding="10")
    button_frame.pack(fill=tk.X)

    def save_marks():
        cid = course_var.get().split(" - ")[0] if " - " in course_var.get() else course_var.get()
        marks = {}
        for sid, entry in marks_entries.items():
            try:
                m = float(entry.get())
                if 0 <= m <= 20:
                    marks[sid] = m
            except ValueError:
                pass

        if marks:
            ok, msg = manager.inputMarks(cid, marks)
            if ok and on_save:
                on_save()
            messagebox.showinfo("Result", msg, parent=dialog)
        dialog.destroy()

    ttk.Button(button_frame, text="Save", command=save_marks).pack(side=tk.RIGHT, padx=5)
    ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
