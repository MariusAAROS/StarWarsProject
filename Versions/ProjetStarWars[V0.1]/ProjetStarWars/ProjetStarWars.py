import csv
from types import LambdaType

class position:
    def __init__(self,t, x, y):
        self.x = x
        self.y = y
        self.t = t

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False
def LoadData(filename:str):
    with open(filename, newline = '') as rawdata:
        rawdata = csv.reader(rawdata, dialect = 'excel')
        data = []
        for line in rawdata:
            splited = line[0].split(';')
            if all(list(map(lambda x: isfloat(x), splited))):
                conv = [float(i) for i in splited]
                data.append(position(conv[0], conv[1], conv[2]))
    return data











ficname = r"position_sample.csv"
data = LoadData(ficname)
print("fin")