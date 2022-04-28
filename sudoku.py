import csv
import enum
from sqlite3 import OperationalError
import string
from urllib.parse import _NetlocResultMixinStr
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
plt.style.use("seaborn")

puzzlereader = []

with open('puzzle.csv', mode='r') as file:
    csvFile = csv.reader(file)
    for lines in csvFile:
        puzzlereader.append(lines)

puzzle = np.array(puzzlereader, dtype='float')
plt.figure(0)
sns.heatmap(data=puzzle,vmax = 0.5,vmin=-0.1,annot=True)
def InitPuzzle(puzzle):
    newpuzzle = np.array(puzzle)
    numseparatedpuzzle = []
    for index in range(9):
        for x,line in enumerate(newpuzzle):
            for y,num in enumerate(line):
                if num != index+1 and num != 0:
                    newpuzzle[x][y] = -1
        numseparatedpuzzle.append(newpuzzle)
        newpuzzle = np.array(puzzle)
    numseparatedpuzzle = np.array(numseparatedpuzzle)
    return numseparatedpuzzle

def SanitizePuzzle(puzzle):
    cleanseparatepuzzle = np.array(puzzle)
    for p, cpuzzle in enumerate(cleanseparatepuzzle):
        for x,line in enumerate(cpuzzle):
            for y,num in enumerate(line):
                if num > 0 and num < 1:
                    cpuzzle[x,y] = 0
    for p,cpuzzle in enumerate(cleanseparatepuzzle):
        for x,line in enumerate(cpuzzle):
            if p+1 in cpuzzle[:,x]:
                for index,num in enumerate(cpuzzle[:,x]):
                    if num == 0:
                        cpuzzle[index,x] = -1
            if p+1 in cpuzzle[x,:]:
                for index,num in enumerate(cpuzzle[x,:]):
                    if num == 0:
                        cpuzzle[x,index] = -1
        for i in range(3):
            for k in range(3):
                if p+1 in np.reshape(cpuzzle[i*3:(i+1)*3:, k*3:(k+1)*3:], 9):
                    for rowindex, row in enumerate(cpuzzle[i*3:(i+1)*3:, k*3:(k+1)*3:]):
                        for index, num in enumerate(row):
                            if num == 0:
                                cpuzzle[rowindex + i*3, index + k*3] = -1
    return cleanseparatepuzzle
def PercentPuzzle(puzzle):
    percentagepuzzle = puzzle
    for p, ppuzzle in enumerate(percentagepuzzle):
        for x,line in enumerate(ppuzzle):
            if np.any(ppuzzle[:,x] < 1)  and np.any(ppuzzle[:,x] >= 0):
                count = (1/np.count_nonzero(ppuzzle[:,x] >= 0))/3
                for index,num in enumerate(ppuzzle[:,x]):
                    if num >= 0 and num < 1:
                        ppuzzle[index,x] += count
            if np.any(ppuzzle[x,:] < 1)  and np.any(ppuzzle[x,:] >= 0):
                count = (1/np.count_nonzero(ppuzzle[x,:] >= 0))/3
                for index,num in enumerate(ppuzzle[x,:]):
                    if num >= 0 and num < 1:
                        ppuzzle[x,index] += count
        for i in range(3):
            for k in range(3):
                if np.any(np.reshape(ppuzzle[i*3:(i+1)*3:, k*3:(k+1)*3:], 9) < 1) and np.any(np.reshape(ppuzzle[i*3:(i+1)*3:, k*3:(k+1)*3:], 9) >= 0):
                    count = round((1/np.count_nonzero(np.reshape(ppuzzle[i*3:(i+1)*3:, k*3:(k+1)*3:], 9) >= 0))/3,5)
                    for rowindex, row in enumerate(ppuzzle[i*3:(i+1)*3:, k*3:(k+1)*3:]):
                        for index, num in enumerate(row):
                            if num >= 0 and num < 1:
                                ppuzzle[rowindex + i*3, index + k*3] += count
                                if ppuzzle[rowindex + i*3, index + k*3] == 1:
                                    ppuzzle[rowindex + i*3, index + k*3] = 0.9
    return percentagepuzzle
def FillInNumber(puzzle):
    numlisttype = np.dtype([('percentage',float),('xcoord',int),('ycoord',int),('puzzle',int)])
    numlist = []
    for n,fpuzzle in enumerate(puzzle):
        for x,line in enumerate(fpuzzle):
            for y,num in enumerate(line):
                if num > 0 and num < 1:
                    numlist.append([num,x,y,n])
    for index,item in enumerate(numlist):
        numlist[index] = tuple(item)
    numlist = np.array(numlist,dtype=numlisttype)   
    orderednumlist = np.sort(numlist, order='percentage')
    FilledInPuzzle = puzzle
    for p,fpuzzle in enumerate(FilledInPuzzle):
                FilledInPuzzle[p,orderednumlist[-1][1],orderednumlist[-1][2]] = -1
    FilledInPuzzle[orderednumlist[-1][3],orderednumlist[-1][1],orderednumlist[-1][2]] = orderednumlist[-1][3]+1
    print(orderednumlist[-10:])
    print("puzzle: " + str(orderednumlist[-1][3]+1) + " x-coord: " + str(orderednumlist[-1][1]) + " y-coord: " + str(orderednumlist[-1][2]))
    return FilledInPuzzle
 
def IteratePuzzle(puzzle,iter):
    IteratedPuzzle = puzzle
    for i in range(iter):
        IteratedPuzzle = FillInNumber(PercentPuzzle(SanitizePuzzle(IteratedPuzzle)))
    return IteratedPuzzle

def ConcatPuzzle(puzzle):
    newpuzzle = []
    for p,cpuzzle in puzzle:
        for x,line in cpuzzle:
            for y,num in cpuzzle:
                print('deez')
                

initedpuzzle = InitPuzzle(puzzle)
finishedpuzzle = IteratePuzzle(initedpuzzle,25)
for i in range(len(finishedpuzzle)):
    plt.figure(i+1)
    sns.heatmap(data=finishedpuzzle[i],vmax = 0.5,vmin=-0.1,annot=True)
plt.show()