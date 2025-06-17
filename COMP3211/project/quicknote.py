class QuickNote:
    #initialise the class
    def __init__(self, name, storeText):
        self.storeText = storeText
        self.name = name
    
    #read the storeText
    def readStoreText(self):
        return self.storeText
    
    #edit the storeText
    def editStoreText(self, storeText):
        self.storeText = storeText
    
    #read the name
    def readName(self):
        return self.name
    
    #edit the name
    def editName(self, name):
        self.name = name

    #show the detail of the quick note
    def showDetail(self):
        print("*************************")
        print(f"Name: {self.name}")
        print(f"Text: {self.storeText}")
        print("*************************\n")
