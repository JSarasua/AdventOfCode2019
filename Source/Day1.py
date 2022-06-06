import statistics
from collections import Counter

#For all days
def print_count(countValue):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Total Count: {countValue}')  # Press Ctrl+F8 to toggle the breakpoint.

def split(word):
    return [char for char in word]

def splitInt(word):
    return [int(char) for char in word]

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

def CalculateFuelPartA(mass:int):
    fuel = int(mass/3) - 2
    return fuel

def CalculateFuelPartB(mass:int):
    currentMass = mass
    fuel = 0
    while currentMass > 0:
        fuelIncrement = int(currentMass / 3) - 2
        fuel += max(fuelIncrement, 0)
        currentMass = fuelIncrement
    return fuel

def SolveDayPartA(filepath):
    with open(filepath, "r") as openedFile:
        fileData = openedFile.readlines()

    #testMass12 = 12
    #testMass14 = 14
    #testMass1969 = 1969
    #testMass100756 = 100756
    #print(CalculateFuel(testMass12))
    #print(CalculateFuel(testMass14))
    #print(CalculateFuel(testMass1969))
    #print(CalculateFuel(testMass100756))

    currentFuelRequirement = 0
    for fileline in fileData:
        currentFuelRequirement += CalculateFuelPartA(int(fileline))
    return currentFuelRequirement



def SolveDayPartB(filepath):
    with open(filepath, "r") as openedFile:
        fileData = openedFile.readlines()

    testMass12 = 12
    testMass14 = 14
    testMass1969 = 1969
    testMass100756 = 100756
    print(CalculateFuelPartB(testMass12))
    print(CalculateFuelPartB(testMass14))
    print(CalculateFuelPartB(testMass1969))
    print(CalculateFuelPartB(testMass100756))

    currentFuelRequirement = 0
    for fileline in fileData:
        currentFuelRequirement += CalculateFuelPartB(int(fileline))
    return currentFuelRequirement

filePath = "C:\\dev\\AdventOfCode2019\\Input\\Day1.txt"
print_count(SolveDayPartA(filePath))
print_count(SolveDayPartB(filePath))