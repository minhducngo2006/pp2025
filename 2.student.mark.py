class Student:  
    def __init__(self,Sid,Sname,Sdob):
        self.__id = Sid 
        self.__name = Sname
        self.__dob = Sdob
    def getName(self):
        return self.__name
    def getID(self):
        return self.__id
    def getDOB(self):
        return self.__dob  
    def print(self):
        print("=======Student database========")
        print(f"Student ID: {self.getID()} ")
        print(f"Student Name: {self.getName()}")
        print(f"Student DOB: {self.getDOB()}")


class Course:
    def __init__(self,Cid,Cname):
        self.__course_id = Cid
        self.__course_name = Cname
    def getCID(self):
        return self.__course_id
    def getCNAME(self):
        return self.__course_name
    def print(self):
        print("=======Course database========")
        print(f"Course ID: {self.getCID()}")
        print(f"COurse Name: {self.getCNAME()}")
class Mark:
    def __init__(self):
        self.__marks = {}
    def markInput(self,students,courses):
        choice = input("Input the course ID you want to set mark: ")
        cid = [c.getCID() for c in courses]
        if choice not in cid:
            print("Course not found!!!!!!!")
            return
        if choice not in self.__marks:
            self.__marks[choice] = {}
        for student in students:
            mark = float(input(f"Input the marks for {student.getName()}:  "))
            if 0 <= mark <= 20:
                self.__marks[choice][student.getID()] = mark
            else:
                print("The mark for students must between 0 and 20")
                exit()
    def display_mark(self,students):
        choice = input("Choose which course you want to show mark: ")
        if choice not in self.__marks:
            print("Course has no mark!!!")
            return
        print(f"========Mark for course {choice}=========")
        for student in students:
            if student.getID() in self.__marks[choice]:
                print(f"Mark for student {student.getName()} ({student.getID()})is: {self.__marks[choice][student.getID()]}")
            else:
                print(f"Mark for student {student.getName()}is: Empty!!!")


class Manager:
    def __init__(self):
        self.students = []
        self.courses = []
        self.mark = Mark()
    def student_info(self):
        student_num = int(input("Enter the number of students: "))
        if student_num <0:
            print("number of student must >0")
            exit()
        for i in range(0,student_num):
            print(f"======Student {i+1} info=======")
            sid = input("Input student ID: ")
            sname = input("Input student name: ")
            sdob = input("Input student date of birth: ")
            self.students.append(Student(sid,sname,sdob))
    def course_info(self):
        course_num = int(input("Input number of course: "))
        if course_num <0:
            print("The number of course must >0")
            exit()
        for i in range(0,course_num):
            print(f"========Course {i+1} info========= ")
            cid = input("Course ID: ")
            cname = input("Course name: ")
            self.courses.append(Course(cid,cname))
    def display_student(self):
        for s in self.students:
            s.print()
    def display_course(self):
        for c in self.courses:
            c.print()
    def mark_input(self):
        self.mark.markInput(self.students,self.courses)
    def displayMark(self):
        self.mark.display_mark(self.students)

def main():
    m = Manager()
    m.student_info()
    m.course_info()
    m.mark_input()
    m.display_student()
    m.display_course()
    m.displayMark()
   
main()



    







