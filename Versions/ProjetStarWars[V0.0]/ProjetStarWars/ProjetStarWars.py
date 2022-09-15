import csv;

def LoadData(filename:str):
    with open(filename, newline = '') as rawdata:
        rawdata = csv.reader(rawdata, dialect = 'excel')
        data = []
        for line in rawdata:
            data.append(line)
    data.pop(0)
    return data


ficname = r"position_sample.csv"
data = LoadData(ficname)
print("fin")