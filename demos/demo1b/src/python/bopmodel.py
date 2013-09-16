import os
from panda3d.core import *
from bisect import *
from utils import *


oneSecond = 1000L
oneMinute = 60L * oneSecond
oneHour = 60L * oneMinute
oneDay = 24L * oneHour
oneWeek = 7L * oneDay
oneYear = 365L * oneDay
oneMillenium = 1000L * oneYear
midnight = 0L
noon = 12L * oneHour


def isUndefined(x):
    return x is None


def lerp(t1, v1, t2, v2, t):
    if isUndefined(v1) or isUndefined(v2):
        return None

    return v1 + (v2 - v1) * (t - t1) / (t2 - t1)


class Chronology:

    def __init__(self, period):
        self.period = period
        self.times = []
        self.values = []

    def getPeriod(self):
        return self.period

    def setValue(self, time, value):
        i = bisect(self.times, time)

        if i < len(self.times) and self.times[i] == time:
            self.values[i] = value
        else:
            self.times.insert(i, time)
            self.values.insert(i, value)

    def getValue(self, time):
        return None


class PiecewiseConstantChronology(Chronology):

    def __init__(self, period):
        Chronology.__init__(self, period)

    def getValue(self, time):
        i = bisect(self.times, time % self.getPeriod())

        return self.values[i - 1]


class PiecewiseLinearChronology(Chronology):

    def __init__(self, period):
        Chronology.__init__(self, period)

    def getValue(self, time):
        if 0 == len(self.times):
            return None

        t = time % self.getPeriod()
        i = bisect(self.times, t)

        if i == len(self.times):
            return lerp(self.times[i - 1], self.values[i - 1],
                        self.times[0] + self.getPeriod(), self.values[0], t)

        return lerp(self.times[i - 1], self.values[i - 1],
                    self.times[i], self.values[i], t)


class Persona:

    def __init__(self, period):
        self.position = PiecewiseLinearChronology(period)

    def getPosition(self, time):
        return self.position.getValue(time)

    def setPosition(self, time, value):
        self.position.setValue(time, value)


class Character:

    def __init__(self):
        self.actualPersona = Persona(oneMillenium)
        self.routinePersona = Persona(oneDay)

    def getActualPersona(self):
        return self.actualPersona

    def getRoutinePersona(self):
        return self.routinePersona

    def getPosition(self, time):
        value = self.getActualPersona().getPosition(time)

        return value if not value is None\
            else self.getRoutinePersona().getPosition(time)


class Population:

    def __init__(self):
        self.characters = []

    def getCharacterCount(self):
        return len(self.characters)

    def getCharacter(self, index):
        return self.characters[index]

    def addCharacter(self, character):
        self.characters.append(character)


class CityBlock:

    GROUND = "ground"

    ROAD = "road"

    POLICE_BUILDING = "policeBuilding"

    OFFICE_BUILDING = "officeBuilding"

    HOUSE = "house"

    def __init__(self, cityBlockType, position):
        self.cityBlockType = cityBlockType
        self.position = position

    def getType(self):
        return self.cityBlockType

    def getPosition(self):
        return self.position


class City:

    BLOCK_SIZE = 10.0

    def __init__(self, blueprintPath):
        blueprint = [line.strip() for line in open(blueprintPath)]
        self.blockCountNS = len(blueprint)
        self.blockCountWE = len(max(blueprint, key=len))
        self.blocks = []
        self.sizeNS = self.getBlockCountNS() * City.BLOCK_SIZE
        self.sizeWE = self.getBlockCountWE() * City.BLOCK_SIZE

        for nsIndex, blueprintRow in enumerate(blueprint):
            self.blocks.append([])

            for weIndex, blueprintItem in enumerate(blueprintRow):
                self.blocks[nsIndex].append(
                    CityBlock(City.blockTypeFromBlueprintItem(blueprintItem),
                              self.blockPosition(nsIndex, weIndex)))

    def getBlockCountNS(self):
        return self.blockCountNS

    def getBlockCountWE(self):
        return self.blockCountWE

    def getSizeNS(self):
        return self.sizeNS

    def getSizeWE(self):
        return self.sizeWE

    def getBlock(self, nsIndex, weIndex):
        if 0 <= nsIndex and nsIndex < self.getBlockCountNS() and\
                0 <= weIndex and weIndex < self.getBlockCountWE():
            return self.blocks[nsIndex][weIndex]
        else:
            return CityBlock(CityBlock.GROUND,
                             self.blockPosition(nsIndex, weIndex))

    def blockPosition(self, nsIndex, weIndex):
        blockX = weIndex * City.BLOCK_SIZE - self.sizeWE / 2
        blockY = (self.sizeNS / 2 - (nsIndex + 1) * City.BLOCK_SIZE)

        return City.vec3(blockX, blockY)

    @staticmethod
    def blockTypeFromBlueprintItem(item):
        return {
            "S": CityBlock.ROAD,
            "P": CityBlock.POLICE_BUILDING,
            "O": CityBlock.OFFICE_BUILDING,
            "H": CityBlock.HOUSE
        }.get(item,  CityBlock.GROUND)

    @staticmethod
    def vec3(blockX, blockY):
        return Vec3(blockX, blockY, 0.0)


class Game:

    def __init__(self, blueprintPath=os.path.join(
            scriptPath, "data", "cityblueprint.txt")):
        self.time = 0L
        self.city = City(blueprintPath)
        self.population = Game.newPopulation(self.getCity())

    def getTime(self):
        return self.time

    def getCity(self):
        return self.city

    def getPopulation(self):
        return self.population

    def update(self, milliseconds):
        self.time += milliseconds

    @staticmethod
    def newPopulation(city):
        result = Population()
        offices = []

        for nsIndex in range(city.getBlockCountNS()):
            for weIndex in range(city.getBlockCountWE()):
                block = city.getBlock(nsIndex, weIndex)

                if CityBlock.HOUSE == block.getType():
                    character = Character()
                    character.getRoutinePersona().setPosition(
                        midnight, block.getPosition())
                    result.addCharacter(character)
                elif CityBlock.OFFICE_BUILDING == block.getType():
                    offices.append(block)

        for i in range(result.getCharacterCount()):
            result.getCharacter(i).getRoutinePersona().setPosition(
                noon, offices[i % len(offices)].getPosition())

        return result
