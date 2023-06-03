from tkinter import *
from tkinter.ttk import *
import requests

mainWindow=Tk(className="Nöbetçi Eczaneler | Proje Ödevi - Mustafa Koloğlu")

baseApiUrl = "https://ne.kobisoft.net/v2/"

#################################################
# Cities Combobox
#################################################
selectedCityId = 0
cities = []

def getCities():
    global cities
    cities = requests.get(baseApiUrl + 'cities').json()

    insertCityList()

def insertCityList():
    cityNames = []

    for value in cities["data"]:
        cityNames.append(value["name"])

    cityCombo["values"] = cityNames
    cityCombo.bind("<<ComboboxSelected>>", selectedCityCallback)


def selectedCityCallback(event):
     setCityIdByName(event.widget.get())  
     getCountiesByCityId()
     
def setCityIdByName(cityName):
    global selectedCityId
    selectedCityId = findCityIdByName(cityName)

def findCityIdByName(cityName):
    for i in cities["data"]:
        if cityName == i["name"] :
            return i["id"]

cityClicked = StringVar()
cityCombo = Combobox(mainWindow, textvariable = cityClicked) 
cityCombo.grid(column = 1, row = 0,pady=10, sticky=NW) 
cityCombo.current()
#################################################

#################################################
# Counties ComboBox
#################################################
selectedCountyId = 0
counties = []

def getCountiesByCityId():
    global counties
    counties = requests.get(baseApiUrl + 'counties?cityId=' + str(selectedCityId)).json()

    insertCountyList()


def insertCountyList():
    countyNames = []

    for value in counties["data"]:
        countyNames.append(value["countyName"])

    countyCombo["values"] = countyNames
    countyCombo.bind("<<ComboboxSelected>>", selectedCountyCallback)


def selectedCountyCallback(event):
     setCountyIdByName(event.widget.get())  

def setCountyIdByName(countyName):
    global selectedCountyId
    selectedCountyId = findCountyIdByName(countyName)

def findCountyIdByName(countyName):
    for i in counties["data"]:
        if countyName == i["countyName"] :
            return i["countyId"]

countyClicked = StringVar()
countyCombo = Combobox(mainWindow, textvariable = countyClicked) 
countyCombo.grid(column = 3, row = 0,pady=10, sticky=NW) 
countyCombo.current()
#################################################

#################################################
# Button
#################################################
def getPharmacies():
    pharmacyResponse = requests.get(baseApiUrl + 'pharmacies?countyId=' + str(selectedCountyId)).json()

    pharmacies = []

    for pharmacy in pharmacyResponse["data"]:
        pharmacies.append((pharmacy["name"], pharmacy["phoneNumber"], pharmacy["address"],pharmacy["countyName"]))

    insertPharmacyList(pharmacies)


def insertPharmacyList(pharmacies):
    gridPharmacy.delete(*gridPharmacy.get_children())

    for data in pharmacies:
        gridPharmacy.insert('', END,text=data[0], values=(data[1],data[2],data[3]))


button = Button( mainWindow , text = "Nöbetçi Eczane Bul",command=getPharmacies) 
button.grid(column = 4, row = 0,pady=10, sticky=NW) 
#################################################

#################################################
# Labels
#################################################
labelCity = Label( mainWindow , text = "Şehir :")
labelCity.grid(column=0,row=0,padx=10,pady=10,sticky=NW)

labelCounty = Label( mainWindow , text = "İlçe :")
labelCounty.grid(column=2,row=0,pady=10,sticky=NW)
#################################################

#################################################
# Grid
#################################################
gridPharmacy = Treeview(mainWindow)
gridPharmacy["columns"]=("col1","col2","col3")
gridPharmacy.heading("#0",text="İsim",anchor=W)
gridPharmacy.heading("#1",text="Telefon",anchor=W)
gridPharmacy.heading("#2",text="Adres",anchor=W)
gridPharmacy.heading("#3",text="İlçe",anchor=W)
gridPharmacy.column('#1', stretch=YES,width=100,anchor=W)
gridPharmacy.column('#2', stretch=YES,width=300,anchor=W)
gridPharmacy.column('#3', stretch=YES,width=120,anchor=W)
gridPharmacy.grid(row=1, column=0,columnspan=5,padx=10, pady=10, sticky=NW)
#################################################

getCities()

mainloop()