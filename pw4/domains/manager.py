from math import floor
import numpy as np
from .student import Student
from .course import Course
from .mark import Mark


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

    def calGPA(self, student):
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
