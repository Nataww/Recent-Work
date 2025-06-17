from datetime import datetime
import os
import json

class PIM:
    #import the class
    from quicknote import QuickNote
    from task import Task
    from event import Event
    from contact import Contact

    #initialise the class
    def __init__(self):
        self.quickNotes = []
        self.tasks = []
        self.events = []
        self.contacts = []

    #add a quick note
    def addQuickNote(self,name, storeText):
        newQuickNote = self.QuickNote(name, storeText)
        self.quickNotes.append(newQuickNote)
        return True

    #add a task
    def addTask(self,name, description, deadline):
        try:
            newTask = self.Task(name, description, deadline)
        except ValueError as e:
            print(e)
            return False
        self.tasks.append(newTask)
        return True
    
    #add an event
    def addEvent(self, name, description, startingTime, alarmTime):
        try:
            newEvent = self.Event(name,description, startingTime, alarmTime)
        except ValueError as e:
            print(e)
            return False
        self.events.append(newEvent)
        return True

    #add a contact
    def addContact(self, name, address, mobile):
        newContact = self.Contact(name, address, mobile)
        self.contacts.append(newContact)
        return True
    
    #get the data list
    def getQuickNotesList(self):
        return self.quickNotes
    
    #get the data list
    def getTasksList(self):
        return self.tasks
    
    #get the data list
    def getEventsList(self):
        return self.events
    
    #get the data list
    def getContactsList(self):
        return self.contacts

    #edit the data by type and index
    def editByTypeAndIndex(self, typeName, index, inputDataDict):
        index = str(index)
        if not index.isnumeric():
            print("Invalid index!\n")
            return False
        index = int(index)
        if index < 0:
            print("Invalid index!\n")
            return False
        if typeName == "QuickNote":
            if index > len(self.quickNotes) - 1:
                print("Invalid index!\n")
                return False
            newName = inputDataDict["name"]
            newText = inputDataDict["storeText"]
            self.quickNotes[index].editName(newName)
            self.quickNotes[index].editStoreText(newText)
        elif typeName == "Task":
            if index > len(self.tasks) - 1:
                print("Invalid index!\n")
                return False
            newDeadline = inputDataDict["deadline"]
            newName = inputDataDict["name"]
            newDescription = inputDataDict["description"]
            try:
                self.tasks[index].editDeadline(newDeadline)
            except ValueError as e:
                print(e)
                return False
            self.tasks[index].editName(newName)
            self.tasks[index].editDescription(newDescription)
        elif typeName == "Event":
            if index > len(self.events) - 1:
                print("Invalid index!\n")
                return False
            newStartingTime = inputDataDict["startingTime"]
            newAlarmTime = inputDataDict["alarmTime"]
            newName = inputDataDict["name"]
            newDescription = inputDataDict["description"]
            tempStartingTimeString = self.events[index].readStartingTimeStr()
            tempAlarmTimeString = self.events[index].readAlarmTimeStr()
            try:
                self.events[index].editStartingTime(newStartingTime)
                self.events[index].editAlarmTime(newAlarmTime)
            except ValueError as e:
                print(e)
                self.events[index].editStartingTime(tempStartingTimeString, True)
                self.events[index].editAlarmTime(tempAlarmTimeString, True)
                return False
            self.events[index].editName(newName)
            self.events[index].editDescription(newDescription)
        elif typeName == "Contact":
            if index > len(self.contacts) - 1:
                print("Invalid index!\n")
                return False
            newName = inputDataDict["name"]
            newAddress = inputDataDict["address"]
            newMobile = inputDataDict["mobile"]
            self.contacts[index].editName(newName)
            self.contacts[index].editAddress(newAddress)
            self.contacts[index].editMobile(newMobile)
        else:
            print("Invalid type!\n")
            return False
        return True
    
    #delete the data by type and index
    def deleteByTypeAndIndex(self, typeName, index):
        index = str(index)
        if not index.isnumeric():
            print("Invalid index!\n")
            return False
        index = int(index)
        if index < 0:
            print("Invalid index!\n")
            return False
        if typeName == "QuickNote":
            if index > len(self.quickNotes) - 1:
                print("Invalid index!\n")
                return False
            self.quickNotes.pop(index)
        elif typeName == "Task":
            if index > len(self.tasks) - 1:
                print("Invalid index!\n")
                return False
            self.tasks.pop(index)
        elif typeName == "Event":
            if index > len(self.events) - 1:
                print("Invalid index!\n")
                return False
            self.events.pop(index)
        elif typeName == "Contact":
            if index > len(self.contacts) - 1:
                print("Invalid index!\n")
                return False
            self.contacts.pop(index)
        else:
            print("Invalid type!\n")
            return False
        return True

    
    #search the data by text
    def __searchByText(self, searchText, negative=False):
        searchList = []
        for index,value in enumerate(self.quickNotes):
            if searchText in value.readName() or searchText in value.readStoreText():
                if not negative:
                    searchList.append(["QuickNote", value.readName(), index+1])
            else:
                if negative:
                    searchList.append(["QuickNote", value.readName(), index+1])
        for index,value in enumerate(self.tasks):
            if searchText in value.readName() or searchText in value.readDescription():
                if not negative:
                    searchList.append(["Task", value.readName(), index+1])
            else:
                if negative:
                    searchList.append(["Task", value.readName(), index+1])
        for index,value in enumerate(self.events):
            if searchText in value.readName() or searchText in value.readDescription():
                if not negative:
                    searchList.append(["Event", value.readName(), index+1])
            else:
                if negative:
                    searchList.append(["Event", value.readName(), index+1])
        for index,value in enumerate(self.contacts):
            if searchText in value.readName() or searchText in value.readAddress() or searchText in value.readMobile():
                if not negative:
                    searchList.append(["Contact", value.readName(), index+1])
            else:
                if negative:
                    searchList.append(["Contact", value.readName(), index+1])
        return searchList
        
    #search the data by time
    def __searchByTime(self, searchText, timeCompare, negative=False):
        searchList = []
        try:
            datetime_object = datetime.strptime(searchText, "%Y-%m-%d %H:%M")
        except ValueError:
            return False
            
        for index,value in enumerate(self.events):
            if timeCompare == "=":
                if value.readStartingTime() == datetime_object or value.readAlarmTime() == datetime_object:
                    if not negative:
                        searchList.append(["Event", value.readName(), index+1])
                else:
                    if negative:
                        searchList.append(["Event", value.readName(), index+1])
            elif timeCompare == ">":
                if value.readStartingTime() > datetime_object or value.readAlarmTime() > datetime_object:
                    if not negative:
                        searchList.append(["Event", value.readName(), index+1])
                else:
                    if negative:
                        searchList.append(["Event", value.readName(), index+1])
            elif timeCompare == "<":
                if value.readStartingTime() < datetime_object or value.readAlarmTime() < datetime_object:
                    if not negative:
                        searchList.append(["Event", value.readName(), index+1])
                else:
                    if negative:
                        searchList.append(["Event", value.readName(), index+1])
            else:
                return False
        for index,value in enumerate(self.tasks):
            if timeCompare == "=":
                if value.readDeadline() == datetime_object:
                    if not negative:
                        searchList.append(["Task", value.readName(), index+1])
                else:
                    if negative:
                        searchList.append(["Task", value.readName(), index+1])
            elif timeCompare == ">":
                if value.readDeadline() > datetime_object:
                    if not negative:
                        searchList.append(["Task", value.readName(), index+1])
                else:
                    if negative:
                        searchList.append(["Task", value.readName(), index+1])
            elif timeCompare == "<":
                if value.readDeadline() < datetime_object:
                    if not negative:
                        searchList.append(["Task", value.readName(), index+1])
                else:
                    if negative:
                        searchList.append(["Task", value.readName(), index+1])

        return searchList

    #search the data by multiple conditions
    def __searchByMC(self, searchText):
        splitAndConditions = searchText.split("&&")
        tempAndSearchList = []
        for i in splitAndConditions:
            splitOrConditions = i.split("||")
            tempOrSearchList = []
            for x in splitOrConditions:
                x = x.strip()
                hasNegative = "!" in x
                # =
                if "=" in x:
                    splitStringFromCommand = x.split("=")
                    searchCommand = splitStringFromCommand[0].strip().replace("!", "")
                    searchValue = splitStringFromCommand[1].strip()
                    if searchCommand == "text":
                        tempOrSearchList = tempOrSearchList + self.__searchByText(searchValue, hasNegative)
                    elif searchCommand == "datetime":
                        __tempList = self.__searchByTime(searchValue, "=", hasNegative)
                        if not __tempList:
                            print("The format string is incorrect.")
                            return False
                        tempOrSearchList = tempOrSearchList + __tempList
                    else:
                        print(f"{x} is not a valid command.")
                        return False
                # >
                elif ">" in x:
                    splitStringFromCommand = x.split(">")
                    searchCommand = splitStringFromCommand[0].strip().replace("!", "")
                    searchValue = splitStringFromCommand[1].strip()
                    if searchCommand == "datetime":
                        __tempList = self.__searchByTime(searchValue, ">", hasNegative)
                        if not __tempList:
                            print("The format string is incorrect.")
                            return False
                        tempOrSearchList = tempOrSearchList + __tempList
                    else:
                        print(f"{x} is not a valid command.")
                        return False
                # <
                elif "<" in x:
                    splitStringFromCommand = x.split("<")
                    searchCommand = splitStringFromCommand[0].strip().replace("!", "")
                    searchValue = splitStringFromCommand[1].strip()
                    if searchCommand == "datetime":
                        __tempList = self.__searchByTime(searchValue, "<", hasNegative)
                        if not __tempList:
                            print("The format string is incorrect.")
                            return False
                        tempOrSearchList = tempOrSearchList + __tempList
                    else:
                        print(f"{x} is not a valid command.")
                        return False
                else:
                    print(f"{x} is not a valid command.")
                    return False
            result = []
            for sublist in tempOrSearchList:
                if sublist not in result:
                    result.append(sublist)
            tempAndSearchList = tempAndSearchList + result
        if len(splitAndConditions) > 1:
            seen = set()
            searchList = []

            for sublist in tempAndSearchList:
                if tuple(sublist) in seen:
                    searchList.append(sublist)
                seen.add(tuple(sublist))
        else:
            searchList = tempAndSearchList
        return searchList
    
    #search main function
    def search(self, typeForSearch, searchText, timeCompare=None,):
        if typeForSearch.upper() != "S" and typeForSearch.upper() != "T" and typeForSearch.upper() != "MC":
            return False
        if typeForSearch.upper() == "S":
            searchList = self.__searchByText(searchText) #[[type, name, index], [type, name, index], ...
            return searchList
        elif typeForSearch.upper() == "T":
            searchList = self.__searchByTime(searchText, timeCompare) #[[type, name, index], [type, name, index], ...
            if searchList == None:
                print("The format string is incorrect.")
                return False
            return searchList
        elif typeForSearch.upper() == "MC":
            searchList = self.__searchByMC(searchText) #[[type, name, index], [type, name, index], ...
            if searchList == None:
                print("The format string is incorrect.")
                return False
            return searchList

    #export the data to a file
    def exportPim(self, fileName):
        try:
            quickNotesStore = []
            for i in self.quickNotes:
                quickNotesStore.append([i.readName(), i.readStoreText()])
            tasksStore = []
            for i in self.tasks:
                tasksStore.append([i.readName(), i.readDescription(), i.readDeadline().strftime("%Y-%m-%d %H:%M")])
            eventsStore = []
            for i in self.events:
                eventsStore.append([i.readName(), i.readDescription(), i.readStartingTime().strftime("%Y-%m-%d %H:%M"), i.readAlarmTime().strftime("%Y-%m-%d %H:%M")])
            contactsStore = []
            for i in self.contacts:
                contactsStore.append([i.readName(), i.readAddress(), i.readMobile()])
            data = {
                "quickNotes": quickNotesStore,
                "tasks": tasksStore,
                "events": eventsStore,
                "contacts": contactsStore
            }
            currentPath = os.path.dirname(os.path.abspath(__file__))
            filePath = os.path.join(currentPath, fileName+".pim")
            # Write the data to the JSON file
            with open(filePath, 'w') as json_file:
                json.dump(data, json_file)
        except:
            return False
        print(f'Data saved to {filePath}')
        print("The file is exported successfully.")
        return True

    #import the data from a file
    def importPim(self, fileName):
        currentPath = os.path.dirname(os.path.abspath(__file__))
        filePath = os.path.join(currentPath, fileName+".pim")
        if not os.path.exists(filePath):
            print("The file does not exist.")
            return False
        try:
            with open(filePath, "r") as f:
                data = json.load(f)
        except:
            print("The file is not a valid pim file.")
            return False
        self.quickNotes.clear()
        self.tasks.clear()
        self.events.clear()
        self.contacts.clear()
        for i in data["quickNotes"]:
            self.addQuickNote(i[0], i[1])
        for i in data["tasks"]:
            self.addTask(i[0], i[1], i[2])
        for i in data["events"]:
            self.addEvent(i[0], i[1], i[2], i[3])
        for i in data["contacts"]:
            self.addContact(i[0], i[1], i[2])
        print(f"Data loaded from {filePath}")
        print("The file is imported successfully.")
        return True
