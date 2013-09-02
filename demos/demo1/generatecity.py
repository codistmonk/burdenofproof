import sys, os
from math import *
from panda3d.core import *
from panda3d.egg import *
from utils import *

def newGroup(eggData):
	group = EggGroup()

	group.setGroupType(EggGroup.GTInstance)

	eggData.addChild(group)

	return group

def isBuilding(blueprintItem):
	return blueprintItem == 'P' or blueprintItem == 'O' or blueprintItem == 'H'

def isRoad(blueprintItem):
	return blueprintItem == 'S'

def isGround(blueprintItem):
	return not isBuilding(blueprintItem) and not isRoad(blueprintItem)

blueprintPath = "models/cityblueprint.txt"

blueprint = [line.strip() for line in open(blueprintPath)]

print blueprint

blockSize = 10.0
citySizeNS = len(blueprint) * blockSize
citySizeWE = len(max(blueprint, key = len)) * blockSize

print "citySize:", citySizeNS, citySizeWE

city = EggData()

for nsIndex, blueprintRow in enumerate(blueprint):
	blockZ = -(citySizeNS / 2 - (nsIndex + 1) * blockSize)

	for weIndex, blueprintItem in enumerate(blueprintRow):
		blockX = weIndex * blockSize - citySizeWE / 2
		block = newGroup(city)
		block.addTranslate3d(Vec3D(blockX, 0.0, blockZ))

		if isBuilding(blueprintItem):
			block.addChild(EggExternalReference("building", "building"))
			block.addChild(EggExternalReference("buildingpad", "buildingpad"))
		elif isRoad(blueprintItem):
			block.addChild(EggExternalReference("road", "road"))
		else:
			block.addChild(EggExternalReference("ground", "ground"))

city.writeEgg("models/city.egg")
