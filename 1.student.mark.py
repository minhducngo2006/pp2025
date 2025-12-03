list_student = []
list_course = []
marks = {}
def student_info():
    student_id = input("input ID: ")
    student_name = input("Input student fullname: ")
    student_DOB = input("Input student DOB: ")
    list_student.append ({
        'id' : student_id,
        'name': student_name,
        'DOB' : student_DOB
    })
def input_mark():
    choice = input("Choose the course id you want to add mark: ")
    if choice not in marks:
        marks[choice] = {}
    for student in list_student:
            mark = float(input(f"Mark for {student['name']}: "))
            if 0<= mark <= 20:    
                marks[choice][student['id']] = mark
            else:
                print("Mark must be >=0 and <=20")
                exit()
def course_info():
    course_ID = input("Input course ID: ")
    course_name = input("input course name: ")
    list_course.append ({
        'course_id' : course_ID,
        'course_name': course_name
    })
def display_student():
    for student in list_student:
        print("===========Student database============")
        print(f"Student ID: {student['id']}\nStudent name: {student['name']}\nStudent DOB {student['DOB']}")
def display_course():
    for course in list_course:
        print("===========Course database============")
        print(f"Course ID: {course["course_id"]}\nCourse Name: {course['course_name']}\n ")

def display_mark():
    choice = input("Choose which course you want to show mark: ")
    if choice not in marks:
        print("Course has no mark!!!")
        return
    print(f"========Mark for course {choice}=========")
    for student in list_student:
        if student['id'] in marks[choice]:
            print(f"Mark for student {student['name']} ({student['id']})is: {marks[choice][student['id']]}")
        else:
            print(f"Mark for student {student['id']}is: Empty!!!")

student_num = int(input("input the number of student: "))
course_num = int(input("Input number of course: "))
if student_num < 0 or course_num <0:
    print("Number of student  and course must > 0")
else:
    for i in range(student_num):
        print(f"========Student {i+1} info========== ")
        student_info()
    for i in range(course_num):
        print(f"=============Course {i+1} info===========")
        course_info()
    input_mark()
    display_student()
    display_course()
    display_mark()
        