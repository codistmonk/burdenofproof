import sys, os
from panda3d.core import *
from panda3d.egg import *

def clamp(value, minValue, maxValue):
	return min(max(minValue, value), maxValue)

def clampX(target, minX, maxX):
	target.setX(clamp(target.getX(), minX, maxX))

def clampY(target, minY, maxY):
	target.setY(clamp(target.getY(), minY, maxY))

def clampZ(target, minZ, maxZ):
	target.setZ(clamp(target.getZ(), minZ, maxZ))

def addEggVertex(eggVertexPool, x, y, z, u = 0, v = 0, useUv = True):
	vertex = EggVertex()

	vertex.setPos(Point3D(x, y, z))

	if useUv:
		vertex.setUv(Point2D(u, v))

	eggVertexPool.addVertex(vertex)

	return vertex

def newGroup(eggData):
	group = EggGroup()

	group.setGroupType(EggGroup.GTInstance)

	eggData.addChild(group)

	return group

def finishEgg(eggData):
	eggData.recomputeVertexNormals(0.0)
	eggData.recomputeTangentBinormalAuto()
	eggData.removeUnusedVertices(True)

scriptPath = os.path.dirname(sys.argv[0]).replace("\\", "/")
