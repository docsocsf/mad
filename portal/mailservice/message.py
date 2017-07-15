class Message:
    def __init__(self, student, subject, message):
        if not subject or not message:
            raise ValueError("Subject and message cannot be empty")

        self.__student = student
        self.__subject = subject
        self.__message = message

    def recipient(self):
        return "%s@ic.ac.uk" % self.__student.username

    def subject(self):
        return self.__subject

    def message(self):
        return "Hi %s \n\n %s \n\nBest regards,\nYour Departmental Representatives" \
               % (self.__student.name, self.__message)
