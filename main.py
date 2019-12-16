import json
import pandas as pd

class User(object):
    """__init__() functions as the class constructor"""
    def __init__(self, uid=None, id=None):
        self.uid = uid
        self.schulklassen = []
        self.schulzimmer = []
        self.regeln = []

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

     
class Schulklasse(object):
    """__init__() functions as the class constructor"""
    def __init__(self, id=None, uid=None, name=None):
        self.id = id
        self.personId = uid
        self.name = name
        self.schueler = []

class Schulzimmer(object):
    """__init__() functions as the class constructor"""
    def __init__(self, uid=None, id=None, name=None):
        self.personId = uid
        self.id = id
        self.name = name 
class Regel(object):
    """__init__() functions as the class constructor"""
    def __init__(self, uid=None, id=None, name=None):
        self.uid = uid
        self.id = id
        self.name = name           

class Schueler(object):
    """__init__() functions as the class constructor"""
    def __init__(self, id=None, schulklassenId=None, name=None, vorname = None, nameKurz = None):
        self.id = id
        self.schulklassenId = schulklassenId
        self.name = name   
        self.vorname = vorname
        self.nameKurz = nameKurz  

class Tisch(object):
    """__init__() functions as the class constructor"""
    def __init__(self, uid=None, id=None, name=None):
        self.uid = uid
        self.id = id
        self.name = name         

    

userList = []

schulklassen = pd.read_csv('data/schulklassen', header=None)
schulzimmer = pd.read_csv('data/schulzimmer', header = None)
regeln = pd.read_csv('data/regeln')
#tische = pd.read_csv('data/tische', header = None)
#schueler = pd.read_csv('data/schueler', header = None)

schulklassen.columns = ['schulklassenId', 'uid','name']
schulzimmer.columns = ['schulzimmerId', 'uid','name']
#regeln.columns = ['regelId', 'uid','type','beschreibung', 'tischId','schueler1Id', 'schueler2Id']
#tische.columns = ['tischId', 'schulzimmerId','row', 'column','active','tischNumber']
#schueler.columns = ['schuelerId', 'schulklassenId','name','vorname','nameKurz']

print(schulklassen.head())
print(schulzimmer.head())
print(regeln.head())
#print(tische.head())
#print(schueler.head())
    # line_count = 0
    # for row in csv_reader:
    #     userTmp = User(row[1])
    #     userTmp.schulklassen.append
    #     schulklassenList.append(Schulklassen(row[1], row[0], row[2]))
    #     line_count += 1
    # print(f'Processed {line_count} lines.')
    # print(schulklassenList[0].toJSON())


