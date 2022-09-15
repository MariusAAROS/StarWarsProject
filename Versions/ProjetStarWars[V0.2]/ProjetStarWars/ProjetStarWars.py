from random import sample
from math import sin
import csv


class position:
    def __init__(self,t, x, y):
        self.x = x
        self.y = y
        self.t = t

"""
Initialisation et utilitaires
"""
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
def xval(indiv, t):
    return (indiv[0] * sin((indiv[1] * t) + indiv[2]))
def yval(indiv, t):
    return (indiv[3] * sin((indiv[4] * t) + indiv[5]))

"""
Méthodes de l'algorithme génétique
"""
class indiv():
    def __init__(self, val=None):
        if val == None:
            self.val = sample(list(range(6)), 6)
        else:
            self.val = val
        self.erreurX = 0
        self.erreurY = 0

    def fitness(self, data):
        for elem in data:
            self.erreurX += abs(elem.x - xval(self.val, elem.t))
            self.erreurY += abs(elem.y - yval(self.val, elem.t))
        return (self.erreurX + self.erreurY)
    
            

"""
Boucle Principale
"""
ficname = r"position_sample.csv"
data = LoadData(ficname)

test = indiv()
test.fitness(data)
print("fin")
