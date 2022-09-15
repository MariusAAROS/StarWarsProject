import csv
from math import sin
#from random import sample
from random import uniform
from random import randint
from copy import deepcopy
from math import sqrt
import time

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
def SaveRes(res:list, iter, tpsExec):
    with open('resultat.txt', 'a') as f:
        new = "\n{0} || Generations: {1} || Execution: {2}s".format("".join(str(res)), iter, tpsExec)
        f.writelines(new)
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
            self.val = deepcopy(val)
        self.erreur = 0
    def createRandPop(count):
        return [indiv() for i in range(count)]
    def fitness(self, data):
        for elem in data:
            self.erreur += sqrt((elem.x - xval(self.val, elem.t))**2 + (elem.y - yval(self.val, elem.t))**2)
        return self.erreur
    def evaluate(pop):
        return sorted(pop, key = lambda elem: elem.erreur)
    def crossing(a, b):
        sel = randint(0,5)
        new1 = a.val[:sel] + b.val[sel:]
        new2 = b.val[:sel] + a.val[sel:]
        return [indiv(new1), indiv(new2)]
    def mutation(i):
        mut = i.val[:]
        for i in range(0, randint(0,6)):
            mut[randint(0,5)] = uniform(-100,100)
        return indiv(mut)
    def selection(pop, hcount, lcount):
        top = pop[:hcount]
        bottom = pop[len(pop) - lcount:]
        return (top + bottom)
    def __str__(self):
        return f"val: {list(map(lambda x: round(x, 4), self.val))} || erreur: {round(self.erreur, 4)}"
    def __eq__(self, elem):
        if isinstance(elem, indiv):
            return True if all(list(map(lambda x,y : round(x, 4) == round(y, 4), self.val, elem.val))) else False
        return False

debug = False

if debug == True:
    essai = [1,2,3,4,5,6]
    SaveRes(essai, 4, 5)
else:
    ficname = r"position_sample.csv"
    data = LoadData(ficname)
    pop = indiv.createRandPop(10)
    solutionFound = False
    nbIter = 0
    timeinit = time.time()
    comptStagne = 0
    indStagne = 0
    conv = False
    last = None
    while solutionFound == False:
        for i in pop:
            i.fitness(data)
        evaluation = indiv.evaluate(pop)
        if (evaluation[0].erreur) < 100 or conv == True:
        #if nbIter >= 5000:
            solutionFound = True
            res = deepcopy(evaluation[0])
        else:
            if last != None and last == evaluation[0]:
                if comptStagne == 0:
                    comptStagne += 1
                    indStagne = nbIter
                elif nbIter % 200 == 0:
                    comptStagne += 1
            else:
                comptStagne = 0
            if comptStagne >= 10:
                conv = True
            last = deepcopy(evaluation[0])
            select = indiv.selection(evaluation, 5, 1) #13,3
            cross = []
            muts = []
            for i in range(0, len(select), 2):
                cross.extend(indiv.crossing(select[i], select[i+1]))
            for i in select:
                muts.append(indiv.mutation(i))
            newchildren = indiv.createRandPop(3)
            pop = select[:] + cross[:] + muts[:] + newchildren[:]
        if nbIter%200 ==0:
            print(evaluation[0], "||",  str(nbIter))
        nbIter +=1
    execTime = time.time() - timeinit
    print(res)
    SaveRes(res, nbIter, round(execTime, 2))
print("fin")