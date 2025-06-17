from datetime import datetime

class Event:
    #initialise the class
    def __init__(self, name, description, startingTime, alarmTime):
        self.description = description
        try:
            self.startingTime = datetime.strptime(startingTime, "%Y-%m-%d %H:%M")
            self.alarmTime = datetime.strptime(alarmTime, "%Y-%m-%d %H:%M")
        except ValueError:
            raise ValueError("The format string is incorrect.")
        if self.alarmTime > self.startingTime:
            raise ValueError("The alarm time cannot later than the starting time.")
        self.name = name
    
    #read the description
    def readDescription(self):
        return self.description
    
    #edit the description
    def editDescription(self, description):
        self.description = description

    #read the starting time
    def readStartingTime(self):
        return self.startingTime
    
    #read the starting time to string
    def readStartingTimeStr(self):
        return self.startingTime.strftime("%Y-%m-%d %H:%M")
    
    #edit the starting time
    def editStartingTime(self, startingTime, withoutChecking = False):
        try:
            self.startingTime = datetime.strptime(startingTime, "%Y-%m-%d %H:%M")
        except ValueError:
            raise ValueError("The format string is incorrect.")
        if self.alarmTime > self.startingTime and withoutChecking == False:
            raise ValueError("The alarm time cannot later than the starting time.")
    
    #read the alarm time
    def readAlarmTime(self):
        return self.alarmTime
    
    #read the alarm time to string
    def readAlarmTimeStr(self):
        return self.alarmTime.strftime("%Y-%m-%d %H:%M")
    
    #edit the alarm time
    def editAlarmTime(self, alarmTime, withoutChecking = False):
        try:
            self.alarmTime = datetime.strptime(alarmTime, "%Y-%m-%d %H:%M")
        except ValueError:
            raise ValueError("The format string is incorrect.")
        if self.alarmTime > self.startingTime and withoutChecking == False:
            raise ValueError("The alarm time cannot later than the starting time.")
    
    #read the name
    def readName(self):
        return self.name
    
    #edit the name
    def editName(self, name):
        self.name = name
    
    #show the detail of the event
    def showDetail(self):
        print("*************************")
        print(f"Name: {self.name}")
        print(f"Description: {self.description}")
        print(f"Starting Time: {self.startingTime}")
        print(f"Alarm Time: {self.alarmTime}")
        print("*************************\n")

