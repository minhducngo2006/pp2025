import curses
from domains import Manager
from input import addStudents, addCourses, inputMarks
from output import displayStudents, displayCourses, displayMarks, displayGPA


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


def main(stdscr):
    manager = Manager()
    menu(stdscr, manager)


if __name__ == '__main__':
    curses.wrapper(main)
