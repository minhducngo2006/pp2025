import zipfile
import os

DATA_FILE = "students.dat"

def compress_to_dat():
    """Compress students.txt, courses.txt, marks.txt into students.dat"""
    with zipfile.ZipFile(DATA_FILE, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write("students.txt", arcname="students.txt")
        zf.write("courses.txt", arcname="courses.txt")
        zf.write("marks.txt", arcname="marks.txt")

def decompress_from_dat():
    """Decompress students.dat to extract text files"""
    if not os.path.exists(DATA_FILE):
        return False
    with zipfile.ZipFile(DATA_FILE, 'r', zipfile.ZIP_DEFLATED) as zf:
        zf.extractall(".")
    return True

def check_dat_exists():
    """Check if students.dat exists"""
    return os.path.exists(DATA_FILE)

def write_students(manager):
    """Write student info to students.txt"""
    with open("students.txt", "w", encoding="utf-8") as f:
        for s in manager.students:
            f.write(f"{s.getID()}|{s.getName()}|{s.getDOB()}\n")

def write_courses(manager):
    """Write course info to courses.txt"""
    with open("courses.txt", "w", encoding="utf-8") as f:
        for c in manager.courses:
            f.write(f"{c.getCID()}|{c.getCNAME()}|{c.getCredit()}\n")

def write_marks(manager):
    """Write marks to marks.txt"""
    marks = manager.mark.getMark()
    with open("marks.txt", "w", encoding="utf-8") as f:
        for cid, student_marks in marks.items():
            for sid, mark in student_marks.items():
                f.write(f"{cid}|{sid}|{mark}\n")

def load_students(manager):
    """Load student info from students.txt"""
    if not os.path.exists("students.txt"):
        return
    with open("students.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) >= 3:
                manager.addStudent(parts[0], parts[1], parts[2])

def load_courses(manager):
    """Load course info from courses.txt"""
    if not os.path.exists("courses.txt"):
        return
    with open("courses.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) >= 3:
                try:
                    credit = int(parts[2])
                    manager.addCourse(parts[0], parts[1], credit)
                except ValueError:
                    pass

def load_marks(manager):
    """Load marks from marks.txt"""
    if not os.path.exists("marks.txt"):
        return
    with open("marks.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) >= 3:
                try:
                    cid, sid = parts[0], parts[1]
                    mark = float(parts[2])
                    manager.inputMarks(cid, {sid: mark})
                except ValueError:
                    pass
