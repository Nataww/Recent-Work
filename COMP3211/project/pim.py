import os
from view import PIMView
from model import PIM

pim = PIM()
pimView = PIMView(pim)
pim.addContact("Ali", "Tehran", "09003456730")
pim.addEvent("Meeting", "Meeting with Ali", "2020-12-12 12:00", "2020-12-12 12:00")
pim.addTask("Task1", "Task1 description", "2020-12-12 12:00")
pim.addEvent("Conference", "Conference call with Team", "2020-12-13 15:30", "2020-12-13 15:30")
pim.addTask("Complete Report", "Finish quarterly report", "2020-12-14 09:00")
pim.addEvent("Lunch", "Lunch with Jane", "2020-12-15 12:30", "2020-12-15 12:30")
pim.addEvent("Lunch2", "Lunch with Jane", "2020-12-16 12:30", "2020-12-16 12:30")
pim.addTask("Project Deadline", "Submit project proposal", "2020-12-16 17:00")
pim.addEvent("Training", "Training session on new software", "2020-12-17 10:00", "2020-12-17 10:00")
pim.addTask("Client Meeting", "Prepare for client meeting", "2020-12-18 14:00")
pim.addEvent("Networking Event", "Attend industry networking event", "2020-12-19 18:00", "2020-12-19 18:00")
pim.addTask("Follow-up Emails", "Send follow-up emails from yesterday's meetings", "2020-12-20 09:30")
pim.addQuickNote("QuickNote1", "QuickNote1 description")

 

while True:
    print("Please select an action:")
    print("Q: Quick Note")
    print("T: Task")
    print("E: Event")
    print("C: Contact")
    print("S: Search items")
    print("IM: Import PIM file")
    print("EX: Export PIM file")
    action = input("Action: ")
    os.system('cls || clear')

    # Seach items function
    if action.upper() == "S":
        print("Please select the type for searching:")
        print("S: Text")
        print("T: Time")
        print("MC: Multiple Conditions")
        print("X: Exit to main menu")
        typeForSearch = input("Type: ")
        os.system('cls || clear')
        # Check the input
        while typeForSearch.upper() != "S" and typeForSearch.upper() != "T" and typeForSearch.upper() != "MC" and typeForSearch.upper() != "X":
            print("Invalid input!\n")
            print("Please select the type for searching:")
            print("S: Text")
            print("T: Time")
            print("MC: Multiple Conditions")
            print("X: Exit to main menu")
            typeForSearch = input("Type: ")
            os.system('cls || clear')
        if typeForSearch.upper() == "S":
            print("Please enter the text for searching:")
            searchText = input("Text: ")
            os.system('cls || clear')
            #do searching
            searchResult = pim.search(typeForSearch, searchText)
            if searchResult == False:
                continue
            if len(searchResult) > 0:
                pimView.showSearchResult(searchResult)
                print("Enter X to return main menu")
                print("Please select an index: ")
                selectedIndex = input("Index: ")
                os.system('cls || clear')
                if selectedIndex.upper() == "X":
                    continue
                if not selectedIndex.isnumeric():
                    print("Invalid index!")
                    continue
                if not pimView.listDetailByTypeAndIndex(searchResult[int(selectedIndex)-1][0], int(searchResult[int(selectedIndex)-1][2])-1):
                    continue
                print("E: Edit")
                print("D: Delete")
                print("X: Exit to main menu")
                print("Please select an action:")
                pirAction = input("Action: ")
                os.system('cls || clear')
                while pirAction.upper() not in ["E", "D", "X"]:
                    print("Invalid input!\n")
                    print("E: Edit")
                    print("D: Delete")
                    print("X: Exit to main menu")
                    print("Please select an action:")
                    pirAction = input("Action: ")
                    os.system('cls || clear')
                if pirAction.upper() == "E":
                    dataDict = pimView.handleUserInputAndGetEditDataDictByType(searchResult[int(selectedIndex)-1][0])
                    if dataDict is None:
                        continue
                    result = pim.editByTypeAndIndex(searchResult[int(selectedIndex)-1][0], int(searchResult[int(selectedIndex)-1][2])-1, dataDict)
                    if result:
                        print("The item is edited successfully.")
                    else:
                        print("The item is not edited.")
                elif pirAction.upper() == "D":
                    result = pim.deleteByTypeAndIndex(searchResult[int(selectedIndex)-1][0], int(searchResult[int(selectedIndex)-1][2])-1)
                    if result:
                        print("The item is deleted successfully.")
                    else:
                        print("The item is not deleted.")
            else:
                print("*************************\nThere is no result. \n*************************\n")
                continue
        elif typeForSearch.upper() == "T":
            print("Please enter the datetime for searching:")
            print("The format string is YYYY-MM-DD HH:MM")
            searchText = input("Date: ")
            os.system('cls || clear')
            print("Please enter the compare symbol:")
            print("=: Equal")
            print(">: Greater than")
            print("<: Less than")
            seachCompareSymbol = input("Symbol: ")
            os.system('cls || clear')
            searchResult = pim.search(typeForSearch, searchText, seachCompareSymbol)
            if searchResult == False:
                print("Invalid Datetime or Symbol!")
                continue
            if len(searchResult) > 0:
                pimView.showSearchResult(searchResult)
                print("Enter X to return main menu")
                print("Please select an index: ")
                selectedIndex = input("Index: ")
                os.system('cls || clear')
                if selectedIndex.upper() == "X":
                    continue
                if not selectedIndex.isnumeric():
                    print("Invalid index!")
                    continue
                if not pimView.listDetailByTypeAndIndex(searchResult[int(selectedIndex)-1][0], int(searchResult[int(selectedIndex)-1][2])-1):
                    continue
                print("E: Edit")
                print("D: Delete")
                print("X: Exit to main menu")
                print("Please select an action:")
                pirAction = input("Action: ")
                os.system('cls || clear')
                while pirAction.upper() not in ["E", "D", "X"]:
                    print("Invalid input!\n")
                    print("E: Edit")
                    print("D: Delete")
                    print("X: Exit to main menu")
                    print("Please select an action:")
                    pirAction = input("Action: ")
                    os.system('cls || clear')
                if pirAction.upper() == "E":
                    dataDict = pimView.handleUserInputAndGetEditDataDictByType(searchResult[int(selectedIndex)-1][0])
                    if dataDict is None:
                        continue
                    result = pim.editByTypeAndIndex(searchResult[int(selectedIndex)-1][0], int(searchResult[int(selectedIndex)-1][2])-1, dataDict)
                    if result:
                        print("The item is edited successfully.")
                    else:
                        print("The item is not edited.")
                elif pirAction.upper() == "D":
                    result = pim.deleteByTypeAndIndex(searchResult[int(selectedIndex)-1][0], int(searchResult[int(selectedIndex)-1][2])-1)
                    if result:
                        print("The item is deleted successfully.")
                    else:
                        print("The item is not deleted.")
            else:
                print("*************************\nThere is no result. \n*************************\n")
                continue
        elif typeForSearch.upper() == "MC":
            print("For multiple condition searching, you may allow searching a note, a description, a name, an address, or a mobile number for a note by using the operator (AND[&&], OR[||], NOT[!]) and the date by using the operator (BEFORE THE DATE[<], AFTER THR DATE[>], EXACTLY DATE[=])")
            print("\nExample: text=Lunch && datetime>2023-01-01 00:00")
            print("Example: text=Lunch || text=Dinner")
            print("\nPlease enter the conditions for searching:\n")
            searchText = input("Conditions: ")
            os.system('cls || clear')
            searchResult = pim.search(typeForSearch, searchText)
            if searchResult == False:
                continue
            if len(searchResult) > 0:
                pimView.showSearchResult(searchResult)
                print("Enter X to return main menu")
                print("Please select an index: ")
                selectedIndex = input("Index: ")
                os.system('cls || clear')
                if selectedIndex.upper() == "X":
                    continue
                if not selectedIndex.isnumeric():
                    print("Invalid index!")
                    continue
                if not pimView.listDetailByTypeAndIndex(searchResult[int(selectedIndex)-1][0], int(searchResult[int(selectedIndex)-1][2])-1):
                    continue
                print("E: Edit")
                print("D: Delete")
                print("X: Exit to main menu")
                print("Please select an action:")
                pirAction = input("Action: ")
                os.system('cls || clear')
                while pirAction.upper() not in ["E", "D", "X"]:
                    print("Invalid input!\n")
                    print("E: Edit")
                    print("D: Delete")
                    print("X: Exit to main menu")
                    print("Please select an action:")
                    pirAction = input("Action: ")
                    os.system('cls || clear')
                if pirAction.upper() == "E":
                    dataDict = pimView.handleUserInputAndGetEditDataDictByType(searchResult[int(selectedIndex)-1][0])
                    if dataDict is None:
                        continue
                    result = pim.editByTypeAndIndex(searchResult[int(selectedIndex)-1][0], int(searchResult[int(selectedIndex)-1][2])-1, dataDict)
                    if result:
                        print("The item is edited successfully.")
                    else:
                        print("The item is not edited.")
                elif pirAction.upper() == "D":
                    result = pim.deleteByTypeAndIndex(searchResult[int(selectedIndex)-1][0], int(searchResult[int(selectedIndex)-1][2])-1)
                    if result:
                        print("The item is deleted successfully.")
                    else:
                        print("The item is not deleted.")
            else:
                print("*************************\nThere is no result. \n*************************\n")
                continue 
        elif typeForSearch.upper() == "X":
            continue

    # Quick Note Control
    elif action.upper() == "Q":
        pimView.listDataByType("QuickNote")
        print("Please select an index (Enter: C to create new | Enter: X to return main menu):")
        selectedIndex = input("Index: ")
        os.system('cls || clear')
        if selectedIndex.upper() == "X":
            continue
        if selectedIndex.upper() == "C":
            print("Please enter the name [Enter X to return main menu]:")
            name = input("Name: ")
            if name == "":
                os.system("cls || clear")
                print("Name can not be empty!\n")
                continue
            if name.upper() == "X":
                os.system("cls || clear")
                continue
            print("Please enter the text [Enter X to return main menu]:")
            text = input("Text: ")
            if text.upper() == "X":
                os.system("cls || clear")
                continue
            os.system('cls || clear')
            result = pim.addQuickNote(name, text)
            if result:
                print("The quick note is created successfully.")
            else:
                print("The quick note is not created.")
            continue
        if not selectedIndex.isnumeric():
            print("Invalid index!\n")
            continue
        if not pimView.listDetailByTypeAndIndex("QuickNote", int(selectedIndex)-1):
            continue
        print("E: Edit")
        print("D: Delete")
        print("X: Exit to main menu")
        print("Please select an action:")
        pirAction = input("Action: ")
        os.system('cls || clear')
        while pirAction.upper() not in ["E", "D", "X"]:
            print("Invalid input!\n")
            print("E: Edit")
            print("D: Delete")
            print("X: Exit to main menu")
            print("Please select an action:")
            pirAction = input("Action: ")
            os.system('cls || clear')
        if pirAction.upper() == "E":
            dataDict = pimView.handleUserInputAndGetEditDataDictByType("QuickNote")
            if dataDict is None:
                continue
            result = pim.editByTypeAndIndex("QuickNote", int(selectedIndex)-1, dataDict)
            if result:
                print("The quick note is edited successfully.")
            else:
                print("The quick note is not edited.")
        elif pirAction.upper() == "D":
            result = pim.deleteByTypeAndIndex("QuickNote", int(selectedIndex)-1)
            if result:
                print("The quick note is deleted successfully.")
            else:
                print("The quick note is not deleted.")
    
    # Task Control
    elif action.upper() == "T":
        pimView.listDataByType("Task")
        print("Please select an index (Enter: C to create new | Enter: X to return main menu):")
        selectedIndex = input("Index: ")
        os.system('cls || clear')
        if selectedIndex.upper() == "X":
            continue
        if selectedIndex.upper() == "C":
            print("Please enter the name [Enter X to return main menu]:")
            name = input("Name: ")
            if name == "":
                os.system("cls || clear")
                print("Name can not be empty!\n")
                continue
            if name.upper() == "X":
                os.system("cls || clear")
                continue
            print("Please enter the description [Enter X to return main menu]:")
            description = input("Description: ")
            if description.upper() == "X":
                os.system("cls || clear")
                continue
            print("The format string is YYYY-MM-DD HH:MM")
            print("Please enter the deadline [Enter X to return main menu]:")
            deadline = input("Deadline: ")
            if deadline.upper() == "X":
                os.system("cls || clear")
                continue
            os.system('cls || clear')
            result = pim.addTask(name, description, deadline)
            if result:
                print("The task is created successfully.")
            else:
                print("The task is not created.")
            continue
        if not selectedIndex.isnumeric():
            print("Invalid index!\n")
            continue
        if not pimView.listDetailByTypeAndIndex("Task", int(selectedIndex)-1):
            continue
        print("E: Edit")
        print("D: Delete")
        print("X: Exit to main menu")
        print("Please select an action:")
        pirAction = input("Action: ")
        os.system('cls || clear')
        while pirAction.upper() not in ["E", "D", "X"]:
            print("Invalid input!\n")
            print("E: Edit")
            print("D: Delete")
            print("X: Exit to main menu")
            print("Please select an action:")
            pirAction = input("Action: ")
            os.system('cls || clear')
        if pirAction.upper() == "E":
            dataDict = pimView.handleUserInputAndGetEditDataDictByType("Task")
            if dataDict is None:
                continue
            result = pim.editByTypeAndIndex("Task", int(selectedIndex)-1, dataDict)
            if result:
                print("The task is edited successfully.")
            else:
                print("The task is not edited.")
        elif pirAction.upper() == "D":
            result = pim.deleteByTypeAndIndex("Task", int(selectedIndex)-1)
            if result:
                print("The task is deleted successfully.")
            else:
                print("The task is not deleted.")

    # Event Control
    elif action.upper() == "E":
        pimView.listDataByType("Event")
        print("Please select an index (Enter: C to create new | Enter: X to return main menu):")
        selectedIndex = input("Index: ")
        os.system('cls || clear')
        if selectedIndex.upper() == "X":
            continue
        if selectedIndex.upper() == "C":
            print("Please enter the name [Enter X to return main menu]:")
            name = input("Name: ")
            if name == "":
                os.system("cls || clear")
                print("Name can not be empty!\n")
                continue
            if name.upper() == "X":
                os.system("cls || clear")
                continue
            print("Please enter the description [Enter X to return main menu]:")
            description = input("Description: ")
            if description.upper() == "X":
                os.system("cls || clear")
                continue
            print("The format string is YYYY-MM-DD HH:MM")
            print("Please enter the starting time [Enter X to return main menu]:")
            startingTime = input("Starting Time: ")
            if startingTime.upper() == "X":
                os.system("cls || clear")
                continue
            print("The format string is YYYY-MM-DD HH:MM")
            print("Please enter the alarm time [Enter X to return main menu]:")
            alarmTime = input("Alarm Time: ")
            if alarmTime.upper() == "X":
                os.system("cls || clear")
                continue
            os.system('cls || clear')
            result = pim.addEvent(name, description, startingTime, alarmTime)
            if result:
                print("The event is created successfully.")
            else:
                print("The event is not created.")
            continue
        if not selectedIndex.isnumeric():
            print("Invalid index!\n")
            continue
        if not pimView.listDetailByTypeAndIndex("Event", int(selectedIndex)-1):
            continue
        print("E: Edit")
        print("D: Delete")
        print("X: Exit to main menu")
        print("Please select an action:")
        pirAction = input("Action: ")
        os.system('cls || clear')
        while pirAction.upper() not in ["E", "D", "X"]:
            print("Invalid input!\n")
            print("E: Edit")
            print("D: Delete")
            print("X: Exit to main menu")
            print("Please select an action:")
            pirAction = input("Action: ")
            os.system('cls || clear')
        if pirAction.upper() == "E":
            dataDict = pimView.handleUserInputAndGetEditDataDictByType("Event")
            if dataDict is None:
                continue
            result = pim.editByTypeAndIndex("Event", int(selectedIndex)-1, dataDict)
            if result:
                print("The event is edited successfully.")
            else:
                print("The event is not edited.")
        elif pirAction.upper() == "D":
            result = pim.deleteByTypeAndIndex("Event", int(selectedIndex)-1)
            if result:
                print("The event is deleted successfully.")
            else:
                print("The event is not deleted.")

    # Contact Control
    elif action.upper() == "C":
        pimView.listDataByType("Contact")
        print("Please select an index (Enter: C to create new | Enter: X to return main menu):")
        selectedIndex = input("Index: ")
        os.system('cls || clear')
        if selectedIndex.upper() == "X":
            continue
        if selectedIndex.upper() == "C":
            print("Please enter the name [Enter X to return main menu]:")
            name = input("Name: ")
            if name == "":
                os.system("cls || clear")
                print("Name can not be empty!\n")
                continue
            if name.upper() == "X":
                os.system("cls || clear")
                continue
            print("Please enter the address [Enter X to return main menu]:")
            address = input("Address: ")
            if address.upper() == "X":
                os.system("cls || clear")
                continue
            print("Please enter the mobile [Enter X to return main menu]:")
            mobile = input("Mobile: ")
            if mobile.upper() == "X":
                os.system("cls || clear")
                continue
            os.system('cls || clear')
            result = pim.addContact(name, address, mobile)
            if result:
                print("The contact is created successfully.")
            else:
                print("The contact is not created.")
            continue
        if not selectedIndex.isnumeric():
            print("Invalid index!\n")
            continue
        if not pimView.listDetailByTypeAndIndex("Contact", int(selectedIndex)-1):
            continue
        print("E: Edit")
        print("D: Delete")
        print("X: Exit to main menu")
        print("Please select an action:")
        pirAction = input("Action: ")
        os.system('cls || clear')
        while pirAction.upper() not in ["E", "D", "X"]:
            print("Invalid input!\n")
            print("E: Edit")
            print("D: Delete")
            print("X: Exit to main menu")
            print("Please select an action:")
            pirAction = input("Action: ")
            os.system('cls || clear')
        if pirAction.upper() == "E":
            dataDict = pimView.handleUserInputAndGetEditDataDictByType("Contact")
            if dataDict is None:
                continue
            result = pim.editByTypeAndIndex("Contact", int(selectedIndex)-1, dataDict)
            if result:
                print("The contact is edited successfully.")
            else:
                print("The contact is not edited.")
        elif pirAction.upper() == "D":
            result = pim.deleteByTypeAndIndex("Contact", int(selectedIndex)-1)
            if result:
                print("The contact is deleted successfully.")
            else:
                print("The contact is not deleted.")
    
    # Import PIM file
    elif action.upper() == "IM":
        print("Please enter the file name (without .pim) [Enter X to return main menu]:")
        fileName = input("FileName: ")
        os.system('cls || clear')
        if fileName == "X":
            continue
        pim.importPim(fileName)
    
    # Export PIM file
    elif action.upper() == "EX":
        print("Please enter the file name (without .pim) [Enter X to return main menu]:")
        fileName = input("FileName: ")
        os.system('cls || clear')
        if fileName == "X":
            continue
        pim.exportPim(fileName)
    
    # Not valid input
    else:
        print("Invalid input!\n\n")


