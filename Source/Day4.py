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

def DoesNumberHaveSameAdjacentDigit(number):
    digitArray = splitIntIntoDigitArray(number)
    for index in range(0, len(digitArray) - 1):
        if(digitArray[index] == digitArray[index+1]):
            return True
    return False

def DoesNumberHaveSameAdjacentDigitButNotMore(number):
    digitArray = splitIntIntoDigitArray(number)
    bHasAtLeaseOnePair = False
    for index in range(0, len(digitArray) - 1):
        if(digitArray[index] == digitArray[index+1]):
            if index != 0:
                if digitArray[index] == digitArray[index-1]:
                    continue
            if len(digitArray) <= index + 2:
                return True
            if digitArray[index] == digitArray[index+2]:
                continue
            else:
                bHasAtLeaseOnePair = True
    return bHasAtLeaseOnePair

def SolveDayPartA(filepath):
    with open(filepath, "r") as openedFile:
        fileData = openedFile.readlines()

    fileLine = fileData[0]
    passwordRange = strArrayToIntArray(fileLine.split('-'))

    passwordCount = 0
    for possiblePassword in range(passwordRange[0],passwordRange[1]):
        #Check for two of the same adjacent digit
        #Check for only ascending digits
        if IsNumberAscending(possiblePassword) and DoesNumberHaveSameAdjacentDigit(possiblePassword):
            passwordCount += 1

    return passwordCount




def SolveDayPartB(filepath):
    with open(filepath, "r") as openedFile:
        fileData = openedFile.readlines()

    fileLine = fileData[0]
    passwordRange = strArrayToIntArray(fileLine.split('-'))

    passwordCount = 0
    for possiblePassword in range(passwordRange[0],passwordRange[1]):
        #Check for two of the same adjacent digit
        #Check for only ascending digits
        if IsNumberAscending(possiblePassword) and DoesNumberHaveSameAdjacentDigitButNotMore(possiblePassword):
            passwordCount += 1

    return passwordCount

filePath = "C:\\dev\\AdventOfCode2019\\Input\\Day4.txt"
print_count(SolveDayPartA(filePath))
print_count(SolveDayPartB(filePath))