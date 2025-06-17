import os

class PIMView:
    __listHeader = ["Index", "Name"]
    __searchListHeader = ["Index", "Type", "Name"]

    def __init__(self, pim):
        self.pim = pim

    #list all the data by type
    def listDataByType(self, typeName):
        objectList = []
        if typeName == "QuickNote":
            objectList = self.pim.getQuickNotesList()
        elif typeName == "Task":
            objectList = self.pim.getTasksList()
        elif typeName == "Event":
            objectList = self.pim.getEventsList()
        elif typeName == "Contact":
            objectList = self.pim.getContactsList()
        else:
            print("Invalid type!\n")
            return False
        print("*************************")
        print(f"{typeName}:")
        print(f"{self.__listHeader[0]:<10}",self.__listHeader[1])
        for index, value in enumerate(objectList):
            print(f"{index+1:<10}",f"{value.readName():<10}")
        print("*************************\n")
        return True

    #list the data deails by type and Index
    def listDetailByTypeAndIndex(self, typeName, index):
        index = str(index)
        if not index.isnumeric():
            print("Invalid index!\n")
            return False
        index = int(index)
        if index < 0:
            print("Invalid index!\n")
            return False
        if typeName == "QuickNote":
            if index > len(self.pim.getQuickNotesList()) - 1:
                print("Invalid index!\n")
                return False
            self.pim.getQuickNotesList()[index].showDetail()
        elif typeName == "Task":
            if index > len(self.pim.getTasksList()) - 1:
                print("Invalid index!\n")
                return False
            self.pim.getTasksList()[index].showDetail()
        elif typeName == "Event":
            if index > len(self.pim.getEventsList()) - 1:
                print("Invalid index!\n")
                return False
            self.pim.getEventsList()[index].showDetail()
        elif typeName == "Contact":
            if index > len(self.pim.getContactsList()) - 1:
                print("Invalid index!\n")
                return False
            self.pim.getContactsList()[index].showDetail()
        else:
            print("Invalid type!\n")
            return False
        return True

    def handleUserInputAndGetEditDataDictByType(self, type):
        if type == "QuickNote":
            print("Please enter the new name [Enter X to return main menu]:")
            newName = input("Name: ")
            os.system("cls || clear")
            if newName == "":
                print("Name can not be empty!\n")
                return None
            if newName.upper() == "X":
                return None
            print("Please enter the new text [Enter X to return main menu]:")
            newText = input("Text: ")
            os.system("cls || clear")
            if newText.upper() == "X":
                return None
            dataDict = {"name": newName, "storeText": newText}
        elif type == "Task":
            print("Please enter the new name [Enter X to return main menu]:")
            newName = input("Name: ")
            os.system("cls || clear")
            if newName == "":
                print("Name can not be empty!\n")
                return None
            if newName.upper() == "X":
                return None
            print("Please enter the new description [Enter X to return main menu]:")
            newDescription = input("Description: ")
            os.system("cls || clear")
            if newDescription.upper() == "X":
                return None
            print("The format string is YYYY-MM-DD HH:MM")
            print("Please enter the new deadline [Enter X to return main menu]:")
            newDeadline = input("Deadline: ")
            os.system("cls || clear")
            if newDeadline.upper() == "X":
                return None
            dataDict = {"name": newName, "description": newDescription, "deadline": newDeadline}
        elif type == "Event":
            print("Please enter the new name [Enter X to return main menu]:")
            newName = input("Name: ")
            os.system("cls || clear")
            if newName == "":
                print("Name can not be empty!\n")
                return None
            if newName.upper() == "X":
                return None
            print("Please enter the new description [Enter X to return main menu]:")
            newDescription = input("Description: ")
            os.system("cls || clear")
            if newDescription.upper() == "X":
                return None
            print("The format string is YYYY-MM-DD HH:MM")
            print("Please enter the new starting time [Enter X to return main menu]:")
            newStartingTime = input("Starting Time: ")
            os.system("cls || clear")
            if newStartingTime.upper() == "X":
                return None
            print("The format string is YYYY-MM-DD HH:MM")
            print("Please enter the new alarm time [Enter X to return main menu]:")
            newAlarmTime = input("Alarm Time: ")
            os.system("cls || clear")
            if newAlarmTime.upper() == "X":
                return None
            dataDict = {"name": newName, "description": newDescription, "startingTime": newStartingTime, "alarmTime": newAlarmTime}
        elif type == "Contact":
            print("Please enter the new name [Enter X to return main menu]:")
            newName = input("Name: ")
            os.system("cls || clear")
            if newName == "":
                print("Name can not be empty!\n")
                return None
            if newName.upper() == "X":
                return None
            print("Please enter the new address [Enter X to return main menu]:")
            newAddress = input("Address: ")
            os.system("cls || clear")
            if newAddress.upper() == "X":
                return None
            print("Please enter the new mobile [Enter X to return main menu]:")
            newMobile = input("Mobile: ")
            os.system("cls || clear")
            if newMobile.upper() == "X":
                return None
            dataDict = {"name": newName, "address": newAddress, "mobile": newMobile}
        else:
            return False
        return dataDict


    def showSearchResult(self, searchResult):
        print("Search Result:")
        print("*************************")
        print(f"{self.__searchListHeader[0]:<5}",f"{self.__searchListHeader[1]:<10}",self.__searchListHeader[2])
        for index,value in enumerate(searchResult):
            print(f"{index+1:<5}",f"{value[0]:<10}",value[1])
        print("*************************\n")