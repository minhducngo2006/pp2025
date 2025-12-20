class Student:
    def __init__(self, Sid, Sname, Sdob):
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

    def setGPA(self, gpa):
        self.__gpa = gpa

    def getGPA(self):
        return self.__gpa

    def print(self):
        return [f"Student ID: {self.getID()}",
                f"Student Name: {self.getName()}",
                f"Student DOB: {self.getDOB()}",
                f"Student GPA: {self.getGPA():.2f}"]
