from traceback import *
from utils import *
from bop import *

totalErrorCount = None

def checkEquals(expected, actual):
	if expected != actual:
		print "Failure: expected", expected, "but was", actual

# Tests definitions

def testCityBlueprintAndPopulation():
	print "testCityBlueprintAndPopulation..."

	game = Game(scriptPath)

	blueprint = game.getCityBlueprint()

	checkEquals(9, blueprint.getSizeNS())
	checkEquals(7, blueprint.getSizeWE())

	checkEquals(CityCell.POLICE_BUILDING, blueprint.getCell(0, 0))
	checkEquals(CityCell.ROAD, blueprint.getCell(0, 1))
	checkEquals(CityCell.OFFICE_BUILDING, blueprint.getCell(0, 2))
	checkEquals(CityCell.HOUSE, blueprint.getCell(0, 4))
	checkEquals(CityCell.GROUND, blueprint.getCell(0, 6))

	population = game.getPopulation()

	checkEquals(21, population.getCharacterCount())

# Insert more test definitions before this line

# Tests execution

totalErrorCount = 0

for test in [
	testCityBlueprintAndPopulation
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
