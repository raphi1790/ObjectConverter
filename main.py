import json
import pandas as pd


class JsonConvert(object):
    mappings = {}
     
    @classmethod
    def class_mapper(clsself, d):
        for keys, cls in clsself.mappings.items():
            if keys.issuperset(d.keys()):   # are all required arguments present?
                return cls(**d)
        else:
            # Raise exception instead of silently returning None
            raise ValueError('Unable to find a matching class for object: {!s}'.format(d))
     
    @classmethod
    def complex_handler(clsself, Obj):
        if hasattr(Obj, '__dict__'):
            return Obj.__dict__
        else:
            raise TypeError('Object of type %s with value of %s is not JSON serializable' % (type(Obj), repr(Obj)))
 
    @classmethod
    def register(clsself, cls):
        clsself.mappings[frozenset(tuple([attr for attr,val in cls().__dict__.items()]))] = cls
        return cls
 
    @classmethod
    def ToJSON(clsself, obj):
        return json.dumps(obj.__dict__, default=clsself.complex_handler, indent=4)
 
    @classmethod
    def FromJSON(clsself, json_str):
        return json.loads(json_str, object_hook=clsself.class_mapper)
     
    @classmethod
    def ToFile(clsself, obj, path):
        with open(path, 'w') as jfile:
            jfile.writelines([clsself.ToJSON(obj)])
        return path
 
    @classmethod
    def FromFile(clsself, filepath):
        result = None
        with open(filepath, 'r') as jfile:
            result = clsself.FromJSON(jfile.read())
        return result


@JsonConvert.register
class Schueler(object):
    """__init__() functions as the class constructor"""
    def __init__(self, id=None, name=None, vorname = None, nameKurz = None):
        self.id = id
        self.name = name   
        self.vorname = vorname
        self.nameKurz = nameKurz 
        return 

@JsonConvert.register     
class Schulklasse(object):
    """__init__() functions as the class constructor"""
    def __init__(self, id=None, uid=None, name=None, schueler:[Schueler]=None):
        self.id = id
        self.name = name
        self.schueler = [] if schueler is None else schueler
        return

@JsonConvert.register
class Position(object):
    """__init__() functions as the class constructor"""
    def __init__(self,  row = None, column = None ):
        self.row = row
        self.column = column  
        return   
@JsonConvert.register
class Tisch(object):
    """__init__() functions as the class constructor"""
    def __init__(self, id = None, position:[Position] = None , active = None, tischNumber = None):
        self.id = id
        self.position = [] if position is None else position
        self.active = active
        self.tischNumber = tischNumber  
        return   

@JsonConvert.register
class Schulzimmer(object):
    """__init__() functions as the class constructor"""
    def __init__(self,  id=None, name=None, tische:[Tisch]=None):
        self.id = id
        self.name = name 
        self.tische = [] if tische is None else tische 
        return
@JsonConvert.register
class Regel(object):
    """__init__() functions as the class constructor"""
    def __init__(self, id=None, type =None, beschreibung = None, tischId=None, schueler1Id=None, schueler2Id = None):
        self.id = id
        self.type = type   
        self.tischId = tischId   
        self.schueler1Id = schueler1Id 
        self.schueler2Id = schueler2Id   
        return    



@JsonConvert.register
class User(object):
    """__init__() functions as the class constructor"""
    def __init__(self, uid=None, id=None, schulklassen:[Schulklasse] =None,schulzimmer:[Schulzimmer] =None,regeln:[Regel] =None, ):
        self.uid = uid
        self.schulklassen = [] if schulklassen is None else schulklassen
        self.schulzimmer = [] if schulzimmer is None else schulzimmer
        self.regeln = [] if regeln is None else regeln
        return



user_list = []

schulklassen = pd.read_csv('data/schulklassen.csv',sep=";", header=0)
schulzimmer = pd.read_csv('data/schulzimmer.csv', sep=";", header = 0)
regeln = pd.read_csv('data/regeln.csv', sep=";", header = 0)
tische = pd.read_csv('data/tische.csv', sep=";", header = 0)
schueler = pd.read_csv('data/schueler.csv', sep=";", header = 0)

# print(schulklassen.uid.unique())
print(schulklassen.head())
print(schueler.head())
print(schulzimmer.head())
print(tische.head())
print(regeln.head())

# create Users
for userId in schulklassen.uid.unique():
    user_list.append(User(uid = userId))

for user in user_list:
    # Prepare Schulklassen with Schueler
    selected_classes = schulklassen.loc[schulklassen['uid'] == user.uid]
    schulklassen_list = []
    for  index, class_row in selected_classes.iterrows():
        selected_students = schueler.loc[schueler['schulklassenId'] == class_row['schulklassenId']]
        student_list = []
        for index, student_row in selected_students.iterrows():
            student_list.append(Schueler(id = student_row['schuelerId'],name=student_row['name'], vorname = student_row['vorname'], nameKurz = student_row['nameKurz']))
        schulklassen_list.append(Schulklasse(name = class_row['name'], id = class_row['schulklassenId'], schueler = student_list))
    # Prepare Schulzimmer with Tische
    selected_rooms = schulzimmer.loc[schulzimmer['uid'] == user.uid]
    schulzimmer_list = []
    for  index, room_row in selected_rooms.iterrows():
        selected_tische = tische.loc[tische['schulzimmerId'] == room_row['schulzimmerId']]
        tische_list = []
        for index, tisch_row in selected_tische.iterrows():
            tische_list.append(Tisch(id = tisch_row['tischId'],position = Position(row=tisch_row['row'], column = tisch_row['column']), active = tisch_row['active'],tischNumber = round(tisch_row['tischNumber']) ))
        schulzimmer_list.append(Schulzimmer(name = room_row['name'], id = room_row['schulzimmerId'], tische = tische_list))

    # Prepare Regeln 
    selected_rules = regeln.loc[regeln['uid'] == user.uid]
    regeln_list = []
    for index, regel_row in selected_rules.iterrows():
        regeln_list.append(Regel(id = regel_row['regelId'], type = regel_row['type'], beschreibung = regel_row['beschreibung'], tischId = regel_row['tischId'],
                    schueler1Id=regel_row['schueler1Id'], schueler2Id =regel_row['schueler2Id']))

    user.schulklassen = schulklassen_list
    user.schulzimmer = schulzimmer_list
    user.regeln = regeln_list


json_string = "{ ""users"": [ "
for user in user_list:
    json_string += "," + JsonConvert.ToJSON(user)
json_string += "] }"
# print(json_string)
text_file = open("sample.txt", "w")
n = text_file.write(json_string)
text_file.close()
# json_dictionary = json.loads(user_list[0].schulklassen.toJson() )
# print(json_dictionary)
# json_string = json.dumps([user.reprJSON() for user in user_list], cls=ComplexEncoder)
# print(json_string)
# print(json.dumps(user_list[0].reprJSON(), cls=ComplexEncoder))
# print(user_list[0].schulklassen[0])
# print(user_list[0].schulklassen[0].schueler[0])


# print(json.dumps(userList))
# print(json.dumps(userList[0]))
# schulklassen.columns = ['schulklassenId', 'uid','name']
# schulzimmer.columns = ['schulzimmerId', 'uid','name']
#regeln.columns = ['regelId', 'uid','type','beschreibung', 'tischId','schueler1Id', 'schueler2Id']
#tische.columns = ['tischId', 'schulzimmerId','row', 'column','active','tischNumber']
#schueler.columns = ['schuelerId', 'schulklassenId','name','vorname','nameKurz']

# print(schulklassen.head())
# print(schulzimmer.head())
# print(regeln.head())
# print(tische.head())
# print(schueler.head())
    # line_count = 0
    # for row in csv_reader:
    #     userTmp = User(row[1])
    #     userTmp.schulklassen.append
    #     schulklassenList.append(Schulklassen(row[1], row[0], row[2]))
    #     line_count += 1
    # print(f'Processed {line_count} lines.')
    # print(schulklassenList[0].toJSON())


