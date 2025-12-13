import curses
from curses import textpad
from math import floor
import numpy as np

class Student:
    def __init__(self,Sid,Sname,Sdob):
        self.__id = Sid 
        self.__name = Sname
        self.__dob = Sdob
        self.__gpa = 0.0
    def getName(self):
        return self.__name
    def getID(self):
        return self.__id
    def getDOB(self):
        return self.__dob  
    def setGPA(self,gpa):
        self.__gpa = gpa
    def getGPA(self):
        return self.__gpa
    def print(self):
        return [f"Student ID: {self.getID()}",
                f"Student Name: {self.getName()}",
                f"Student DOB: {self.getDOB()}",
                f"Student GPA: {self.getGPA():.2f}"]

class Course:
    def __init__(self,Cid,Cname,credits):
        self.__course_id = Cid
        self.__course_name = Cname
        self.__credits = credits
    def getCID(self):
        return self.__course_id
    def getCNAME(self):
        return self.__course_name
    def getCredit(self):
        return self.__credits
    def print(self):
        return [f"Course ID: {self.getCID()}",
                f"Course Name: {self.getCNAME()}",
                f"Course Credit: {self.getCredit()}"]

class Mark:
    def __init__(self):
        self.__marks = {}
    def set_mark(self, course_id, student_id, mark):
        if course_id not in self.__marks:
            self.__marks[course_id] = {}
        self.__marks[course_id][student_id] = mark
    def get_course_marks(self, course_id):
        return self.__marks.get(course_id, {})
    def getMark(self):
        return self.__marks

class Manager:
    def __init__(self):
        self.students = []
        self.courses = []
        self.mark = Mark()
    def findStudent(self, sid):
        for s in self.students:
            if s.getID() == sid:
                return s
        return None
    def findCourse(self, cid):
        for c in self.courses:
            if c.getCID() == cid:
                return c
        return None
    def addStudent(self, sid, sname, sdob):
        if self.findStudent(sid):
            return False
        self.students.append(Student(sid, sname, sdob))
        return True
    def addCourse(self, cid, cname, credit):
        if self.findCourse(cid):
            return False
        self.courses.append(Course(cid, cname, credit))
        return True
    def inputMarks(self, cid, marks):
        course = self.findCourse(cid)
        if not course:
            return False, "Course not found"
        for sid, m in marks.items():
            student = self.findStudent(sid)
            if not student:
                return False, f"Student {sid} not found"
            if not (0 <= m <= 20):
                return False, f"Invalid mark {m} for {sid}"
            shifted = floor(m * 10)
            final = shifted / 10.0
            self.mark.set_mark(cid, sid, final)
        return True, "OK"

    def calGPA(self,student):
        mark = self.mark.getMark()
        credits = []
        marks = []
        for course in self.courses:
            cid = course.getCID()
            if cid in mark and student.getID() in mark[cid]:
                credits.append(course.getCredit())
                marks.append(mark[cid][student.getID()])
        if len(marks) == 0:
            student.setGPA(0)
            return 0
        credit_arr = np.array(credits)
        mark_arr = np.array(marks)
        gpa = np.sum(credit_arr * mark_arr) / np.sum(credit_arr)
        student.setGPA(gpa)
        return gpa

    def sortGPA(self):
        for s in self.students:
            self.calGPA(s)
        self.students.sort(key=lambda x: x.getGPA(), reverse=True)

def Box(stdscr, y, x, h, w, title=None):
    win = stdscr.derwin(h, w, y, x)
    win.box()
    if title:
        win.addstr(0, 2, f" {title} ")
    return win


def prompt_input(stdscr, prompt):
    curses.echo()
    stdscr.addstr(prompt)
    stdscr.refresh()
    s = stdscr.getstr().decode('utf-8')
    curses.noecho()
    return s


def prompt_number(stdscr, prompt, cast=int):
    while True:
        s = prompt_input(stdscr, prompt)
        try:
            return cast(s)
        except Exception:
            stdscr.addstr("  <-- invalid, try again\n")


def show_list(stdscr, lines, title=""):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    win = Box(stdscr, 1, 2, h-4, w-4, title)
    for idx, line in enumerate(lines[:h-6]):
        win.addstr(1+idx, 2, line)
    win.addstr(h-6, 2, "(Press any key to return)")
    stdscr.refresh()
    stdscr.getch()


def menu(stdscr, manager):
    curses.curs_set(0)
    current = 0
    options = [
        "Add students",
        "Add courses",
        "Input marks for a course",
        "Display students",
        "Display courses",
        "Display marks for a course",
        "Sort students by GPA (desc) and show",
        "Exit",
    ]
    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        stdscr.addstr(1, 2, "Student Manager (curses UI)")
        for i, opt in enumerate(options):
            marker = '>' if i == current else ' '
            stdscr.addstr(3 + i, 4, f"{marker} {opt}")
        stdscr.addstr(h-2, 2, "Use Up/Down to move, Enter to select")
        key = stdscr.getch()
        if key in [curses.KEY_UP, ord('k')]:
            current = (current - 1) % len(options)
        elif key in [curses.KEY_DOWN, ord('j')]:
            current = (current + 1) % len(options)
        elif key in [curses.KEY_ENTER, 10, 13]:
            if current == 0:
                addStudents(stdscr, manager)
            elif current == 1:
                addCourses(stdscr, manager)
            elif current == 2:
                inputMarks(stdscr, manager)
            elif current == 3:
                displayStudents(stdscr, manager)
            elif current == 4:
                displayCourses(stdscr, manager)
            elif current == 5:
                displayMarks(stdscr, manager)
            elif current == 6:
                manager.sortGPA()
                displayGPA(stdscr, manager, title="Students sorted by GPA")
            elif current == 7:
                break
        elif key in [ord('q'), 27]:
            break


def addStudents(stdscr, manager):
    stdscr.clear()
    stdscr.addstr(1,2, "Add students (enter blank ID to stop)")
    row = 3
    while True:
        sid = prompt_input(stdscr, f"Student ID: ")
        if sid.strip() == '':
            break
        sname = prompt_input(stdscr, f"Student Name: ")
        sdob = prompt_input(stdscr, f"Student DOB: ")
        ok = manager.addStudent(sid, sname, sdob)
        stdscr.addstr(f"  -> {'Added' if ok else 'Already exists'}\n")
    stdscr.addstr("(Press any key to return to menu)")
    stdscr.getch()


def addCourses(stdscr, manager):
    stdscr.clear()
    stdscr.addstr(1,2, "Add courses (enter blank ID to stop)")
    while True:
        cid = prompt_input(stdscr, f"Course ID: ")
        if cid.strip() == '':
            break
        cname = prompt_input(stdscr, f"Course name: ")
        credit = prompt_number(stdscr, f"Course credit (integer): ", int)
        ok = manager.addCourse(cid, cname, credit)
        stdscr.addstr(f"  -> {'Added' if ok else 'Already exists'}")
    stdscr.addstr("(Press any key to return to menu)")
    stdscr.getch()


def inputMarks(stdscr, manager):
    stdscr.clear()
    cid = prompt_input(stdscr, "Enter course ID to set marks: ")
    course = manager.findCourse(cid)
    if not course:
        stdscr.addstr("Course not found. Press any key to return.")
        stdscr.getch()
        return
    marks = {}
    stdscr.addstr(f"Entering marks for course {cid} - {course.getCNAME()}")
    for s in manager.students:
        while True:
            val = prompt_input(stdscr, f"Mark for {s.getName()} (0-20): ")
            try:
                m = float(val)
                if 0 <= m <= 20:
                    marks[s.getID()] = m
                    break
            except:
                pass
            stdscr.addstr("  <-- invalid mark, try again")
    ok, msg = manager.inputMarks(cid, marks)
    stdscr.addstr(f"Result: {msg}\n(Press any key to continue)")
    stdscr.getch()


def displayStudents(stdscr, manager, title="Students"):
    lines = []
    for s in manager.students:
        lines.extend(s.print())
        lines.append('-'*30)
    if not lines:
        lines = ["No students yet"]
    show_list(stdscr, lines, title)


def displayGPA(stdscr, manager, title="Students"):
    lines = []
    for s in manager.students:
        lines.extend(s.print())
        lines.append('-'*30)
    if not lines:
        lines = ["No students yet"]
    show_list(stdscr, lines, title)


def displayCourses(stdscr, manager):
    lines = []
    for c in manager.courses:
        lines.extend(c.print())
        lines.append('-'*30)
    if not lines:
        lines = ["No courses yet"]
    show_list(stdscr, lines, title="Courses")


def displayMarks(stdscr, manager):
    cid = prompt_input(stdscr, "Enter course ID to view marks: ")
    cm = manager.mark.getMark()
    if cid not in cm:
        stdscr.addstr("Course has no marks or not found. Press any key to return.")
        stdscr.getch()
        return
    course = manager.findCourse(cid)
    lines = [f"Marks for course {cid} - {course.getCNAME() if course else ''}"]
    lines.append('')
    for s in manager.students:
        if s.getID() in cm[cid]:
            lines.append(f"{s.getName()} (ID:{s.getID()}): {cm[cid][s.getID()]:.1f}")
        else:
            lines.append(f"{s.getName()} (ID:{s.getID()}): Empty")
    show_list(stdscr, lines, title=f"Marks: {cid}")


def Curses(stdscr):
    manager = Manager()
    menu(stdscr, manager)

if __name__ == '__main__':
    curses.wrapper(Curses)
