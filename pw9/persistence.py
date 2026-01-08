import pickle
import gzip
import os
import threading
import queue

DATA_FILE = "students.dat"
_save_queue = queue.Queue()
_save_thread = None
_running = True


def _worker():
    """Background worker thread that processes save requests"""
    global _running
    while _running or not _save_queue.empty():
        try:
            # Wait for save request with timeout to allow checking _running
            data = _save_queue.get(timeout=0.5)
            with gzip.open(DATA_FILE, 'wb') as f:
                pickle.dump(data, f)
            _save_queue.task_done()
        except queue.Empty:
            continue


def _get_thread():
    """Get or create the background save thread"""
    global _save_thread
    if _save_thread is None or not _save_thread.is_alive():
        _running = True
        _save_thread = threading.Thread(target=_worker, daemon=True)
        _save_thread.start()
    return _save_thread


def save_to_dat(manager, background=True):
    """
    Save all manager data to students.dat using pickle with compression.
    If background=True (default), save in a separate thread and return immediately.
    If background=False, wait for save to complete.
    """
    data = {
        'students': manager.students,
        'courses': manager.courses,
        'marks': manager.mark.getMark()
    }

    if background:
        _get_thread()
        _save_queue.put(data)
    else:
        with gzip.open(DATA_FILE, 'wb') as f:
            pickle.dump(data, f)


def stop_background_save():
    """Stop the background save thread gracefully"""
    global _running
    _running = False
    if _save_thread and _save_thread.is_alive():
        _save_thread.join(timeout=2)


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
