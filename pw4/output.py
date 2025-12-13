import curses
from .input import prompt_input


def Box(stdscr, y, x, h, w, title=None):
    win = stdscr.derwin(h, w, y, x)
    win.box()
    if title:
        win.addstr(0, 2, f" {title} ")
    return win


def show_list(stdscr, lines, title=""):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    win = Box(stdscr, 1, 2, h-4, w-4, title)
    for idx, line in enumerate(lines[:h-6]):
        win.addstr(1+idx, 2, line)
    win.addstr(h-6, 2, "(Press any key to return)")
    stdscr.refresh()
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
