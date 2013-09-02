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

def getItem(blueprint, nsIndex, weIndex):
	if nsIndex < 0 or len(blueprint) <= nsIndex:
		return "_"

	blueprintRow = blueprint[nsIndex]

	if weIndex < 0 or len(blueprintRow) <= weIndex:
		return "_"

	return blueprintRow[weIndex]

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

		if not isBuilding(blueprintItem):
			nwItem = getItem(blueprint, nsIndex - 1, weIndex - 1)
			nItem = getItem(blueprint, nsIndex - 1, weIndex)
			neItem = getItem(blueprint, nsIndex - 1, weIndex + 1)
			wItem = getItem(blueprint, nsIndex, weIndex - 1)
			eItem = getItem(blueprint, nsIndex, weIndex + 1)
			swItem = getItem(blueprint, nsIndex + 1, weIndex - 1)
			sItem = getItem(blueprint, nsIndex + 1, weIndex)
			seItem = getItem(blueprint, nsIndex + 1, weIndex + 1)

			if wItem != blueprintItem and nItem != blueprintItem:
				block.addChild(EggExternalReference("sidewalk", "nwexteriorsidewalk"))
			if eItem != blueprintItem and nItem != blueprintItem:
				block.addChild(EggExternalReference("sidewalk", "neexteriorsidewalk"))
			if wItem != blueprintItem and sItem != blueprintItem:
				block.addChild(EggExternalReference("sidewalk", "swexteriorsidewalk"))
			if eItem != blueprintItem and sItem != blueprintItem:
				block.addChild(EggExternalReference("sidewalk", "seexteriorsidewalk"))
			if wItem == blueprintItem and nItem == blueprintItem and nwItem != blueprintItem:
				block.addChild(EggExternalReference("sidewalk", "nwinteriorsidewalk"))
			if eItem == blueprintItem and nItem == blueprintItem and neItem != blueprintItem:
				block.addChild(EggExternalReference("sidewalk", "neinteriorsidewalk"))
			if wItem == blueprintItem and sItem == blueprintItem and swItem != blueprintItem:
				block.addChild(EggExternalReference("sidewalk", "swinteriorsidewalk"))
			if eItem == blueprintItem and sItem == blueprintItem and seItem != blueprintItem:
				block.addChild(EggExternalReference("sidewalk", "seinteriorsidewalk"))
			if wItem != blueprintItem and nItem == blueprintItem:
				block.addChild(EggExternalReference("sidewalk", "nwhalf1sidewalk"))
			if eItem != blueprintItem and nItem == blueprintItem:
				block.addChild(EggExternalReference("sidewalk", "nehalf2sidewalk"))
			if wItem != blueprintItem and sItem == blueprintItem:
				block.addChild(EggExternalReference("sidewalk", "swhalf2sidewalk"))
			if eItem != blueprintItem and sItem == blueprintItem:
				block.addChild(EggExternalReference("sidewalk", "sehalf1sidewalk"))
			if wItem == blueprintItem and nItem != blueprintItem:
				block.addChild(EggExternalReference("sidewalk", "nwhalf2sidewalk"))
			if eItem == blueprintItem and nItem != blueprintItem:
				block.addChild(EggExternalReference("sidewalk", "nehalf1sidewalk"))
			if wItem == blueprintItem and sItem != blueprintItem:
				block.addChild(EggExternalReference("sidewalk", "swhalf1sidewalk"))
			if eItem == blueprintItem and sItem != blueprintItem:
				block.addChild(EggExternalReference("sidewalk", "sehalf2sidewalk"))

city.writeEgg("models/city.egg")
