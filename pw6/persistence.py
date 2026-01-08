import pickle
import gzip
import os

DATA_FILE = "students.dat"

def save_to_dat(manager):
    """Save all manager data to students.dat using pickle with compression"""
    data = {
        'students': manager.students,
        'courses': manager.courses,
        'marks': manager.mark.getMark()
    }
    with gzip.open(DATA_FILE, 'wb') as f:
        pickle.dump(data, f)

def load_from_dat(manager):
    """Load all manager data from students.dat using pickle with compression"""
    if not os.path.exists(DATA_FILE):
        return False
    with gzip.open(DATA_FILE, 'rb') as f:
        data = pickle.load(f)
    manager.students = data.get('students', [])
    manager.courses = data.get('courses', [])
    marks_data = data.get('marks', {})
    for cid, student_marks in marks_data.items():
        for sid, mark in student_marks.items():
            manager.mark.set_mark(cid, sid, mark)
    return True

def check_dat_exists():
    """Check if students.dat exists"""
    return os.path.exists(DATA_FILE)
