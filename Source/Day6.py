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

def splitIntIntoDigitArray(number):
    return [int(digit) for digit in str(number)]

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


def GetCommandCode(opcode):
    operator = int(str(opcode)[-2:])
    opcodeStr = str(opcode)
    parameterStr = opcodeStr[:len(opcodeStr)-2]
    parameterModes = []
    if parameterStr != '':
        reversedStr = parameterStr[::-1]
        parameterModes = splitInt(reversedStr)
    commandCode = []
    commandCode.append(operator)
    commandCode.extend(parameterModes)
    return commandCode

def RunOpcode(commandCode, dataArray, startingIndex):
    operator = commandCode[0]
    parameterValues = []
    invalidOutput = -99999999999
    result = [] # Always return 2 values. 1: Output, invalidOutput if none 2: Number of spots in dataArray to increment by
    if operator == 1:
        #Expect 3 parameters
        parameter1Mode = 0
        parameter2Mode = 0
        if IsValidIndex(commandCode, 1):
            parameter1Mode = commandCode[1]
        if IsValidIndex(commandCode, 2):
            parameter2Mode = commandCode[2]

        val1 = 0
        val2 = 0
        val3 = 0
        if parameter1Mode == 0:
            val1 = dataArray[dataArray[startingIndex+1]]
        else:
            val1 = dataArray[startingIndex+1]

        if parameter2Mode == 0:
            val2 = dataArray[dataArray[startingIndex+2]]
        else:
            val2 = dataArray[startingIndex+2]

        val3 = val1 + val2
        dataArray[dataArray[startingIndex+3]] = val3
        return [invalidOutput,startingIndex+4]
    elif operator == 2:
        #Expect 3 parameters
        parameter1Mode = 0
        parameter2Mode = 0
        if IsValidIndex(commandCode, 1):
            parameter1Mode = commandCode[1]
        if IsValidIndex(commandCode, 2):
            parameter2Mode = commandCode[2]

        val1 = 0
        val2 = 0
        val3 = 0
        if parameter1Mode == 0:
            val1 = dataArray[dataArray[startingIndex+1]]
        else:
            val1 = dataArray[startingIndex+1]

        if parameter2Mode == 0:
            val2 = dataArray[dataArray[startingIndex+2]]
        else:
            val2 = dataArray[startingIndex+2]

        val3 = val1 * val2
        dataArray[dataArray[startingIndex+3]] = val3
        return [invalidOutput,startingIndex+4]
    elif operator == 3:
        val1 = int(input("prompt: "))
        dataArray[dataArray[startingIndex+1]] = val1
        return [invalidOutput,startingIndex+2]
    elif operator == 4:
        parameter1Mode = 0
        if IsValidIndex(commandCode, 1):
            parameter1Mode = commandCode[1]
        val1 = 0
        if parameter1Mode == 0:
            val1 = dataArray[dataArray[startingIndex+1]]
        else:
            val1 = dataArray[startingIndex+1]
        return [val1,startingIndex+2]
    elif operator == 5: #jump-if-true
        parameter1Mode = 0
        parameter2Mode = 0
        if IsValidIndex(commandCode, 1):
            parameter1Mode = commandCode[1]
        if IsValidIndex(commandCode, 2):
            parameter2Mode = commandCode[2]

        val1 = 0
        val2 = 0
        if parameter1Mode == 0:
            val1 = dataArray[dataArray[startingIndex+1]]
        else:
            val1 = dataArray[startingIndex+1]

        if parameter2Mode == 0:
            val2 = dataArray[dataArray[startingIndex+2]]
        else:
            val2 = dataArray[startingIndex+2]

        newStartingIndex = startingIndex
        if val1 != 0:
            return[invalidOutput,val2]
        else:
            return[invalidOutput,startingIndex+3]
    elif operator == 6: #jump-if-false
        parameter1Mode = 0
        parameter2Mode = 0
        if IsValidIndex(commandCode, 1):
            parameter1Mode = commandCode[1]
        if IsValidIndex(commandCode, 2):
            parameter2Mode = commandCode[2]

        val1 = 0
        val2 = 0
        if parameter1Mode == 0:
            val1 = dataArray[dataArray[startingIndex + 1]]
        else:
            val1 = dataArray[startingIndex + 1]

        if parameter2Mode == 0:
            val2 = dataArray[dataArray[startingIndex + 2]]
        else:
            val2 = dataArray[startingIndex + 2]

        newStartingIndex = startingIndex
        if val1 == 0:
            return [invalidOutput, val2]
        else:
            return [invalidOutput, startingIndex + 3]
    elif operator == 7: #less-than
        # Expect 3 parameters
        parameter1Mode = 0
        parameter2Mode = 0
        if IsValidIndex(commandCode, 1):
            parameter1Mode = commandCode[1]
        if IsValidIndex(commandCode, 2):
            parameter2Mode = commandCode[2]

        val1 = 0
        val2 = 0
        val3 = 0
        if parameter1Mode == 0:
            val1 = dataArray[dataArray[startingIndex + 1]]
        else:
            val1 = dataArray[startingIndex + 1]

        if parameter2Mode == 0:
            val2 = dataArray[dataArray[startingIndex + 2]]
        else:
            val2 = dataArray[startingIndex + 2]

        valueToStore = 0
        if val1 < val2:
            valueToStore = 1

        dataArray[dataArray[startingIndex + 3]] = valueToStore
        return [invalidOutput, startingIndex + 4]
    elif operator == 8: #equals-than
        # Expect 3 parameters
        parameter1Mode = 0
        parameter2Mode = 0
        if IsValidIndex(commandCode, 1):
            parameter1Mode = commandCode[1]
        if IsValidIndex(commandCode, 2):
            parameter2Mode = commandCode[2]

        val1 = 0
        val2 = 0
        val3 = 0
        if parameter1Mode == 0:
            val1 = dataArray[dataArray[startingIndex + 1]]
        else:
            val1 = dataArray[startingIndex + 1]

        if parameter2Mode == 0:
            val2 = dataArray[dataArray[startingIndex + 2]]
        else:
            val2 = dataArray[startingIndex + 2]

        valueToStore = 0
        if val1 == val2:
            valueToStore = 1

        dataArray[dataArray[startingIndex + 3]] = valueToStore
        return [invalidOutput, startingIndex + 4]



def CalculateIntCode(dataArray):
    intDataArray = dataArray.copy()
    invalidOutput = -99999999999
    currentIndex = 0
    output=0
    while intDataArray[currentIndex] != 99:
        opcode = intDataArray[currentIndex]
        commandCode = GetCommandCode(opcode)
        result = RunOpcode(commandCode, intDataArray, currentIndex)
        output = result[0]
        newIndex = result[1]

        if output != invalidOutput:
            print("Output: " + str(output))

        currentIndex = newIndex

    return output


def CalculateManhattanDistance(pointA, pointB):
    xDist = abs(pointB[0] - pointA[0])
    yDist = abs(pointB[1] - pointA[1])
    manhattanDistance = xDist + yDist

    return manhattanDistance

def FindShortestDistance(distances):
    return min(distances)

def IsNumberAscending(number):
    digitArray = splitIntIntoDigitArray(number)
    for index in range(0, len(digitArray) - 1):
        if(digitArray[index] > digitArray[index+1]):
            return False
    return True


def GetOrbitCount(orbitingDict:dict, key):
    currentKey = key
    orbitCount = 0
    while True:
        if currentKey in orbitingDict:
            currentKey = orbitingDict[currentKey]
        else:
            break
        orbitCount += 1
    return orbitCount

def SolveDayPartA(filepath):
    with open(filepath, "r") as openedFile:
        fileData = openedFile.readlines()

    orbitingDict = {}
    for fileLine in fileData:
        fileRow = fileLine.strip().split(')')
        orbitingDict[fileRow[1]] = fileRow[0]

    orbits = 0
    for key in orbitingDict:
        orbits += GetOrbitCount(orbitingDict,key)
    return orbits

def GetOrbitArray(orbitingDict, start):
    currentKey = start
    orbitArray = [start]
    while True:
        if currentKey in orbitingDict:
            currentKey = orbitingDict[currentKey]
            orbitArray.append(currentKey)
        else:
            break

    return orbitArray[::-1]

def SolveDayPartB(filepath):
    with open(filepath, "r") as openedFile:
        fileData = openedFile.readlines()

    startingOrbit = 'YOU'
    endOrbit = 'SAN'
    orbitingDict = {}
    for fileLine in fileData:
        fileRow = fileLine.strip().split(')')
        orbitingDict[fileRow[1]] = fileRow[0]

    actualStart = orbitingDict[startingOrbit]
    actualEnd = orbitingDict[endOrbit]
    orbits = 0

    startOrbitArray = GetOrbitArray(orbitingDict, actualStart)
    endOrbitArray = GetOrbitArray(orbitingDict, actualEnd)

    #look for either the end or the branching point
    #if a branching point is found then its the number of indices between each arrays current point and end
    #if a branching point is not found then one start must be in the others end
    currentIndex = 0
    wasBranchFound = False
    wasStartFoundInEnd = False
    wasEndFoundInStart = False
    for orbitObject in startOrbitArray:
        if orbitObject == actualEnd:
            wasEndFoundInStart = True
            break
        elif orbitObject in endOrbitArray:
            currentIndex+=1
            continue
        else:
            wasBranchFound = True
            break

    distanceFromStartToEnd = 0
    if wasBranchFound:
        startOrbitToBranch = len(startOrbitArray) - currentIndex
        endOrbitToBranch = len(endOrbitArray) - currentIndex
        distanceFromStartToEnd = startOrbitToBranch + endOrbitToBranch
        return distanceFromStartToEnd

    if wasStartFoundInEnd:
        distanceFromStartToEnd = len(startOrbitArray) - currentIndex

    else:
        distanceFromStartToEnd = len(endOrbitArray) - currentIndex

    return distanceFromStartToEnd

filePath = "C:\\dev\\AdventOfCode2019\\Input\\Day6.txt"
print_count(SolveDayPartA(filePath))
print_count(SolveDayPartB(filePath))