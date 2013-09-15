import sys, os
from traceback import *
import bopmodel
from bopmodel import *
from panda3d.core import *
from utils import *

def checkEquals(expected, actual):
    if expected != actual:
        global totalErrorCount

        totalErrorCount += 1

        print "Failure: expected", expected, "but was", actual

# Tests definitions

framerate = 40 # Actual value may not be constant
midnight = 0L
noon = 12L * oneHour
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

    assert home    == character.getPosition(january14th + midnight)
    assert office  == character.getPosition(january14th + noon)
    assert home    == character.getPosition(january15th + midnight)
    assert dentist == character.getPosition(january15th + noon)
    assert home    == character.getPosition(january16th + midnight)
    assert office  == character.getPosition(january16th + noon)
    assert home    == character.getPosition(february15th + midnight)
    assert office  == character.getPosition(february15th + noon)

    print "testActualPersona: OK"

def testPiecewiseConstantChronology():
    print "testPiecewiseConstantChronology..."

    day = PiecewiseConstantChronology(oneDay)

    day.setValue(sixAM, "morning")
    day.setValue(noon,  "afternoon")
    day.setValue(sixPM, "night")

    assert "morning"   == day.getValue(sixAM)
    assert "morning"   == day.getValue(eightAM)
    assert "afternoon" == day.getValue(noon)
    assert "afternoon" == day.getValue(twoPM)
    assert "night"     == day.getValue(sixPM)
    assert "night"     == day.getValue(tenPM)
    assert "night"     == day.getValue(midnight)
    assert "night"     == day.getValue(threeAM)

    print "testPiecewiseConstantChronology: OK"

def testCity():
    print "testCity..."

    city = City(os.path.join(scriptPath, "data", "testcityblueprint.txt"))

    checkEquals(9, city.getBlockCountNS())
    checkEquals(7, city.getBlockCountWE())

    checkEquals(CityBlock.POLICE_BUILDING, city.getBlock(0, 0).getType())
    checkEquals(Vec3(0.0, 0.0, -0.0) * City.BLOCK_SIZE, city.getBlock(0, 0).getPosition())
    checkEquals(CityBlock.ROAD, city.getBlock(0, 1).getType())
    checkEquals(Vec3(1.0, 0.0, -0.0) * City.BLOCK_SIZE, city.getBlock(0, 1).getPosition())
    checkEquals(CityBlock.OFFICE_BUILDING, city.getBlock(0, 2).getType())
    checkEquals(Vec3(2.0, 0.0, -0.0) * City.BLOCK_SIZE, city.getBlock(0, 0).getPosition())
    checkEquals(CityBlock.HOUSE, city.getBlock(0, 4).getType())
    checkEquals(Vec3(4.0, 0.0, -0.0) * City.BLOCK_SIZE, city.getBlock(0, 0).getPosition())
    checkEquals(CityBlock.GROUND, city.getBlock(0, 6).getType())
    checkEquals(Vec3(6.0, 0.0, -0.0) * City.BLOCK_SIZE, city.getBlock(0, 0).getPosition())

    print "testCity: OK"

# Insert more test definitions before this line

# Tests execution

totalErrorCount = 0

for test in [
    # initializeTests,
    # testCityBlueprint,
    # testPopulation,
    # testUpdate
    testRoutinePersona,
    testActualPersona,
    testPiecewiseConstantChronology,
    testCity
# Insert more test names before this line
]:
    try:
        test()
    except Exception:
        totalErrorCount += 1
        print "Unexpected error:", sys.exc_info()
        print_tb(sys.exc_info()[2])

if 0 == totalErrorCount:
    print "All tests PASS"
else:
    print "Some tests FAIL:", totalErrorCount, "failure(s) detected"
    
    quit(-1)
