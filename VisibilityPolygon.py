import matplotlib.pyplot as plt
import math
import random

from shapely.geometry import Polygon, Point


def calculateDistance(cordinateFirst, cordinateSecond):
    return math.sqrt(((cordinateFirst[0] - cordinateSecond[0]) ** 2) + ((cordinateFirst[1] - cordinateSecond[1]) ** 2))

def calculateAllDistanceForTwoFactorCombinations(twoFactorCombinationData):
    distancesTwoFactorCombinationData = []
    for twoFactorCombination in twoFactorCombinationData:
        distancesTwoFactorCombinationData.append(calculateDistance(twoFactorCombination[0], twoFactorCombination[1]))

    return distancesTwoFactorCombinationData

def isSimilarCoordinates(coordinateDistancesOne, coordinateDistancesTwo):
    for i in range(len(coordinateDistancesOne)):
        if coordinateDistancesOne[i] != coordinateDistancesTwo[i]:
            return False
    return True

def distanceBetweenPossibleAndVisibilityCoordinate(polygonCoordinateData, visibilityCoordinateData):
    visibilityCoordinateDataSize = len(visibilityCoordinateData)
    twoFactorCombinationSize = 2
    similarPolygonCoordinates = []

    possibleVisibilityCordinatesCombination = generatePossibleCoordinates(visibilityCoordinateData, twoFactorCombinationSize)
    distancesTwoFactorCombinationVisibilityData = calculateAllDistanceForTwoFactorCombinations(possibleVisibilityCordinatesCombination)

    possiblePolygonCordinatesCombination = generatePossibleCoordinates(polygonCoordinateData, visibilityCoordinateDataSize)

    for possiblePolygonCordinates in possiblePolygonCordinatesCombination:
        possiblePolygonCordinateCombination = generatePossibleCoordinates(possiblePolygonCordinates, twoFactorCombinationSize)
        distancesTwoFactorCombinationPolygonData = calculateAllDistanceForTwoFactorCombinations(possiblePolygonCordinateCombination)

        if isSimilarCoordinates(sorted(distancesTwoFactorCombinationPolygonData), sorted(distancesTwoFactorCombinationVisibilityData)):
            similarPolygonCoordinates.append(possiblePolygonCordinates)

    return similarPolygonCoordinates

def generatePossibleCoordinates(polygonCoordinateData, combinationSize):
    data = [0] * combinationSize
    start = 0
    startIndex = 0
    possibleCordinates = []

    combinationUtil(polygonCoordinateData, data, start,
                    len(polygonCoordinateData) -1, startIndex, combinationSize, possibleCordinates)

    return possibleCordinates

def combinationUtil(polygonCoordinateData, data, start,
                    last, startIndex, combinationSize, possibleCordinates):
    if (startIndex == combinationSize):
        possibleCordinates.append(data.copy())
        return

    i = start
    while (i <= last and last - i + 1 >= combinationSize - startIndex):
        data[startIndex] = polygonCoordinateData[i]
        combinationUtil(polygonCoordinateData, data, i + 1,
                        last, startIndex + 1, combinationSize, possibleCordinates)
        i += 1
def printSimilarCoordinates(similarCoordinates):
    for coordinates in similarCoordinates:
        for coordinate in coordinates:
            print(coordinate, end = ' ')
        print()

def overlay_Intersection(xs,ys,xx,yy,xxx,yyy):
    overlayCoordinate = []
    xDistance = abs(xx[0] - xxx[0])
    yDistance = abs(yy[1] - yyy[1])
    for i in range(len(xx)):

        temp = []
        resultX = xx[i] - xDistance
        resultY = yy[i] - yDistance
        temp.append(resultX)
        temp.append(resultY)
        overlayCoordinate.append(temp)

    print(overlayCoordinate)

    return overlayCoordinate

def random_points_within(poly, num_points):
    min_x, min_y, max_x, max_y = poly.bounds

    points = []

    while len(points) < num_points:
        random_point = Point([random.randint(min_x, max_x), random.randint(min_y, max_y)])
        if (random_point.within(poly)):
            points.append(random_point)

    return points

def create2DArray(polygon):
    pointsX, pointsY = zip(*polygon)
    xPoints = []
    yPoints = []
    for i in range (len(pointsX)):
        xPoints.append(pointsX[i])
        yPoints.append(pointsY[i])

    xPoints.sort()
    yPoints.sort()
    maxX = xPoints[-1]
    minX = xPoints[0]
    maxY = yPoints[-1]
    minY = yPoints[0]

    rows, cols = (maxX - minX, maxY - minY)
    arr = [[0]* (rows*2)  for _ in range(cols*2)]
    return arr

def findEdges(plygon):
    result = []
    #edgesPoints = [[0]  * 2 for _ in range(2)]
    for i in range(len(plygon) - 1):
        result.append([plygon[i][0],plygon[i][1],plygon[i+1][0],plygon[i+1][1]])

    return result