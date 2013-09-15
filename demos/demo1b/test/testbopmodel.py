import sys, os, inspect
from traceback import *
import bopmodel
from bopmodel import *
from panda3d.core import *
from utils import *

def checkEquals(expected, actual):
    if expected != actual:
        global totalFailureCount

        totalFailureCount += 1

        print inspect.stack()[1]
        print "FAILURE: expected", expected, "but was", actual

# Tests definitions

framerate = 40 # Actual value may not be constant
millisecondsPerFrame = oneSecond / framerate
sixAM = 6L * oneHour
threeAM = 3L * oneHour
sevenAM = 7L * oneHour
eightAM = 8L * oneHour
noon = 12L * oneHour
twoPM = 14L * oneHour
sixPM = 18L * oneHour
sevenPM = 19L * oneHour
eightPM = 20L * oneHour
tenPM = 22L * oneHour
january = -1L * oneDay
february = january + 31L * oneDay
january14th = january + 14L * oneDay
january15th = january + 15L * oneDay
january16th = january + 16L * oneDay
february15th = february + 15L * oneDay
blueprintPath = os.path.join(scriptPath, "data", "testcityblueprint.txt")

def testRoutinePersona():
    print "testRoutinePersona..."

    character = bopmodel.Character()
    home = Vec3(0.0, 0.0, 0.0)
    office = Vec3(10.0, 10.0, 0.0)
    midway = (home + office) / 2.0

    checkEquals(None, character.getPosition(midnight))

    character.getRoutinePersona().setPosition(midnight, home)

    checkEquals(home, character.getPosition(midnight))
    checkEquals(home, character.getPosition(noon))

    character.getRoutinePersona().setPosition(noon, office)

    checkEquals(home,   character.getPosition(midnight))
    checkEquals(midway, character.getPosition(sixAM))
    checkEquals(office, character.getPosition(noon))
    checkEquals(midway, character.getPosition(sixPM))

    character.getRoutinePersona().setPosition(sixAM,   home)
    character.getRoutinePersona().setPosition(eightAM, office)
    character.getRoutinePersona().setPosition(sixPM,   office)
    character.getRoutinePersona().setPosition(eightPM, home)

    checkEquals(home,   character.getPosition(midnight))
    checkEquals(home,   character.getPosition(sixAM))
    checkEquals(midway, character.getPosition(sevenAM))
    checkEquals(office, character.getPosition(eightAM))
    checkEquals(office, character.getPosition(noon))
    checkEquals(office, character.getPosition(sixPM))
    checkEquals(midway, character.getPosition(sevenPM))
    checkEquals(home,   character.getPosition(eightPM))
    checkEquals(home,   character.getPosition(tenPM))
    checkEquals(home,   character.getPosition(oneWeek + midnight))
    checkEquals(office, character.getPosition(oneWeek + noon))

    print "testRoutinePersona: OK"

def testActualPersona():
    print "testActualPersona..."

    character = bopmodel.Character()
    home = Vec3(0.0, 0.0, 0.0)
    office = Vec3(10.0, 10.0, 0.0)
    dentist = Vec3(10.0, 20.0, 0.0)

    character.getRoutinePersona().setPosition(midnight, home)
    character.getRoutinePersona().setPosition(noon, office)

    character.getActualPersona().setPosition(january15th + midnight - 1L, None)
    character.getActualPersona().setPosition(january15th + midnight,      home)
    character.getActualPersona().setPosition(january15th + noon,          dentist)
    character.getActualPersona().setPosition(january16th + midnight,      home)
    character.getActualPersona().setPosition(january16th + midnight + 1L, None)

    checkEquals(home,    character.getPosition(january14th + midnight))
    checkEquals(office,  character.getPosition(january14th + noon))
    checkEquals(home,    character.getPosition(january15th + midnight))
    checkEquals(dentist, character.getPosition(january15th + noon))
    checkEquals(home,    character.getPosition(january16th + midnight))
    checkEquals(office,  character.getPosition(january16th + noon))
    checkEquals(home,    character.getPosition(february15th + midnight))
    checkEquals(office,  character.getPosition(february15th + noon))

    print "testActualPersona: OK"

def testPiecewiseConstantChronology():
    print "testPiecewiseConstantChronology..."

    day = PiecewiseConstantChronology(oneDay)

    day.setValue(sixAM, "morning")
    day.setValue(noon,  "afternoon")
    day.setValue(sixPM, "night")

    checkEquals("morning",   day.getValue(sixAM))
    checkEquals("morning",   day.getValue(eightAM))
    checkEquals("afternoon", day.getValue(noon))
    checkEquals("afternoon", day.getValue(twoPM))
    checkEquals("night",     day.getValue(sixPM))
    checkEquals("night",     day.getValue(tenPM))
    checkEquals("night",     day.getValue(midnight))
    checkEquals("night",     day.getValue(threeAM))

    print "testPiecewiseConstantChronology: OK"

def testCity():
    print "testCity..."

    city = City(blueprintPath)

    checkEquals(9, city.getBlockCountNS())
    checkEquals(7, city.getBlockCountWE())

    checkEquals(CityBlock.POLICE_BUILDING, city.getBlock(0, 0).getType())
    checkEquals(Vec3(-3.5, 0.0, -3.5) * City.BLOCK_SIZE, city.getBlock(0, 0).getPosition())
    checkEquals(CityBlock.ROAD, city.getBlock(0, 1).getType())
    checkEquals(Vec3(-2.5, 0.0, -3.5) * City.BLOCK_SIZE, city.getBlock(0, 1).getPosition())
    checkEquals(CityBlock.OFFICE_BUILDING, city.getBlock(0, 2).getType())
    checkEquals(Vec3(-1.5, 0.0, -3.5) * City.BLOCK_SIZE, city.getBlock(0, 2).getPosition())
    checkEquals(CityBlock.HOUSE, city.getBlock(0, 4).getType())
    checkEquals(Vec3(0.5, 0.0, -3.5) * City.BLOCK_SIZE, city.getBlock(0, 4).getPosition())
    checkEquals(CityBlock.GROUND, city.getBlock(0, 6).getType())
    checkEquals(Vec3(2.5, 0.0, -3.5) * City.BLOCK_SIZE, city.getBlock(0, 6).getPosition())

    checkEquals(CityBlock.GROUND, city.getBlock(-1, -1).getType())
    checkEquals(Vec3(-4.5, 0.0, -4.5) * City.BLOCK_SIZE, city.getBlock(-1, -1).getPosition())

    print "testCity: OK"

def testUpdate():
    print "testUpdate..."

    game = Game(blueprintPath)

    checkEquals(midnight, game.getTime())

    population = game.getPopulation()

    # Character 0 is player
    for i in range(1, 21):
        character = population.getCharacter(i)

        checkEquals(character.getRoutinePersona().getPosition(midnight), character.getPosition(game.getTime()))

    for i in range(12L * oneHour / millisecondsPerFrame):
        game.update(millisecondsPerFrame)

    checkEquals(noon, game.getTime())

    for i in range(1, 21):
        character = population.getCharacter(i)

        checkEquals(character.getRoutinePersona().getPosition(noon), character.getPosition(game.getTime()))

# Insert more test definitions before this line

# Tests execution

totalFailureCount = 0

for test in [
    testRoutinePersona,
    testActualPersona,
    testPiecewiseConstantChronology,
    testCity,
    testUpdate
# Insert more test names before this line
]:
    try:
        test()
    except Exception:
        totalFailureCount += 1

        print "FAILURE: Unexpected error:", sys.exc_info()
        print_tb(sys.exc_info()[2])

if 0 == totalFailureCount:
    print "All tests PASS"
else:
    print "Some tests FAIL:", totalFailureCount, "failure(s) detected"
    
    quit(-1)
