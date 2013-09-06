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

def addData(writer, values):
	n = len(values)

	if n == 2:
		writer.addData2f(values[0], values[1])
	elif n == 3:
		writer.addData3f(values[0], values[1], values[2])
	elif n == 4:
		writer.addData4f(values[0], values[1], values[2], values[3])
	else:
		raise Exception("Invalid vector size: %d" % n)

def vec3(floats):
	return Vec3(floats[0], floats[1], floats[2])

def setOrbiterHeading(orbiter, heading, target, distanceFromTarget = None):
	if distanceFromTarget == None:
		distanceFromTarget = (orbiter.getPos() - target).length()

	orbiter.setH(heading)
	orbiter.setPos(target - orbiter.getMat().getRow3(1) * distanceFromTarget)

def newGroup(eggData):
	group = EggGroup()

	group.setGroupType(EggGroup.GTInstance)

	eggData.addChild(group)

	return group

def newEggVertex(eggVertexPool, x, y, z, uv = None, normal = None):
	vertex = EggVertex()

	vertex.setPos(Point3D(x, y, z))

	if not uv is None:
		vertex.setUv(uv)

	if not normal is None:
		vertex.setNormal(normal)

	eggVertexPool.addVertex(vertex)

	return vertex

def finishEgg(eggData, smoothingThresholdDegrees):
	eggData.recomputePolygonNormals()
	eggData.recomputeVertexNormals(smoothingThresholdDegrees)
	eggData.recomputeTangentBinormalAuto()
	eggData.removeUnusedVertices(True)
