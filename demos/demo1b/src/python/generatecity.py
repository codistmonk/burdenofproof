import sys
import os
from math import *
from panda3d.core import *
from panda3d.egg import *
from utils import *


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


def addExternalReference(nodeName, fileName, block, outlineBlock=None):
    block.addChild(EggExternalReference(nodeName, fileName))

    if not outlineBlock is None:
        outlineBlock.addChild(EggExternalReference(
            nodeName, fileName + "_outline"))


blueprintPath = "models/cityblueprint.txt"

blueprint = [line.strip() for line in open(blueprintPath)]

print blueprint

blockSize = 10.0
citySizeNS = len(blueprint) * blockSize
citySizeWE = len(max(blueprint, key=len)) * blockSize

print "citySize:", citySizeNS, citySizeWE

city = EggData()
cityOuline = EggData()

for nsIndex, blueprintRow in enumerate(blueprint):
    blockZ = -(citySizeNS / 2 - (nsIndex + 1) * blockSize)

    for weIndex, blueprintItem in enumerate(blueprintRow):
        blockX = weIndex * blockSize - citySizeWE / 2
        block = newGroup(city)
        outlineBlock = newGroup(cityOuline)
        block.addTranslate3d(Vec3D(blockX, 0.0, blockZ))
        outlineBlock.addTranslate3d(Vec3D(blockX, 0.0, blockZ))

        if isBuilding(blueprintItem):
            addExternalReference("building", "building", block)
            addExternalReference("buildingPad", "buildingpad",
                                 block, outlineBlock)
        elif isRoad(blueprintItem):
            addExternalReference("road", "road", block)
        else:
            addExternalReference("ground", "ground", block)

        if not isBuilding(blueprintItem):
            nwItem = getItem(blueprint, nsIndex - 1, weIndex - 1)
            nItem = getItem(blueprint, nsIndex - 1, weIndex)
            neItem = getItem(blueprint, nsIndex - 1, weIndex + 1)
            wItem = getItem(blueprint, nsIndex, weIndex - 1)
            eItem = getItem(blueprint, nsIndex, weIndex + 1)
            swItem = getItem(blueprint, nsIndex + 1, weIndex - 1)
            sItem = getItem(blueprint, nsIndex + 1, weIndex)
            seItem = getItem(blueprint, nsIndex + 1, weIndex + 1)

            if isRoad(nItem) and isRoad(blueprintItem) and isRoad(eItem) and\
               not isRoad(wItem) and not isRoad(sItem):
                addExternalReference("marking", "swmarking", block)
            if isRoad(wItem) and isRoad(blueprintItem) and isRoad(nItem) and\
               not isRoad(sItem) and not isRoad(eItem):
                addExternalReference("marking", "semarking", block)
            if isRoad(sItem) and isRoad(blueprintItem) and isRoad(wItem) and\
               not isRoad(eItem) and not isRoad(nItem):
                addExternalReference("marking", "nemarking", block)
            if isRoad(eItem) and isRoad(blueprintItem) and isRoad(sItem) and\
               not isRoad(nItem) and not isRoad(wItem):
                addExternalReference("marking", "nwmarking", block)

            if isRoad(wItem) and isRoad(blueprintItem) and isRoad(eItem) and\
               (not isRoad(nItem) or not isRoad(sItem)):
                addExternalReference("marking", "wemarking", block)
            if isRoad(nItem) and isRoad(blueprintItem) and isRoad(sItem) and\
               (not isRoad(wItem) or not isRoad(eItem)):
                addExternalReference("marking", "nsmarking", block)

            if wItem != blueprintItem and nItem != blueprintItem:
                addExternalReference("sidewalk", "nwexteriorsidewalk",
                                     block, outlineBlock)
            if eItem != blueprintItem and nItem != blueprintItem:
                addExternalReference("sidewalk", "neexteriorsidewalk",
                                     block, outlineBlock)
            if wItem != blueprintItem and sItem != blueprintItem:
                addExternalReference("sidewalk", "swexteriorsidewalk",
                                     block, outlineBlock)
            if eItem != blueprintItem and sItem != blueprintItem:
                addExternalReference("sidewalk", "seexteriorsidewalk",
                                     block, outlineBlock)

            if wItem == blueprintItem and nItem == blueprintItem and\
               nwItem != blueprintItem:
                addExternalReference("sidewalk", "nwinteriorsidewalk",
                                     block, outlineBlock)
            if eItem == blueprintItem and nItem == blueprintItem and\
               neItem != blueprintItem:
                addExternalReference("sidewalk", "neinteriorsidewalk",
                                     block, outlineBlock)
            if wItem == blueprintItem and sItem == blueprintItem and\
               swItem != blueprintItem:
                addExternalReference("sidewalk", "swinteriorsidewalk",
                                     block, outlineBlock)
            if eItem == blueprintItem and sItem == blueprintItem and\
               seItem != blueprintItem:
                addExternalReference("sidewalk", "seinteriorsidewalk",
                                     block, outlineBlock)

            if wItem != blueprintItem and nItem == blueprintItem:
                addExternalReference("sidewalk", "nwhalf1sidewalk",
                                     block, outlineBlock)
            if eItem != blueprintItem and nItem == blueprintItem:
                addExternalReference("sidewalk", "nehalf2sidewalk",
                                     block, outlineBlock)
            if wItem != blueprintItem and sItem == blueprintItem:
                addExternalReference("sidewalk", "swhalf2sidewalk",
                                     block, outlineBlock)
            if eItem != blueprintItem and sItem == blueprintItem:
                addExternalReference("sidewalk", "sehalf1sidewalk",
                                     block, outlineBlock)
            if wItem == blueprintItem and nItem != blueprintItem:
                addExternalReference("sidewalk", "nwhalf2sidewalk",
                                     block, outlineBlock)
            if eItem == blueprintItem and nItem != blueprintItem:
                addExternalReference("sidewalk", "nehalf1sidewalk",
                                     block, outlineBlock)
            if wItem == blueprintItem and sItem != blueprintItem:
                addExternalReference("sidewalk", "swhalf1sidewalk",
                                     block, outlineBlock)
            if eItem == blueprintItem and sItem != blueprintItem:
                addExternalReference("sidewalk", "sehalf2sidewalk",
                                     block, outlineBlock)

city.writeEgg("models/city.egg")
cityOuline.writeEgg("models/city_outline.egg")
