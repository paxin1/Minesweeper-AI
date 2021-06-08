# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================
import random
import time
from AI import AI
from Action import Action


class MyAI( AI ):

        def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
                self.__totalMines = totalMines
                self.__rowDimension = rowDimension
                self.__colDimension = colDimension
                self.__currX = startX
                self.__currY = startY
                self.__uncoveredWithNum = {0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[]}
                self.__uncoveredWithoutNum = []
                self.__checked = []
                self.__toUncover = []
                self.__Flagged = []
                self.__toFlag = []
                self.__termCond = (rowDimension*colDimension) - totalMines
                self.__UnMarkedCovered = []
                for x in range(0,colDimension):
                        for y in range(0,rowDimension):
                                self.__UnMarkedCovered.append((x,y))
                
        def getAction(self, number: int) -> "Action Object":
                if (number != -1):
                        self.__uncoveredWithNum[number].append((self.__currX, self.__currY))
                        self.__uncoveredWithoutNum.append((self.__currX, self.__currY))
                        try:
                                if (self.__currX, self.__currY) in self.__UnMarkedCovered:
                                    self.__UnMarkedCovered.remove((self.__currX, self.__currY))
                        except:
                                pass
                if (len(self.__uncoveredWithoutNum) == self.__termCond):
                        return Action(AI.Action(0))
                self.__toFlag = list(set(self.__toFlag) - set(self.__Flagged))
                if(self.__toFlag):
                        coord = self.__toFlag[0]
                        del self.__toFlag[0]
                        self.__currX = coord[0]
                        self.__currY = coord[1]
                        return Action(AI.Action(2),coord[0],coord[1])
                if (number == -1):
                        if (self.__currX, self.__currY) not in self.__Flagged:
                                self.__Flagged.append((self.__currX, self.__currY))
                        if (self.__currX, self.__currY) in self.__UnMarkedCovered:
                                self.__UnMarkedCovered.remove((self.__currX, self.__currY))
                if (len(self.__Flagged) == self.__totalMines):
                        self.__toUncover = self.__UnMarkedCovered
                if (MyAI.Cornered(self, self.__UnMarkedCovered)):
                        random.shuffle(self.__UnMarkedCovered)
                        self.__toUncover = self.__UnMarkedCovered
                if self.__toUncover == []:
                        run = True
                        for num, coordList in self.__uncoveredWithNum.items():
                                if num == 0:
                                        for u_coord in coordList:
                                                if u_coord in self.__checked:
                                                        continue
                                                else:
                                                        self.__checked.append(u_coord)
                                                        self.__toUncover = MyAI.adjacencyCheck(self,u_coord[0],u_coord[1])
                                                        if (self.__toUncover == []):
                                                                continue
                                                        else:
                                                                run = False
                                                                break
                                        if (run == False):
                                                break
                                if num > 0:
                                        for u_coord in coordList:
                                                adjacencyList = MyAI.adjacencyCheck(self,u_coord[0],u_coord[1])
                                                if (len(adjacencyList) == num):
                                                        for coord in adjacencyList:
                                                                if coord in self.__Flagged:
                                                                        continue
                                                                else:
                                                                        self.__toFlag.append(coord)
                                                        self.__toFlag = list(set(self.__toFlag) - set(self.__Flagged))
                                                        if(self.__toFlag):
                                                                #print(self.__toFlag)
                                                                coord = self.__toFlag[0]
                                                                del self.__toFlag[0]
                                                                self.__currX = coord[0]
                                                                self.__currY = coord[1]
                                                                #print("FLAGGING in lower statement")
                                                                return Action(AI.Action(2),coord[0],coord[1])
                                                if (len(adjacencyList) > num):
                                                        fList = []
                                                        uList = []
                                                        for coord in adjacencyList:
                                                                if coord in self.__Flagged:
                                                                        fList.append(coord)
                                                                else:
                                                                        uList.append(coord)
                                                        if (len(fList) == num):
                                                                self.__toUncover = uList
                                                                break

                #print("BOTTOM: ",self.__toUncover)
                if(self.__toUncover == []):
                        #print("GOING RANDO")
                        fDict = MyAI.genFrontier(self)
                        #print(fDict)
                        currCFrontier = min(fDict.items(), key=lambda x: len(x[1][1]))[1][1]
                        currUFrontier = min(fDict.items(), key=lambda x: len(x[1][1]))[1][0]
                        #print("CURR C FRONTIER: ",currCFrontier)
                        #print("CURR U FRONTIER: ",currUFrontier)
                        #Creates permutations of zeros and ones of size n where one is a bomb and zero is safe
                        removedUCoords = set()
                        for uCoord in currUFrontier.keys():
                                nSet = set(MyAI.getUnMarkedCoveredNeighbours(self, uCoord[0], uCoord[1]))
                                cSet = set(currCFrontier)
                                aSet = set(MyAI.soleCheck(self,uCoord[0],uCoord[1],currCFrontier,[]))
                                if (aSet != nSet):
                                        removedUCoords.add(uCoord)
                        if len(currCFrontier) > 15:
                                currCFrontier = currCFrontier[0:15]
                                for uCoord in currUFrontier.keys():
                                        nSet = set(MyAI.getUnMarkedCoveredNeighbours(self, uCoord[0], uCoord[1]))
                                        cSet = set(currCFrontier)
                                        aSet = set(MyAI.soleCheck(self,uCoord[0],uCoord[1],currCFrontier,[]))
                                        if (aSet != nSet):
                                                removedUCoords.add(uCoord)
                                        if (len(nSet.intersection(cSet)) == 0):
                                                removedUCoords.add(uCoord)
                                #print(currUFrontier)
                        for removedUCoord in list(removedUCoords):
                                del currUFrontier[removedUCoord]
                        permList = MyAI.recursePerm(self,[[0],[1]],len(currCFrontier))
                        #print('CURRCFRONTIER', currCFrontier)
                        #print('CURRUFRONTIER', currUFrontier)
                        LegalList = []
                        #Assigns coordinates a value of one or zero in a dictionary and valid combinations are added to the LegalList
                        #Invalid permutations are permutations where there are more ones than flags remaining
                                #and the effective label of any of the uncoveredFrontier nodes are not zero
                        #Checking for validity should be done as we loop through the permutations
                        for p in permList:
                                minesLeft = self.__totalMines - len(self.__Flagged)
                                if (p.count(1) > minesLeft):
                                        continue
                                cond = True
                                run = True
                                tempDict = {}
                                labelCon = []
                                for index, num in enumerate(p):
                                     tempDict[currCFrontier[index]] = num
                                for coord, label in currUFrontier.items():
                                        labelC = label
                                        aList = MyAI.soleCheck(self,coord[0],coord[1],currCFrontier,[])
                                        for c in aList:
                                                if tempDict[c] == 1:
                                                        labelC -= 1
                                        labelCon.append(labelC)
                                if labelCon.count(0) == len(labelCon):
                                        LegalList.append(tempDict)       
                                #print(tempDict)
                        #print(LegalList)
                        finalDict = {}
                        for d in LegalList:
                                for coord, state in d.items():
                                        if coord not in finalDict.keys():
                                                finalDict[coord] = 0
                                        finalDict[coord] += state
                        #print('FINALDICT', finalDict)
                        choices = []
                        minState = min(finalDict.values())
                        for k, v in finalDict.items():
                                if (v == minState):
                                        choices.append(k)
                        #print('CHOICES', choices)
                        self.__toUncover.append(random.choice(choices))
                        '''probDict = {}
                        probList = []
                        #Calculate probability of safely uncovering a tile by calculating a coordinate's effective label and dividing it by total number of unmarked and covered neighbours
                        #probability = (label - numMarkedNeighbours)/numUnmarkedCoveredNeighbours
                        for label, coordList in self.__uncoveredWithNum.items():
                                for coord in coordList:
                                        #print("COORDINATE: ",coord)
                                        if (len(MyAI.getUnMarkedCoveredNeighbours(self,coord[0],coord[1])) == 0):
                                            pass
                                        else:
                                                #print("WE HERE BOIS")
                                                prob = 1 - (label - len(MyAI.getFlaggedNeighbours(self,coord[0],coord[1])))/len(MyAI.getUnMarkedCoveredNeighbours(self,coord[0],coord[1]))
                                                if prob not in probDict:
                                                        probDict[prob] = [coord]
                                                        probList.append(prob)
                                                else:
                                                        probDict[prob].append(coord)
                                                

                        maxKey = max(probList)
                        coord = probDict[maxKey][0]
                        del probDict[maxKey][0]
                        toUncover = random.choice(MyAI.getUnMarkedCoveredNeighbours(self,coord[0],coord[1]))'''
                #else:
                #print('TO UNCOVER', self.__toUncover)
                toUncover = self.__toUncover[0]
                del self.__toUncover[0]
                #print("UNCOVERING: ",toUncover)
                self.__currX = toUncover[0]
                self.__currY = toUncover[1]
                return Action(AI.Action(1),toUncover[0],toUncover[1])


        def getFlaggedNeighbours(self, x, y):
                fList = []
                AList = [(x-1,y),(x-1,y-1),(x-1,y+1),(x,y-1),
                (x,y+1),(x+1,y-1),(x+1,y),(x+1,y+1)]
                for coord in AList:
                        if coord in self.__Flagged:
                                fList.append(coord)
                return fList
        def getUnMarkedCoveredNeighbours(self, x, y):
                fList = []
                AList = [(x-1,y),(x-1,y-1),(x-1,y+1),(x,y-1),
                (x,y+1),(x+1,y-1),(x+1,y),(x+1,y+1)]
                for coord in AList:
                        if coord in self.__uncoveredWithoutNum:
                                continue
                        if coord in self.__Flagged:
                                continue
                        if (coord[0] < 0 or coord[1] < 0):
                                continue
                        if (coord[0] > self.__colDimension  - 1 or coord[1] > self.__rowDimension - 1):
                                continue
                        else:
                                fList.append(coord)
                return fList

        def Cornered(self,cList):
                #If all neighbours are covered or flagged
                for coord in cList:
                        x = coord[0]
                        y = coord[1]
                        nList = []
                        rList = []
                        AList = [(x-1,y),(x-1,y-1),(x-1,y+1),(x,y-1),
                        (x,y+1),(x+1,y-1),(x+1,y),(x+1,y+1)]
                        for coord in AList:
                                if (coord[0] < 0 or coord[1] < 0):
                                        continue
                                if (coord[0] > self.__colDimension  - 1 or coord[1] > self.__rowDimension - 1):
                                        continue
                                else:
                                        nList.append(coord)
                        for coord in nList:
                                if coord in self.__uncoveredWithoutNum:
                                        rList.append(coord)
                        if (len(rList) > 0):
                                return False
                return True

        def genFrontier(self):
            coveredFrontier = set()
            uncoveredFrontier = set()
            for coord in self.__uncoveredWithoutNum:
                aList = MyAI.adjacencyCheck(self,coord[0],coord[1])
                aList = list(set(aList)-set(self.__Flagged))
                if len(aList) > 0:
                    uncoveredFrontier.add(coord)
                    for c in aList:
                        coveredFrontier.add(c)
            coveredFrontier = list(coveredFrontier)
            #coveredFrontier.sort()
            uncoveredFrontier = list(uncoveredFrontier)
            #uncoveredFrontier.sort()
            checked = []
            fDict = {}
            counter = 0
            size = len(coveredFrontier)
            while (len(set(checked)) < size):
                    chain = []
                    startCoord = coveredFrontier[0]
                    chain.append(startCoord)
                    del coveredFrontier[0]
                    aList = MyAI.soleCheck(self, startCoord[0], startCoord[1],coveredFrontier, checked)
                    checked.append(startCoord)
                    while(aList != []):
                        for c in aList:
                            chain.append(c)
                        for c in chain:
                            if c not in checked:
                                aList = MyAI.soleCheck(self, c[0], c[1], coveredFrontier, checked)
                                for coord in aList:
                                        chain.append(coord)
                                checked.append(c)
                                num = coveredFrontier.index(c)
                                del coveredFrontier[num]
                    chain = list(set(chain))
                    chain.sort()
                    #print("COVERED: ", chain)
                    uChain = set()
                    for i in chain:
                            aList = MyAI.soleCheck(self, i[0], i[1],uncoveredFrontier,[])
                            for x in aList:
                                    uChain.add(x)
                    uChain = list(uChain)
                    uChainDict = {}
                    #print("UNCOVERED: ",uChain)
                    for coord in uChain:
                            for label, l in self.__uncoveredWithNum.items():
                                    if coord in l:
                                            uChainDict[coord] = label - len(MyAI.getFlaggedNeighbours(self,coord[0],coord[1]))
                    counter += 1
                    fDict[counter] = (uChainDict, chain)
            
            return fDict
                

        def getCoveredNeighbours(self, x, y):
                realList = []
                AList = [(x-1,y),(x-1,y-1),(x-1,y+1),(x,y-1),
                (x,y+1),(x+1,y-1),(x+1,y),(x+1,y+1)]
                for coord in AList:
                        if coord in self.__Flagged:
                                continue
                        if (coord[0] < 0 or coord[1] < 0):
                                continue
                        if (coord[0] > self.__colDimension  - 1 or coord[1] > self.__rowDimension - 1):
                                continue
                        else:
                                realList.append(coord)
                return realList

        def soleCheck(self, x, y, eList, cList):
                #adjacancy check where all its elements are in eList and none of its elements are from cList
                realList = []
                AList = [(x-1,y),(x-1,y-1),(x-1,y+1),(x,y-1),
                (x,y+1),(x+1,y-1),(x+1,y),(x+1,y+1)]
                for coord in AList:
                        if coord not in eList:
                                continue
                        if coord in cList:
                                continue
                        else:
                            realList.append(coord)
                return realList
                        
        def adjacencyCheck(self, x, y):
                #print("CHECK FOR ",(x,y))
                realList = []
                AList = [(x-1,y),(x-1,y-1),(x-1,y+1),(x,y-1),
                (x,y+1),(x+1,y-1),(x+1,y),(x+1,y+1)]
                for coord in AList:
                        if coord in self.__uncoveredWithoutNum:
                                continue
                        if (coord[0] < 0 or coord[1] < 0):
                                continue
                        if (coord[0] > self.__colDimension  - 1 or coord[1] > self.__rowDimension - 1):
                                continue
                        else:
                                realList.append(coord)
                return realList

        def recursePerm(self, setList, numPerm):
            tempList = []
            if len(setList[0]) == numPerm:
                return setList
            for elem in setList:
                tempList.append([0]+elem)
                tempList.append([1]+elem)
            return MyAI.recursePerm(self, tempList,numPerm)
        



