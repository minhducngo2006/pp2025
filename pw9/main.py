import tkinter as tk
from tkinter import ttk, messagebox
from domains import Manager
from input import addStudentsDialog, addCoursesDialog, inputMarksDialog
from output import displayStudents, displayCourses, displayMarks, displayGPA
from persistence import check_dat_exists, save_to_dat, load_from_dat, stop_background_save


class StudentManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager")
        self.root.geometry("800x600")

        self.manager = Manager()

        self.create_menu()

        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.welcome_label = ttk.Label(
            self.main_frame,
            text="Student Manager",
            font=("Arial", 24, "bold")
        )
        self.welcome_label.pack(pady=50)

        self.info_label = ttk.Label(
            self.main_frame,
            text="Use the menu above to manage students, courses, and marks",
            font=("Arial", 12)
        )
        self.info_label.pack(pady=10)

        if check_dat_exists():
            load_from_dat(self.manager)
            self.info_label.config(text=f"Loaded data. Students: {len(self.manager.students)}, Courses: {len(self.manager.courses)}")

    def create_menu(self):
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Save Data", command=self.save_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_exit)
        menubar.add_cascade(label="File", menu=file_menu)

        students_menu = tk.Menu(menubar, tearoff=0)
        students_menu.add_command(label="Add Students", command=self.add_students)
        students_menu.add_command(label="Display Students", command=self.show_students)
        menubar.add_cascade(label="Students", menu=students_menu)

        courses_menu = tk.Menu(menubar, tearoff=0)
        courses_menu.add_command(label="Add Courses", command=self.add_courses)
        courses_menu.add_command(label="Display Courses", command=self.show_courses)
        menubar.add_cascade(label="Courses", menu=courses_menu)

        marks_menu = tk.Menu(menubar, tearoff=0)
        marks_menu.add_command(label="Input Marks", command=self.input_marks)
        marks_menu.add_command(label="Display Marks", command=self.show_marks)
        menubar.add_cascade(label="Marks", menu=marks_menu)

        gpa_menu = tk.Menu(menubar, tearoff=0)
        gpa_menu.add_command(label="Sort by GPA", command=self.sort_by_gpa)
        menubar.add_cascade(label="GPA", menu=gpa_menu)

        self.root.config(menu=menubar)

    def add_students(self):
        addStudentsDialog(self.root, self.manager, self.save_data)

    def add_courses(self):
        addCoursesDialog(self.root, self.manager, self.save_data)

    def input_marks(self):
        inputMarksDialog(self.root, self.manager, self.save_data)

    def show_students(self):
        displayStudents(self.root, self.manager)

    def show_courses(self):
        displayCourses(self.root, self.manager)

    def show_marks(self):
        displayMarks(self.root, self.manager)

    def sort_by_gpa(self):
        self.manager.sortGPA()
        displayGPA(self.root, self.manager, title="Students Sorted by GPA")

    def save_data(self):
        save_to_dat(self.manager)

    def on_exit(self):
        self.save_data()
        stop_background_save()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = StudentManagerApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
