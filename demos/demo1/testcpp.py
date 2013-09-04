from traceback import *
from utils import *
from bop import *

totalErrorCount = None

def checkEquals(expected, actual):
	if expected != actual:
		global totalErrorCount

		totalErrorCount += 1

		print "Failure: expected", expected, "but was", actual

# Tests definitions

framerate = 40 # Actual value may not be constant
oneSecond = 1000L # Make sure all times are in same unit (eg milliseconds)
millisecondsPerFrame = oneSecond / framerate
oneHour = 3600L * oneSecond
midnight = 0L * oneHour
noon = 12L * oneHour
game = None

def initializeTests():
	print "initializeTests..."

	global game

	game = Game(scriptPath)

def testCityBlueprint():
	print "testCityBlueprint..."

	blueprint = game.getCityBlueprint()

	checkEquals(9, blueprint.getSizeNS())
	checkEquals(7, blueprint.getSizeWE())

	checkEquals(CityCell.POLICE_BUILDING, blueprint.getCell(0, 0))
	checkEquals(CityCell.ROAD, blueprint.getCell(0, 1))
	checkEquals(CityCell.OFFICE_BUILDING, blueprint.getCell(0, 2))
	checkEquals(CityCell.HOUSE, blueprint.getCell(0, 4))
	checkEquals(CityCell.GROUND, blueprint.getCell(0, 6))

def testPopulation():
	print "testPopulation..."

	population = game.getPopulation()

	checkEquals(21, population.getCharacterCount())

def testUpdate():
	print "testUpdate..."

	checkEquals(midnight, game.getTime())

	population = game.getPopulation()

	# Character 0 is player
	for i in range(1, 21):
		character = population.getCharacter(i)
		routinePosition = character.getRoutinePersona().getPosition()
		actualPosition = character.getActualPersona().getPosition()

		checkEquals(routinePosition.getValue(midnight), actualPosition.getValue(game.getTime()))

	for i in range(12L * oneHour / millisecondsPerFrame):
		game.update(millisecondsPerFrame)

	checkEquals(noon, game.getTime())

	for i in range(1, 21):
		character = population.getCharacter(i)
		routinePosition = character.getRoutinePersona().getPosition()
		actualPosition = character.getActualPersona().getPosition()
		
		checkEquals(routinePosition.getValue(noon), actualPosition.getValue(game.getTime()))

# Insert more test definitions before this line

# Tests execution

totalErrorCount = 0

for test in [
	initializeTests,
	testCityBlueprint,
	testPopulation,
	testUpdate
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
