from utils import *
from bop import *

# Tests definitions

def testCityBlueprint():
	print "testCityBlueprint..."

	game = Game(scriptPath)
	blueprint = game.getCityBlueprint()

	assert 9 == blueprint.getSizeNS()
	assert 7 == blueprint.getSizeWE()

	assert CityCell.POLICE_BUILDING == blueprint.getCell(0, 0)
	assert CityCell.ROAD == blueprint.getCell(0, 1)
	assert CityCell.OFFICE_BUILDING == blueprint.getCell(0, 2)
	assert CityCell.HOUSE == blueprint.getCell(0, 4)
	assert CityCell.GROUND == blueprint.getCell(0, 6)

	print "testCityBlueprint: OK"

# Tests execution

testCityBlueprint()
