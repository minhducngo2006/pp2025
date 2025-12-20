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
