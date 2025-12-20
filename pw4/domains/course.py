class Course:
    def __init__(self, Cid, Cname, credits):
        self.__course_id = Cid
        self.__course_name = Cname
        self.__credits = credits

    def getCID(self):
        return self.__course_id

    def getCNAME(self):
        return self.__course_name

    def getCredit(self):
        return self.__credits

    def print(self):
        return [f"Course ID: {self.getCID()}",
                f"Course Name: {self.getCNAME()}",
                f"Course Credit: {self.getCredit()}"]
