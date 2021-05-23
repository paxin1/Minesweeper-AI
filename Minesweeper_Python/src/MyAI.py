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
from AI import AI
from Action import Action


class MyAI( AI ):

        def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
                self.__totalMines = totalMines
                self.__rowDimension = colDimension
                self.__colDimension = rowDimension
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
                        #print(len(self.__UnMarkedCovered))
                        try:
                                self.__UnMarkedCovered.remove((self.__currX, self.__currY))
                        except:
                                pass
                if (len(self.__uncoveredWithoutNum) == self.__termCond):
                        #print("END ME PLEASE")
                        return Action(AI.Action(0))
                if(self.__toFlag):
                        coord = self.__toFlag[0]
                        del self.__toFlag[0]
                        self.__currX = coord[0]
                        self.__currY = coord[1]
                        return Action(AI.Action(2),coord[0],coord[1])
                if (number == -1):
                        self.__Flagged.append((self.__currX, self.__currY))
                        self.__UnMarkedCovered.remove((self.__currX, self.__currY))
                if (len(self.__Flagged) == self.__totalMines):
                        self.__toUncover = self.__UnMarkedCovered
                        #print("UNCOVER THE REST")
                        #print(len(self.__UnMarkedCovered))
                if (MyAI.Cornered(self, self.__UnMarkedCovered)):
                        #print("FML")
                        #print(self.__UnMarkedCovered)
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
                                                        if(self.__toFlag):
                                                                coord = self.__toFlag[0]
                                                                del self.__toFlag[0]
                                                                self.__currX = coord[0]
                                                                self.__currY = coord[1]
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
                if(self.__toUncover == []):
                        #print("GOING RANDO")
                        probDict = {}
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
                        toUncover = random.choice(MyAI.getUnMarkedCoveredNeighbours(self,coord[0],coord[1]))
                else:
                        toUncover = self.__toUncover[0]
                        del self.__toUncover[0]
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
                        if (coord[0] > self.__rowDimension  - 1 or coord[1] > self.__colDimension - 1):
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
                                if (coord[0] > self.__rowDimension  - 1 or coord[1] > self.__colDimension - 1):
                                        continue
                                else:
                                        nList.append(coord)
                        for coord in nList:
                                if coord in self.__uncoveredWithoutNum:
                                        rList.append(coord)
                        if (len(rList) > 0):
                                return False
                return True
                                
                        
        def adjacencyCheck(self, x, y):
                
                realList = []
                AList = [(x-1,y),(x-1,y-1),(x-1,y+1),(x,y-1),
                (x,y+1),(x+1,y-1),(x+1,y),(x+1,y+1)]
                for coord in AList:
                        if coord in self.__uncoveredWithoutNum:
                                continue
                        if (coord[0] < 0 or coord[1] < 0):
                                continue
                        if (coord[0] > self.__rowDimension  - 1 or coord[1] > self.__colDimension - 1):
                                continue
                        else:
                                realList.append(coord)
                return realList

        
