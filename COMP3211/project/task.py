from datetime import datetime

class Task:
    #initialise the class
    def __init__(self, name, description, deadline):
        self.description = description
        try:
            self.deadline = datetime.strptime(deadline, "%Y-%m-%d %H:%M")
        except ValueError:
            raise ValueError("The format string is incorrect.")
            
        self.name = name
    
    #read the description
    def readDescription(self):
        return self.description
    
    #edit the description
    def editDescription(self, description):
        self.description = description
    
    #read the deadline
    def readDeadline(self):
        return self.deadline
    
    #read the deadline to string
    def readDeadlineStr(self):
        return self.deadline.strftime("%Y-%m-%d %H:%M")
    
    #edit the deadline
    def editDeadline(self, deadline):
        try:
            self.deadline = datetime.strptime(deadline, "%Y-%m-%d %H:%M")
        except ValueError:
            raise ValueError("The format string is incorrect.")
    
    #read the name
    def readName(self):
        return self.name
    
    #edit the name
    def editName(self, name):
        self.name = name
    
    #show the detail of the task
    def showDetail(self):
        print("*************************")
        print(f"Name: {self.name}")
        print(f"Description: {self.description}")
        print(f"Deadline: {self.deadline}")
        print("*************************\n")
