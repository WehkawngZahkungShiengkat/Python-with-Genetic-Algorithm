# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 23:03:23 2020

@author: We-z
"""
import math 
import random
import matplotlib.pyplot as plt 
import re 

#######Start of Functions Section############Start of Functions Section#########
def pathsDistance(List):
    sumDistance = 0.0
    for x in range(len(List)-1):
        Dist = math.sqrt((List[x][0] - List[x+1][0])**2 + (List[x][1] - List[x+1][1])**2)
        sumDistance += Dist
    return sumDistance

def pathDistance(DictIn):
    List = []
    for x in DictIn:
        List.append(DictIn[x])
    sumDistance = 0.0
    for x in range(len(List)-1):
        Dist = math.sqrt((List[x][0] - List[x+1][0])**2 + (List[x][1] - List[x+1][1])**2)
        sumDistance += Dist
    return sumDistance

def GAselection(nodelist,HeadN):
    selections = []
    for x in range(5):
        ran1 = random.sample(range(1,281),280)
        #print(ran1)
        #print('x'*30)
        test1 = {HeadN:nodelist[HeadN-1]}
        for x in ran1:
            if x != HeadN:
                test1[x]=nodelist[x-1]
        selections.append(test1)
        
    #print(test3)
    temphold = []
    for x in test1:
        temphold.append(test1[x])
    #shortestP = {}
    selectionsSave = []
    for x in selections:
        distance = pathDistance(x)
        pathSave = []
        for z in x.keys():
            pathSave.append(z)
        selectionsSave.append([pathSave,distance])
    return Selecting(selectionsSave)

def Selecting(llin):
    SecondMin = llin[1]
    firstMin = llin[0]
    for c in range(1,len(llin)):
        if llin[c][1]<firstMin[1]:
            SecondMin = firstMin
            firstMin = llin[c]        
        elif llin[c][1]<SecondMin[1]:
            SecondMin = llin[c]
    return firstMin,SecondMin

def GAcrossover(Fst,Snd):
    child12 = [None]*280
    child12[0] = Fst[0]
    for d in range(50,71):
        child12[d]=Fst[d]
    
    by1 = 71
    runthrough = 71
    while None in child12:
        if Snd[runthrough] not in child12:
            if child12[by1] == None:
                child12[by1] = Snd[runthrough]
                by1 += 1
                runthrough += 1
                if by1 >= 280:
                    by1 = 0
                if runthrough >= 280:
                    runthrough = 0
            else:
                by1 += 1
        else: 
            runthrough +=1
    return child12        

def GAmutation(crIn):
    for run in range(200):
        Rno1 = random.randint(1,279)
        Rno2 = random.randint(1,279)
        temp1 = crIn[Rno1]
        temp2 = crIn[Rno2]
        crIn[Rno1] = temp2
        crIn[Rno2] = temp1
    return crIn

def ShowInGraph(BrIn):         
    # x axis values 
    x = [] 
    for nl in range(1,len(BrIn)+1):
        x.append(nl)
    # corresponding y axis values 
    y = []
    for br in BrIn:
        y.append(br[1])
    # plotting the points  
    plt.plot(x, y, color='green', linestyle='dashed', linewidth = 1, 
             marker='o', markerfacecolor='blue', markersize=5) 
      
    # setting x and y axis range 
    plt.ylim(29000,33000) 
    plt.xlim(0,len(BrIn)+1) 
      
    # naming the x axis 
    plt.xlabel('Numbers of GA records') 
    # naming the y axis 
    plt.ylabel('Total distance to travel all nodes') 
      
    # giving a title to my graph 
    plt.title('Travel with GA!') 
      
    # function to show the plot 
    plt.show()

def DisplayRecords():
    infile = open('sol_a280_5905040063.txt', 'r')
    inf = infile.read()
    RecordBestD = re.findall(r"\<.*?\<([^\<|^\>]+)\>.*?\>",inf)
    r2 =[]
    for x in RecordBestD:
        x = re.sub("\s",'',x)
        r2.append(x)
    print(r2)
    ls = re.findall(r"\s\[.+\]\s",inf)
    allRecords = {}
    totrackMin = r2[0]
    for x in range(len(r2)):
        allRecords[r2[x]] =ls[x]
        if r2[x]<totrackMin:
            totrackMin = r2[x]
    return totrackMin,allRecords

########END of Functions Section#############END of Functions Section##########
###############################################################################

##########Start of Main Section##############Start of Main Section############

# Open input file
infile = open('a280.tsp', 'r')

# Read instance header
Name = infile.readline().strip().split()[1] # NAME
FileType = infile.readline().strip().split()[1] # TYPE
Comment = infile.readline().strip().split()[1] # COMMENT
Dimension = infile.readline().strip().split()[1] # DIMENSION
EdgeWeightType = infile.readline().strip().split()[1] # EDGE_WEIGHT_TYPE
infile.readline()

# Read node list
nodelist = []
N = int(Dimension)
for i in range(0, int(Dimension)):
    x,y = infile.readline().strip().split()[1:]
    nodelist.append([float(x), float(y)])

# Close input file    
infile.close()

try:
    while True:
        StartN = int(input("please Enter start node which is a number between 1-280:"))
        if StartN <= 280 and StartN > 0:
            break
    Nloops = int(input("Please Enter a number to run the loop that number of times:"))
    First,Second = GAselection(nodelist,StartN)
    Parent1 = First
    Parent2 = Second
    Bestrecords = []
    for Runall in range(Nloops):
        Record = [Parent1,Parent2]        
        for loops in range(20):
            runtimeCount = 0
            while True:
                crover = GAcrossover(Parent1[0],Parent2[0])
                #print("Cr success")
                crover = GAmutation(crover)
                #print("Mut success")
                test2 = {}
                for x in crover:
                    test2[x]=nodelist[x-1]
                    
                Dhold = []
                for x in test2:
                    Dhold.append(test2[x])
                runtimeCount += 1
                if (pathsDistance(Dhold)<First[1]):
                    Record.append([crover,pathsDistance(Dhold)])
                    break
                elif runtimeCount == 200:
                    break
            #print(loops)
        #print("pass loop number",Runall+1)
        Best1,Best2 = Selecting(Record)
        Parent1 = Best1
        Parent2 = Best2
        Bestrecords.append(Best1)
    ShowInGraph(Bestrecords)
    with open('sol_a280_5905040063.txt', 'a') as f:
        print("The Start Node =",StartN,"\nNumber of looping =",Nloops,
              "\nThe possible shortest total distance to visit all node is <<<",
              Best1[1],">>>\n The paht direction:\n",Best1[0],"\n", file=f)
    print("The possible shortest total distance to visit all node is <<<",
          Best1[1],">>>\n The paht direction:\n",Best1[0])
    allBest,allBestDic = DisplayRecords()
    AllRec = []
    rNo = 0
    for AllR in allBestDic.keys():
        AllR = float(AllR)
        AllRec.append([rNo,AllR])
        rNo += 1
    ShowInGraph(AllRec)
    print("The shortest paths of all time records is <<<",allBest,">>>and with the path\n",
          allBestDic[allBest])
except:
    if Bestrecords != None:
        print("Error occured when running the",len(Bestrecords)-1,"times")
    else:
        print("Invalid input. Note* Please enter just a number")
    
##########End of Main Section##################End of Main Section#############
###############################################################################