import curses
from persistence import write_students, write_courses, write_marks


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


def addStudents(stdscr, manager):
    stdscr.clear()
    stdscr.addstr(1, 2, "Add students (enter blank ID to stop)")
    while True:
        sid = prompt_input(stdscr, "Student ID: ")
        if sid.strip() == '':
            break
        sname = prompt_input(stdscr, "Student Name: ")
        sdob = prompt_input(stdscr, "Student DOB: ")
        ok = manager.addStudent(sid, sname, sdob)
        stdscr.addstr(f"  -> {'Added' if ok else 'Already exists'}\n")
    write_students(manager)
    stdscr.addstr("(Press any key to return to menu)")
    stdscr.getch()


def addCourses(stdscr, manager):
    stdscr.clear()
    stdscr.addstr(1, 2, "Add courses (enter blank ID to stop)")
    while True:
        cid = prompt_input(stdscr, "Course ID: ")
        if cid.strip() == '':
            break
        cname = prompt_input(stdscr, "Course name: ")
        credit = prompt_number(stdscr, "Course credit (integer): ", int)
        ok = manager.addCourse(cid, cname, credit)
        stdscr.addstr(f"  -> {'Added' if ok else 'Already exists'}\n")
    write_courses(manager)
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
    stdscr.addstr(f"Entering marks for course {cid} - {course.getCNAME()}\n")
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
            stdscr.addstr("  <-- invalid mark, try again\n")
    ok, msg = manager.inputMarks(cid, marks)
    write_marks(manager)
    stdscr.addstr(f"Result: {msg}\n(Press any key to continue)")
    stdscr.getch()
