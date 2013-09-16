import sys
import os
from math import *
from panda3d.core import *
from panda3d.egg import *
from utils import *
from bopmodel import *


def isRoad(blockType):
    return CityBlock.ROAD == blockType


def isGround(blockType):
    return CityBlock.GROUND == blockType


def isBuilding(blockType):
    return not isRoad(blockType) and not isGround(blockType)


def addExternalReference(nodeName, fileName, blockGroup,
                         outlineBlockGroup=None):
    blockGroup.addChild(EggExternalReference(nodeName, fileName))

    if not outlineBlockGroup is None:
        outlineBlockGroup.addChild(EggExternalReference(
            nodeName, fileName + "_outline"))


def vec3d(v):
    return Vec3D(v.getX(), v.getY(), v.getZ())


blueprintPath = os.path.join(scriptPath, "data", "cityblueprint.txt")
modelsPath = os.path.join(scriptPath, "data", "models")
city = City(blueprintPath)
cityEgg = EggData()
cityOulineEgg = EggData()

for nsIndex in range(city.getBlockCountNS()):
    for weIndex in range(city.getBlockCountWE()):
        block = city.getBlock(nsIndex, weIndex)
        blockType = block.getType()
        blockPosition = vec3d(block.getPosition())
        blockGroup = newGroup(cityEgg)
        outlineBlockGroup = newGroup(cityOulineEgg)
        blockGroup.addTranslate3d(blockPosition)
        outlineBlockGroup.addTranslate3d(blockPosition)

        if isBuilding(blockType):
            addExternalReference("building", "building", blockGroup)
            addExternalReference("buildingPad", "buildingpad",
                                 blockGroup, outlineBlockGroup)
        elif isRoad(blockType):
            addExternalReference("road", "road", blockGroup)
        else:
            addExternalReference("ground", "ground", blockGroup)

        if not isBuilding(blockType):
            nwBlock = city.getBlock(nsIndex - 1, weIndex - 1).getType()
            nBlock = city.getBlock(nsIndex - 1, weIndex).getType()
            neBlock = city.getBlock(nsIndex - 1, weIndex + 1).getType()
            wBlock = city.getBlock(nsIndex, weIndex - 1).getType()
            eBlock = city.getBlock(nsIndex, weIndex + 1).getType()
            swBlock = city.getBlock(nsIndex + 1, weIndex - 1).getType()
            sBlock = city.getBlock(nsIndex + 1, weIndex).getType()
            seBlock = city.getBlock(nsIndex + 1, weIndex + 1).getType()

            if isRoad(nBlock) and isRoad(blockType) and isRoad(eBlock) and\
               not isRoad(wBlock) and not isRoad(sBlock):
                addExternalReference("marking", "swmarking", blockGroup)
            if isRoad(wBlock) and isRoad(blockType) and isRoad(nBlock) and\
               not isRoad(sBlock) and not isRoad(eBlock):
                addExternalReference("marking", "semarking", blockGroup)
            if isRoad(sBlock) and isRoad(blockType) and isRoad(wBlock) and\
               not isRoad(eBlock) and not isRoad(nBlock):
                addExternalReference("marking", "nemarking", blockGroup)
            if isRoad(eBlock) and isRoad(blockType) and isRoad(sBlock) and\
               not isRoad(nBlock) and not isRoad(wBlock):
                addExternalReference("marking", "nwmarking", blockGroup)

            if isRoad(wBlock) and isRoad(blockType) and isRoad(eBlock) and\
               (not isRoad(nBlock) or not isRoad(sBlock)):
                addExternalReference("marking", "wemarking", blockGroup)
            if isRoad(nBlock) and isRoad(blockType) and isRoad(sBlock) and\
               (not isRoad(wBlock) or not isRoad(eBlock)):
                addExternalReference("marking", "nsmarking", blockGroup)

            if wBlock != blockType and nBlock != blockType:
                addExternalReference("sidewalk", "nwexteriorsidewalk",
                                     blockGroup, outlineBlockGroup)
            if eBlock != blockType and nBlock != blockType:
                addExternalReference("sidewalk", "neexteriorsidewalk",
                                     blockGroup, outlineBlockGroup)
            if wBlock != blockType and sBlock != blockType:
                addExternalReference("sidewalk", "swexteriorsidewalk",
                                     blockGroup, outlineBlockGroup)
            if eBlock != blockType and sBlock != blockType:
                addExternalReference("sidewalk", "seexteriorsidewalk",
                                     blockGroup, outlineBlockGroup)

            if wBlock == blockType and nBlock == blockType and\
               nwBlock != blockType:
                addExternalReference("sidewalk", "nwinteriorsidewalk",
                                     blockGroup, outlineBlockGroup)
            if eBlock == blockType and nBlock == blockType and\
               neBlock != blockType:
                addExternalReference("sidewalk", "neinteriorsidewalk",
                                     blockGroup, outlineBlockGroup)
            if wBlock == blockType and sBlock == blockType and\
               swBlock != blockType:
                addExternalReference("sidewalk", "swinteriorsidewalk",
                                     blockGroup, outlineBlockGroup)
            if eBlock == blockType and sBlock == blockType and\
               seBlock != blockType:
                addExternalReference("sidewalk", "seinteriorsidewalk",
                                     blockGroup, outlineBlockGroup)

            if wBlock != blockType and nBlock == blockType:
                addExternalReference("sidewalk", "nwhalf1sidewalk",
                                     blockGroup, outlineBlockGroup)
            if eBlock != blockType and nBlock == blockType:
                addExternalReference("sidewalk", "nehalf2sidewalk",
                                     blockGroup, outlineBlockGroup)
            if wBlock != blockType and sBlock == blockType:
                addExternalReference("sidewalk", "swhalf2sidewalk",
                                     blockGroup, outlineBlockGroup)
            if eBlock != blockType and sBlock == blockType:
                addExternalReference("sidewalk", "sehalf1sidewalk",
                                     blockGroup, outlineBlockGroup)
            if wBlock == blockType and nBlock != blockType:
                addExternalReference("sidewalk", "nwhalf2sidewalk",
                                     blockGroup, outlineBlockGroup)
            if eBlock == blockType and nBlock != blockType:
                addExternalReference("sidewalk", "nehalf1sidewalk",
                                     blockGroup, outlineBlockGroup)
            if wBlock == blockType and sBlock != blockType:
                addExternalReference("sidewalk", "swhalf1sidewalk",
                                     blockGroup, outlineBlockGroup)
            if eBlock == blockType and sBlock != blockType:
                addExternalReference("sidewalk", "sehalf2sidewalk",
                                     blockGroup, outlineBlockGroup)

ensureDirectory(modelsPath)
cityEgg.writeEgg(os.path.join(modelsPath, "city.egg"))
cityOulineEgg.writeEgg(os.path.join(modelsPath, "city_outline.egg"))
