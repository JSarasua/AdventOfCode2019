import statistics
from collections import Counter
import numpy

#For all days
def print_count(countValue):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Total Count: {countValue}')  # Press Ctrl+F8 to toggle the breakpoint.

def split(word):
    return [char for char in word]

def splitInt(word):
    return [int(char) for char in word]

def strArrayToIntArray(strArray):
    intArray = [int(numString) for numString in strArray]
    return intArray

def IsValidIndex( listToCheck:list, index):
    if 0 <= index < len(listToCheck):
        return True
    return False

def IsValidCoordinate( listToCheck, rowIndex, colIndex):
    if IsValidIndex(listToCheck, rowIndex):
        if IsValidIndex(listToCheck[rowIndex], colIndex):
            return True
    return False

def IsValidCoordinateTuple( listToCheck, xyTuple:tuple):
    return IsValidCoordinate(listToCheck, xyTuple[1], xyTuple[0])

def GetValAtCoordinate( list:list, xy:tuple):
    return list[xy[1]][xy[0]]

def SetValAtCoordinate( list:list, xy:tuple, val):
    list[xy[1]][xy[0]] = val
    return

def GetCharacterCount(char, wordList):
    charCount = 0
    for word in wordList:
        count = Counter(word)
        if count[char] > 0:
            charCount += 1
    return charCount

def Make2DDataArray(fileData):
    dataArray = []
    for fileLine in fileData:
        dataArray.append(splitInt(fileLine.strip()))

    return dataArray

def AddCountToDict(dict:dict, key, count):
    if key in dict.keys():
        dict[key] += count
    else:
        dict[key] = count

def MakeListInitialVal(length, initialVal):
    list = [initialVal] * length
    return list

def Make2DList(rowLen, colLen, initialVal):
    list = []
    for colIndex in range(0, colLen):
        list.append(MakeListInitialVal(rowLen, initialVal))

    return list

def AddXY(a,b):
    c = (a[0] + b[0], a[1] + b[1])
    return c

def ListToString(list:list):
    return ''.join(map(str,list))

#For current day
def GetDecimalNumber(binaryList:str, startingIndex, count):
    return int(binaryList[startingIndex:startingIndex+count],2)

def GetPacketVersion(binaryList:str, startingIndex):
    packetVersion = GetDecimalNumber(binaryList, startingIndex, 3)
    return packetVersion, startingIndex + 3

def GetPacketTypeID(binaryList:str, startingIndex):
    packetTypeID = GetDecimalNumber(binaryList, startingIndex, 3)
    return packetTypeID, startingIndex + 3

def GetLiteralValue(binaryList:str, startingIndex):
    currentBinaryString = ''
    while binaryList[startingIndex] == '1':
        startingIndex += 1
        currentBinaryString += binaryList[startingIndex:startingIndex+4]
        startingIndex += 4

    startingIndex += 1
    currentBinaryString += binaryList[startingIndex:startingIndex + 4]
    startingIndex += 4
    return GetDecimalNumber(currentBinaryString, 0, len(currentBinaryString)), startingIndex

def GetLengthTypeID(binaryList:str, startingIndex):
    lengthTypeID = GetDecimalNumber(binaryList, startingIndex, 1)
    return lengthTypeID, startingIndex + 1

def CalculateIntCode(dataArray, val1, val2):
    intDataArray = dataArray.copy()
    intDataArray[1] = val1
    intDataArray[2] = val2
    currentIndex = 0
    while currentIndex < len(intDataArray)-4 and intDataArray[currentIndex] != 99:
        operator = intDataArray[currentIndex]
        loc1 = intDataArray[currentIndex + 1]
        loc2 = intDataArray[currentIndex + 2]
        loc3 = intDataArray[currentIndex + 3]

        val1 = intDataArray[loc1]
        val2 = intDataArray[loc2]

        if(operator == 1):
            intDataArray[loc3] = val1 + val2
        elif(operator == 2):
            intDataArray[loc3] = val1 * val2

        currentIndex += 4

    return intDataArray[0]

def ConvertWireToCoordinate(wire):
    firstChar = wire[0]
    distance = int(wire[1: len(wire)])

    if(firstChar == 'R'):
        return numpy.array([distance,0])
    elif(firstChar == 'L'):
        return numpy.array([-distance,0])
    elif(firstChar == 'U'):
        return numpy.array([0,distance])
    elif(firstChar == 'D'):
        return numpy.array([0,-distance])
    else:
        print(f"Error: {firstChar} is not a valid char")
        quit(0)


def GenerateWires(wireData):

    previousPoint = numpy.array([0,0])
    wires = []
    for wireLine in wireData:
        wireStart = previousPoint
        wireEnd = previousPoint + ConvertWireToCoordinate(wireLine)
        wires.append([wireStart,wireEnd])
        previousPoint = wireEnd
    return wires

def CalculateManhattanDistance(pointA, pointB):
    xDist = abs(pointB[0] - pointA[0])
    yDist = abs(pointB[1] - pointA[1])
    manhattanDistance = xDist + yDist

    return manhattanDistance

def FindShortestDistance(distances):
    return min(distances)

def CalculateWirePartLength(wirePart):
    return CalculateManhattanDistance(wirePart[0], wirePart[1])

def FindAWireIntersection(wirePart1, wirePart2):

    BadIntersection = numpy.array([-9999999,-9999999])

    wire1Start = wirePart1[0]
    wire1End = wirePart1[1]
    wire2Start = wirePart2[0]
    wire2End = wirePart2[1]

    if numpy.array_equal(wire1Start,wire1End) or numpy.array_equal(wire2Start,wire2End):
        return BadIntersection

    bIsWire1Vertical = False
    bIsWire2Vertical = False
    if wire1Start[0] == wire1End[0]:
        bIsWire1Vertical = True
    if wire2Start[0] == wire2End[0]:
        bIsWire2Vertical = True

    if bIsWire1Vertical == bIsWire2Vertical:
        return BadIntersection

    if bIsWire1Vertical:
        #For a hit wire2s start X has to be < wire1s and end X > than wire1s AND wire1s start Y has to be < wire 2s and vice versa
        wire1X = wire1Start[0]
        wire2Y = wire2Start[1]
        if (wire2Start[0] < wire1X and wire2End[0] > wire1X) or (wire2Start[0] > wire1X and wire2End[0] > wire1X):
            #X intersection, now check Y
            if (wire1Start[1] < wire2Y and wire1End[1] > wire2Y) or (wire1Start[1] > wire2Y and wire1End[1] < wire2Y):
                return numpy.array([wire1X,wire2Y])

    else:
        #Wire 1 is horizontal so wire 2 must be vertical
        wire1Y = wire1Start[1]
        wire2X = wire2Start[0]
        if (wire1Start[0] < wire2X and wire1End[0] > wire2X) or (wire1Start[0] > wire2X and wire1End[0] < wire2X):
            #X intersection, now check Y
            if (wire2Start[1] < wire1Y and wire2End[1] > wire1Y) or (wire2Start[1] > wire1Y and wire2End[1] < wire1Y):
                return numpy.array([wire2X,wire1Y])

    return BadIntersection


def FindWireIntersections(wire1, wire2):
    BadIntersection = numpy.array([-9999999,-9999999])
    intersections = []
    for wire1Part in wire1:
        for wire2Part in wire2:
            wireIntersection = FindAWireIntersection(wire1Part, wire2Part)
            if not (numpy.array_equal(wireIntersection, BadIntersection)):
                intersections.append(wireIntersection)

    return intersections

def FindShortestWireDistanceToIntersection(wire1, wire2):
    intersectionDistances = []

    BadIntersection = numpy.array([-9999999,-9999999])
    intersections = []
    currentWire1Length = 0
    currentWire2Length = 0
    for wire1Part in wire1:
        wire1PartLength = CalculateWirePartLength(wire1Part)
        currentWire2Length = 0
        for wire2Part in wire2:
            wire2PartLength = CalculateWirePartLength(wire2Part)
            wireIntersection = FindAWireIntersection(wire1Part, wire2Part)
            if not (numpy.array_equal(wireIntersection, BadIntersection)):
                wire1IntersectionDistance = CalculateManhattanDistance(wire1Part[0],wireIntersection)
                wire2IntersectionDistance = CalculateManhattanDistance(wire2Part[0],wireIntersection)
                intersectionDistances.append(currentWire1Length + wire1IntersectionDistance + currentWire2Length + wire2IntersectionDistance)
            currentWire2Length += wire2PartLength
        currentWire1Length += wire1PartLength

    return min(intersectionDistances)



def SolveDayPartA(filepath):
    with open(filepath, "r") as openedFile:
        fileData = openedFile.readlines()
    origin = numpy.array([0, 0])

    wireArray = []
    for fileLine in fileData:
        dataLine = (fileLine.split(','))
        wireArray.append(GenerateWires(dataLine))

    wireIntersections = FindWireIntersections(wireArray[0], wireArray[1])

    distances = []
    for intersection in wireIntersections:
        distances.append(CalculateManhattanDistance(origin, intersection))
    shortestDistance = FindShortestDistance(distances)

    return shortestDistance




def SolveDayPartB(filepath):
    with open(filepath, "r") as openedFile:
        fileData = openedFile.readlines()
    origin = numpy.array([0, 0])


    wireArray = []

    for fileLine in fileData:
        dataLine = (fileLine.split(','))
        wireArray.append(GenerateWires(dataLine))

    #wireArray.append(GenerateWires(["R8","U5","L5","D3"]))
    #wireArray.append(GenerateWires(["U7","R6","D4","L4"]))

    shortestWireLengthsToIntersection = FindShortestWireDistanceToIntersection(wireArray[0], wireArray[1])
    return shortestWireLengthsToIntersection

filePath = "C:\\dev\\AdventOfCode2019\\Input\\Day3.txt"
print_count(SolveDayPartA(filePath))
print_count(SolveDayPartB(filePath))