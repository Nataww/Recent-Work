class Contact:
    #initialise the class
    def __init__(self, name, address, mobile):
        self.name = name
        self.address = address
        self.mobile = mobile
    
    #read the name
    def readName(self):
        return self.name
    
    #edit the name
    def editName(self, name):
        self.name = name

    #read the address
    def readAddress(self):
        return self.address
    
    #edit the address
    def editAddress(self, address):
        self.address = address
    
    #read the mobile
    def readMobile(self):
        return self.mobile
    
    #edit the mobile
    def editMobile(self, mobile):
        self.mobile = mobile
    
    #show the detail of the contact
    def showDetail(self):
        print("*************************")
        print(f"Name: {self.name}")
        print(f"Address: {self.address}")
        print(f"Mobile: {self.mobile}")
        print("*************************\n")
