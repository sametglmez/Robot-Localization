import VisibilityPolygon as vis

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        return 0

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div

    # Bulduğum kesişim noktası verilen line üzerinde mi kontrol ediliyor
    if ((((line1[0][0] <= x <= line1[1][0]) or (line1[0][0] >= x >= line1[1][0]))
         and ((line1[0][1] <= y <= line1[1][1]) or (line1[0][1] >= y >= line1[1][1])))
            and (((line2[0][0] <= x <= line2[1][0]) or (line2[0][0] >= x >= line2[1][0]))
                and ((line2[0][1] <= y <= line2[1][1]) or (line2[0][1] >= y >= line2[1][1])))):

        # Bulduğum kesişim verdiğim noktalar dahil ise çıkarıyor
        if ((line1[0][0] == x and line1[0][1] == y) or (line1[1][0] == x and line1[1][1] == y)
                or (line2[0][0] == x and line2[0][1] == y) or(line2[1][0] == x and line2[1][1] == y)):
            return 0

        return 1

    return 0


def findVisibleVertex(coord,location,edges):
    flag = 0
    result = []
    for i in range(len(coord)):
        for j in range(len(edges)):
            line1  = [[edges[j][0],edges[j][1]],[edges[j][2],edges[j][3]]]
            line2 = []
            line2.append(coord[i])
            line2.append(location)

            if line_intersection(line1,line2) == 1:
                flag = 1
                break
        if(flag == 0):
            result.append(coord[i])
        else:
            flag = 0

    return result

def findUsefulPoints(randomPointsTranscation,transcation,startPoint):

    resultPoint = []
    flag = 0

    randomPoints = []
    randomPoints = randomPointsTranscation.copy()
    edgesOfPolygon = vis.findEdges(transcation)
    visibilirtyCorner = findVisibleVertex(transcation, startPoint, edgesOfPolygon)
    #print("start point : " , startPoint)
    resultPoint.append(startPoint)

    while len(randomPoints) != 0:
        distanceBetweenStartPoint = []
        for j in range(len(randomPoints)):
            distanceBetweenStartPoint.append(vis.calculateDistance(startPoint,randomPoints[j]))

        index = distanceBetweenStartPoint.index(min(distanceBetweenStartPoint))
        randomVisibilityCorner = findVisibleVertex(transcation, randomPoints[index], edgesOfPolygon)


        for k in range(len(randomVisibilityCorner)):
            if randomVisibilityCorner[k] not in visibilirtyCorner:
                flag = 1

        forIntersectionControl = []
        forIntersectionControl.append(randomPoints[index])
        forIntersectionControl.append(startPoint)


        if flag == 1:
            for t in range(len(edgesOfPolygon)):
                line1 = [[edgesOfPolygon[t][0], edgesOfPolygon[t][1]], [edgesOfPolygon[t][2], edgesOfPolygon[t][3]]]
                if line_intersection(line1,forIntersectionControl ) == 1:
                    flag = 0


        if flag == 0:
            randomPoints.pop(index)

        if flag == 1:
            for k in range(len(randomVisibilityCorner)):
                if randomVisibilityCorner[k] not in visibilirtyCorner:
                    visibilirtyCorner.append(randomVisibilityCorner[k])
            resultPoint.append(randomPoints[index])
            startPoint = randomPoints[index]
            randomPoints.pop(index)
            flag = 0


    return resultPoint


