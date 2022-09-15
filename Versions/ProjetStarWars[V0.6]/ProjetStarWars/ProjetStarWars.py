import csv
from math import sin
#from random import sample
from random import uniform
from random import randint
from copy import deepcopy

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
def xval(indiv, t):
    return (indiv[0] * sin((indiv[1] * t) + indiv[2]))
def yval(indiv, t):
    return (indiv[3] * sin((indiv[4] * t) + indiv[5]))

class indiv():
    def __init__(self, val=None):
        if val == None:
            self.val = [uniform(-100, 100) for i in range(6)]
            #self.val = sample(list(range(0,6)), 6)
        else:
            self.val = val
        self.erreurX = 0
        self.erreurY = 0
    def createRandPop(count):
        return [indiv() for i in range(count)]
    def fitness(self, data):
        for elem in data:
            self.erreurX += abs(elem.x - xval(self.val, elem.t))
            self.erreurY += abs(elem.y - yval(self.val, elem.t))
        return (self.erreurX + self.erreurY)
    def evaluate(pop):
        return sorted(pop, key = lambda elem: (elem.erreurX + elem.erreurY))
    def crossing(a, b):
        new1 = a.val[:3] + b.val[3:]
        new2 = b.val[:3] + a.val[3:]
        return [new1, new2]
    def mutation(i):
        mut = i.val[:]
        mut[randint(0,5)] = uniform(-100,100)
        return indiv(mut)
    def selection(pop, hcount, lcount):
        top = pop[:hcount]
        bottom = pop[len(pop) - lcount:]
        return (top + bottom)
    def __str__(self):
        return f"val: {self.val} || erreurX: {self.erreurX}, erreurY: {self.erreurY}"



ficname = r"position_sample.csv"
data = LoadData(ficname)
pop = indiv.createRandPop(25)
solutionFound = False
nbIter = 0
while solutionFound == False:
    for i in pop:
        i.fitness(data)
    evaluation = indiv.evaluate(pop)
    #if (evaluation[0].erreurX + evaluation[0].erreurY) < 100:
    if nbIter >= 5000:
        solutionFound = True
        res = deepcopy(evaluation[0])
    else:
        select = indiv.selection(pop, 10, 4) 
        cross = []
        muts = []
        for i in range(len(select), 2):
            cross.extend(indiv.crossing(select[i], select[i+1]))
        for i in select:
            muts.append(indiv.mutation(i))
        newchildren = indiv.createRandPop(5)
        pop = select[:] + cross[:] + muts[:] + newchildren[:]
    nbIter +=1

print(res)
print("fin")