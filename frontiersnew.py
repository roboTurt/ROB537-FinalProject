from matplotlib.image import NonUniformImage
import numpy as np 
import random 
import pdb
import gym_Explore2D

class FrontierPointFinder:
     
    def __init__(self, frontierMap, visited_list):
         
        self.frontierMap = frontierMap
        self.frontierMapShape = frontierMap.shape   
        self.frontierCoords = []
        self.hiddenCoords = []
        self.agentPosition = np.where(self.frontierMap == 2) 
        self.freeCoords = []
        self.tragetFrontier = []
        self.visited = visited_list

    def findFrontierCoordsDijsktra(self):
        # the frontier points are on the boundary of the explored map
        # [[3 3 3 3]
        # [1 4 3 3 ]
        # [2 0 4 3]
        # [1 0 4 3]
        # [3 4 3 3]]
        # 1 - obstacle space
        # 2 - current location
        # 4 - frontier to explore
        # 3 - hidden unknown
        # 0 - open space
        
        # appending the 0,1 to the dijsktra map
        list_coordinate0 = np.where(self.frontierMap == 0)
        list_coordinate = np.where(self.frontierMap == 1)
        self.dijsktraMap = []
        for i in range(len(list_coordinate[0])):
            self.dijsktraMap.append((list_coordinate[0][i], list_coordinate[1][i]))
        for i in range(len(list_coordinate0[0])):
            self.dijsktraMap.append((list_coordinate0[0][i], list_coordinate0[1][i]))
        
        # generate 4 on the map
        agentPosition = np.where(self.frontierMap == 2)
        agentCoord = np.array([agentPosition[0][0],agentPosition[1][0]])
        rowID = agentCoord[0]
        columnID = agentCoord[1]
        newmap = np.copy(self.frontierMap)
        if (columnID >= 2):
            if rowID - 1 >= 0:
                newmap[rowID-1][columnID-2] = 4
            newmap[rowID][columnID-2] = 4
            if rowID + 1 < newmap.shape[0]:
                newmap[rowID+1][columnID-2] = 4

        if (columnID < newmap.shape[1]-2):
            if rowID - 1 >= 0:
                newmap[rowID-1][columnID+2] = 4
            newmap[rowID][columnID+2] = 4
            if rowID + 1 < newmap.shape[0]:
                newmap[rowID+1][columnID+2] = 4
        
        if (rowID - 2 >= 0):
            if columnID - 1 >= 0:
                newmap[rowID-2][columnID-1] = 4
            newmap[rowID-2][columnID] = 4
            if columnID + 1 < newmap.shape[0]:
                newmap[rowID-2][columnID+1] = 4

        if (rowID < newmap.shape[0]-2):
            if columnID - 1 >= 0:
                newmap[rowID+2][columnID-1] = 4
            newmap[rowID+2][columnID] = 4
            if columnID + 1 < newmap.shape[0]:
                newmap[rowID+2][columnID+1] = 4
        print(newmap, "newmap")

        # appending 4 to the map and the frontierlist
        list_coordinate2 = np.where(newmap == 4)
        self.dijsktraMap.append((agentPosition[0][0],agentPosition[1][0]))
        for i in range(len(list_coordinate2[0])):
            self.dijsktraMap.append((list_coordinate2[0][i], list_coordinate2[1][i]))
            self.frontierCoords.append((list_coordinate2[0][i], list_coordinate2[1][i]))
        for pts in self.frontierCoords:
            if pts in self.visited:
                self.frontierCoords.remove(pts)
        
        
    def findFrontierCoords(self):
        # the point with the minimum distance from the current location
        self.findFrontierCoordsDijsktra()
        mindist = 1000
        for pts in self.frontierCoords:
            dist = np.sqrt(np.power(self.agentPosition[0] - pts[0], 2) + np.power(self.agentPosition[1] - pts[1], 2))
            if dist <= mindist:
                mindist = dist
                self.tragetFrontier = pts
        return self.tragetFrontier, self.dijsktraMap

    def returnTargetFrontierPoint(self):
        return self.findFrontierCoords()
