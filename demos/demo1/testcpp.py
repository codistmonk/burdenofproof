from utils import *
from bop import *

totalErrorCount = None

def checkEquals(expected, actual):
	if expected != actual:
		totalErrorCount += 1
		print "Failure: expected", expected, "but was", actual

# Tests definitions

def testCityBlueprint():
	print "testCityBlueprint..."

	game = Game(scriptPath)
	blueprint = game.getCityBlueprint()

	checkEquals(9, blueprint.getSizeNS())
	checkEquals(7, blueprint.getSizeWE())

	checkEquals(CityCell.POLICE_BUILDING, blueprint.getCell(0, 0))
	checkEquals(CityCell.ROAD, blueprint.getCell(0, 1))
	checkEquals(CityCell.OFFICE_BUILDING, blueprint.getCell(0, 2))
	checkEquals(CityCell.HOUSE, blueprint.getCell(0, 4))
	checkEquals(CityCell.GROUND, blueprint.getCell(0, 6))

# Insert more test definitions before this line

# Tests execution

totalErrorCount = 0

testCityBlueprint()

# Insert more test calls before this line

if 0 == totalErrorCount:
	print "All tests PASS"
else:
	print "Some tests FAIL:", totalErrorCount, "failures detected"
