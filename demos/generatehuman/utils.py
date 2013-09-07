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

def newEggVertex(eggVertexPool, xyz, uv = None, normal = None):
	vertex = EggVertex()

	vertex.setPos(Point3D(xyz[0], xyz[1], xyz[2]))

	if not uv is None:
		vertex.setUv(Point2D(uv[0], uv[1]))

	if not normal is None:
		vertex.setNormal(Point3D(normal[0], normal[1], normal[2]))

	eggVertexPool.addVertex(vertex)

	return vertex

def finishEgg(eggData, smoothingThresholdDegrees):
	eggData.recomputePolygonNormals()
	eggData.recomputeVertexNormals(smoothingThresholdDegrees)
	eggData.recomputeTangentBinormalAuto()
	eggData.removeUnusedVertices(True)
