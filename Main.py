from pathlib import Path
import numpy as np

import matplotlib.pyplot as plt
import startPoint as st
import math
import random

from matplotlib import colors
from shapely.geometry import Polygon, Point

import VisibilityPolygon as vis
import HypothesisElimination as hep


polygonCoord = []
visibilityCoord = []
transcationCoord = []
randomPointsNumber = 100

hypotesis = []
#hypotesis.append(transcation)
#hypotesis.append(transcationTempFalse1)
#hypotesis.append(transcationTempFalse2)

def createPolygonWithSimilarCoordinates(similarCoordinates):
    #xs, ys = zip(*coord)  # Polygon of x and y values
    xx, yy = zip(*similarCoordinates[0])
    xxx, yyy = zip(*similarCoordinates[1])

    #plt.figure()
    #plt.plot(xs, ys)
    #plt.plot(xx, yy, 'ro')
    #plt.plot(xxx, yyy, 'ro', color="orange")

def createRandomPoints(transcationParameter):

    poly = Polygon(transcationParameter)
    points = vis.random_points_within(poly, randomPointsNumber)

    pointResult = []
    for p in points:
        tempArr = []
        tempArr.append(p.x)
        tempArr.append(p.y)
        pointResult.append(tempArr)

    return pointResult

def convertPolygonTo2dList():
    1
    #flag = vis.create2DArray(coord)
    #leng = len(flag)
    #leng1 = len(flag[0])
    #print(leng, " ---   ---- ", leng1)
    #for i in range(len(coord)):
        #flag[len(flag) - coord[i][1] - 1][coord[i][0]] = '7'

   # return flag

def compareTwoZoneVisibilityWithDistance(baseZoneVisibleVertex, targetZoneVisibleVertex,xDistance, yDistance):
    if len(baseZoneVisibleVertex) != len(targetZoneVisibleVertex):
        return False

    for visibleVertex in targetZoneVisibleVertex:
        visibleVertexWithDistance = visibleVertex
        visibleVertexWithDistance[0] += xDistance
        visibleVertexWithDistance[1] += yDistance

        if visibleVertexWithDistance not in baseZoneVisibleVertex:
            return False


    return  True



def fillDataSet(datasetNumber):
    datasetPath = "C:\\Users\\samet\\Desktop\\BitirmeDataSet\\dataset" + str(datasetNumber) + "\\dataset.txt"
    datasetFile = open(datasetPath, 'r')
    while True:
        line = datasetFile.readline()
        lineData = line.split()  # split string into a list
        datas = []
        for data in lineData:
            datas.append(int(data))
        if not line:
            break
        polygonCoord.append(datas.copy())
    datasetFile.close()

    datasetPath = "C:\\Users\\samet\\Desktop\\BitirmeDataSet\\dataset" + str(datasetNumber) + "\\visibility.txt"
    datasetFile = open(datasetPath, 'r')
    while True:
        line = datasetFile.readline()
        lineData = line.split()  # split string into a list
        datas = []
        for data in lineData:
            datas.append(int(data))
        if not line:
            break
        visibilityCoord.append(datas.copy())
    datasetFile.close()


    i = 1

    transName = "transcation"
    datasetPath = "C:\\Users\\samet\\Desktop\\BitirmeDataSet\\dataset" + str(datasetNumber) + "\\"
    while(True):
        transcationList = []
        datasetPath = datasetPath + transName + str(i) + ".txt"
        if Path(datasetPath).is_file() :
            datasetFile = open(datasetPath, 'r')
            while True:
                line = datasetFile.readline()
                lineData = line.split()  # split string into a list
                datas = []
                for data in lineData:
                    datas.append(int(data))
                if not line:
                    break
                transcationList.append(datas.copy())
            #print(transcationList)
            transcationCoord.append(transcationList)
            datasetFile.close()
        else:
            break
        i += 1
        datasetPath = "C:\\Users\\samet\\Desktop\\BitirmeDataSet\\dataset" + str(datasetNumber) + "\\"



def drawSimilarCoordinate(similarCoordinates):
    jet = plt.get_cmap('jet')
    colors = iter(jet(np.linspace(0, 5, 10)))
    polygonX, polygonY = zip(*polygonCoord)

    #plt.figure()
    #plt.plot(polygonX, polygonY )
    for i in range(len(similarCoordinates)):
        x,y = zip(*similarCoordinates[i])

        #plt.plot(x, y,'ro')

    #plt.show()

def checkForElimination(usefulPoints,baseZone,targetZone):
    xDistance = baseZone[0][0] - targetZone[0][0]
    yDistance = baseZone[0][1] - targetZone[0][1]

    baseZoneEdges = vis.findEdges(baseZone)
    targetZoneEdges = vis.findEdges(targetZone)

    for usefulPoint in usefulPoints:
        baseZoneVisibleVertex = hep.findVisibleVertex(baseZone,usefulPoint,baseZoneEdges)
        usefulPointForTarget = usefulPoint.copy()
        usefulPointForTarget[0] += xDistance
        usefulPointForTarget[1] += yDistance
        targetZoneVisibleVertex = hep.findVisibleVertex(targetZone, usefulPointForTarget, targetZoneEdges)
        if compareTwoZoneVisibilityWithDistance(baseZoneVisibleVertex, targetZoneVisibleVertex, xDistance, yDistance) == False:
            return False

    return True

def eliminateHypotesis(startPoints):
    # todo intersection for hypotesis ? maybe should be outside of while
    usefulPointsTemp = []
    while len(hypotesis) != 1:
        for i in range(0, len(hypotesis)):
            #print("hypotesis[i]:", hypotesis[i])

            randomPointsTranscation = createRandomPoints(hypotesis[i])
            #randomPointsTranscation = createRandomPoints(polygonCoord)
            edgesOfPolygon = vis.findEdges(polygonCoord)
            usefulPointsTemp = hep.findUsefulPoints(randomPointsTranscation, hypotesis[i], startPoints[i])
            #usefulPointsTemp = hep.findUsefulPoints(randomPointsTranscation,polygonCoord, startPoints[i])

            if checkForElimination(usefulPointsTemp, hypotesis[i], hypotesis[i+1]) == False:
                #print("removed hypotes index :", i+1)
                #print("removed hypotes :", hypotesis[i+1])
                hypotesis.pop(i+1)
                break
    #print("result of hypotesis size :", len(hypotesis))
    #print("result of hypotesis :", hypotesis)

    return usefulPointsTemp


def wanderPolygon(startPoint):
    randomPointsTranscation = createRandomPoints(polygonCoord)
    usefulPointsTemp = hep.findUsefulPoints(randomPointsTranscation, polygonCoord, startPoint)

    sametX, sametY = zip(*usefulPointsTemp);
    polygonX, polygonY = zip(*polygonCoord)
    plt.figure()
    plt.plot(polygonX, polygonY);
    plt.plot(sametX, sametY);

    return usefulPointsTemp

def compareResultDistance(result1,result2):
    distance1 = []
    distance2 = []
    sumDistanceElimination = 0;
    sumDistancePolygon = 0;
    for i in range(len(result1)-1):
        sumDistanceElimination += vis.calculateDistance(result1[i],result1[i+1])

    for i in range(len(result2)-1):
        sumDistancePolygon += vis.calculateDistance(result2[i], result2[i + 1])


    return sumDistanceElimination,sumDistancePolygon

def main1(number):
    fillDataSet(number)
    polygonCoord.append(polygonCoord[0])
    similarCoordinates = vis.distanceBetweenPossibleAndVisibilityCoordinate(polygonCoord, visibilityCoord)
    #vis.printSimilarCoordinates(similarCoordinates)

    #--------Polygonların sonu ile başını bağlama--------------------
    polygonCoord.append(polygonCoord[0])
    visibilityCoord.append(visibilityCoord[0])
    #---------Polygon görünebilir alanları gösterme -------------
    #drawSimilarCoordinate(similarCoordinates)

    for i in range(len(transcationCoord)):
        transcationCoord[i].append(transcationCoord[i][0])
        hypotesis.append(transcationCoord[i])

    startPoint1 = [121,285]
    startPoint2 = [181,285]
    startPoint3 = [241,205]
    startPoint4 = [294,205]

    startPoints = []
    """startPoints.append(startPoint1)
    startPoints.append(startPoint2)
    startPoints.append(startPoint3)
    startPoints.append(startPoint4)"""


    for i in range(len(st.startPointsMain[number-1])):
        #for j in range(len(st.startPointsMain[number-1][i])):
        #print("sstart point : " , st.startPointsMain[number-1][i])
        startPoints.append(st.startPointsMain[number-1][i])



    """startPoints.append(startPointsMain[number-1])
    startPoints.append(startPoint2)
    startPoints.append(startPoint3)"""
    #startPoints.append(startPoint4)

    polygonX, polygonY = zip(*polygonCoord)
    plt.figure()
    plt.plot(polygonX, polygonY)
    print(startPoints)
    counter = 0
    while(True):
        counter += 1
        resultPoints = eliminateHypotesis(startPoints)
        if len(resultPoints) > 1:
            resultX, resultY = zip(*resultPoints)
            plt.plot(resultX, resultY)
            break
        if (counter == 10):
            resultPoints = wanderPolygon(startPoints[0])
            break




    #----------------------- Bütün alanı dolaşma ---------------------------
    result2 = wanderPolygon(startPoints[0])

    distanceElimination, distancePolygon =  compareResultDistance(resultPoints,result2)

    print("Heuristic Algorithm : " , distanceElimination , "\nBute Force Algorithm : " , distancePolygon, "\n" )

    plt.show()

    return distanceElimination


def drawPolygon(num):
    fillDataSet(num)
    polygonX, polygonY = zip(*polygonCoord)
    plt.figure()
    plt.plot(polygonX, polygonY)
    #plt.show()

def test():
    #main1()
    #drawPolygon(1)
    #main1(1)
    distance = 0
    distanceOrtalama = []
    for j in range(3):
        for i in range(25):
            if i == 6 or i == 12 or i == 24 :
                continue
            print(i+1,end ="    ")
            #main1(i+1)
            distance = distance + main1(i+1)
            polygonCoord.clear()
            visibilityCoord.clear()
            transcationCoord.clear()
            hypotesis.clear()
            print(distance)
        print("\n\n----------------------------------\n\n")
        if j == 0:
            randomPointsNumber =  500
        if j == 1:
            randomPointsNumber = 1000

        distanceOrtalama.append(float(distance/24))
        print("--------> ", float(distance/24))
        distance = 0
        ##main1(3)

    print(distanceOrtalama)

if __name__ == '__main__':
    while(True):
        number = int(input("Enter Polygon Number : "))
        if number == -1:
            break

        main1(number)
        polygonCoord.clear()
        visibilityCoord.clear()
        transcationCoord.clear()
        hypotesis.clear()

    #drawPolygon()