import sys, os
from math import *
from panda3d.core import *
from panda3d.egg import *
from utils import *

def retrieveTexture(textureName, textureFolderName, textureEnvType = EggTexture.ETUnspecified, textureScale = 1.0, textureFormat = "png"):
	if EggTexture.ETUnspecified == textureEnvType:
		textureNameEnding = "Diffuse"
		textureFileNameEnding = "diffuse"
	elif EggTexture.ETNormal == textureEnvType:
		textureNameEnding = "Normal"
		textureFileNameEnding = "normal"
	else:
		raise Exception("Unhandled texture env type: " + str(textureEnvType))

	texture = EggTexture(
		textureName + "Texture" + textureNameEnding,
		"textures/" + textureFolderName + "/" + textureFolderName + "_" + textureFileNameEnding + "." + textureFormat)

	texture.setEnvType(textureEnvType)

	texture.setMinfilter(EggTexture.FTLinearMipmapLinear)

	if textureScale == 1.0:
		texture.setWrapMode(EggTexture.WMClamp)
	else:
		texture.setWrapMode(EggTexture.WMRepeat)
		texture.addScale2d(textureScale)

	return texture

def finishEgg(eggData):
	eggData.recomputeVertexNormals(0.0)
	eggData.recomputeTangentBinormalAuto()
	eggData.removeUnusedVertices(True)

def xyFromUv(u, v, quarterTurns):
	if quarterTurns == 1:
		return 1.0 - v, u
	elif quarterTurns == 2:
		return 1.0 - u, 1.0 - v
	elif quarterTurns == 3:
		return v, 1.0 - u
	else:
		return u, v

def generateTexturedQuad(name, size, textureName, useTextureNormal = False, textureScale = 1.0, scale = None, translation = None, quarterTurns = 0):
	vertices = EggVertexPool(name + "Vertices")
	polygon = EggPolygon()

	x, y = xyFromUv(0, 0, quarterTurns)
	polygon.addVertex(addEggVertex(vertices, x * size, 0, - y * size, 0, 0))
	x, y = xyFromUv(1, 0, quarterTurns)
	polygon.addVertex(addEggVertex(vertices, x * size, 0, - y * size, 1, 0))
	x, y = xyFromUv(1, 1, quarterTurns)
	polygon.addVertex(addEggVertex(vertices, x * size, 0, - y * size, 1, 1))
	x, y = xyFromUv(0, 1, quarterTurns)
	polygon.addVertex(addEggVertex(vertices, x * size, 0, - y * size, 0, 1))

	polygon.addTexture(retrieveTexture(name, textureName, EggTexture.ETUnspecified, textureScale))

	if useTextureNormal:
		polygon.addTexture(retrieveTexture(name, textureName, EggTexture.ETNormal, textureScale))

	egg = EggData()

	egg.addChild(vertices)

	group = EggGroup()
	egg.addChild(group)
	group.setGroupType(EggGroup.GTInstance)
	group.addChild(polygon)

	if not scale is None:
		group.addScale3d(scale)
	if not translation is None:
		group.addTranslate3d(translation)

	finishEgg(egg)
	egg.writeEgg("models/" + name + ".egg")

def newFlatPolygon(eggVertices, uvs, quarterTurns = 0):
	polygon = EggPolygon()

	for i in range(0, len(uvs), 2):
		u, v = uvs[i], uvs[i + 1]
		x, y = xyFromUv(u, v, quarterTurns)
		polygon.addVertex(addEggVertex(eggVertices, x, y, 0.0, x, y))

	return polygon

def newEggAndGroup():
	egg = EggData()
	group = EggGroup()

	egg.addChild(group)
	group.setGroupType(EggGroup.GTInstance)

	return egg, group

def generateBuildingPad(size):
	name = "buildingpad"
	textureName = "pavers"
	textureScale = size
	vertices = EggVertexPool(name + "Vertices")
	egg, group = newEggAndGroup()
	egg.addChild(vertices)
	uvs = [
		0.0, 0.0,
		0.9, 0.0,
		0.9, 0.1,
		0.0, 0.1
	]

	for quarterTurns in range(4):
		polygon = newFlatPolygon(vertices, uvs, quarterTurns)
		polygon.addTexture(retrieveTexture(name, textureName, EggTexture.ETUnspecified, textureScale))
		polygon.addTexture(retrieveTexture(name, textureName, EggTexture.ETNormal, textureScale))
		group.addChild(polygon)

	group.addRotx(-90.0)
	group.addUniformScale(size)
	group.addTranslate3d(Vec3D(0.0, 0.1, 0.0))

	finishEgg(egg)
	egg.writeEgg("models/" + name + ".egg")

def arc(centerX, centerY, radius, angleBegin, angleEnd, angleCount, includeEnd = False, rounding = 4):
	uvs = []
	angleExtent = angleEnd - angleBegin
	n = angleCount + (1 if includeEnd else 0)

	for i in range(n):
		angle = angleBegin + i * angleExtent / angleCount
		uvs.append(round(centerX + radius * cos(angle), rounding))
		uvs.append(round(centerY + radius * sin(angle), rounding))

	return uvs

def reverseUvs(uvs):
	result = []

	for i in range(len(uvs) - 2, -1, -2):
		result.append(uvs[i])
		result.append(uvs[i + 1])

	return result

def newCurbTop(eggVertices, curbUvs, quarterTurns = 0):
	result = []
	polygon = EggPolygon()
	walksideUvs = curbUvs[0]
	roadsideUvs = curbUvs[1]
	n = len(roadsideUvs)

	for i in range(0, n - 2, 2):
		x1, y1 = xyFromUv(roadsideUvs[i], roadsideUvs[i + 1], quarterTurns)
		x2, y2 = xyFromUv(roadsideUvs[i + 2], roadsideUvs[i + 3], quarterTurns)
		x3, y3 = xyFromUv(walksideUvs[i + 2], walksideUvs[i + 3], quarterTurns)
		x4, y4 = xyFromUv(walksideUvs[i], walksideUvs[i + 1], quarterTurns)
		polygon = EggPolygon()

		polygon.addVertex(addEggVertex(eggVertices, x1, y1, 0.0, 0.01, i / (n - 2.0)))
		polygon.addVertex(addEggVertex(eggVertices, x2, y2, 0.0, 0.01, (i + 2) / (n - 2.0)))
		polygon.addVertex(addEggVertex(eggVertices, x3, y3, 0.0, 0.00, (i + 2) / (n - 2.0)))
		polygon.addVertex(addEggVertex(eggVertices, x4, y4, 0.0, 0.00, i / (n - 2.0)))

		result.append(polygon)

	return result

def newCurbSide(eggVertices, curbUvs, quarterTurns = 0):
	result = []
	roadsideUvs = curbUvs[1]
	n = len(roadsideUvs)

	for i in range(0, n - 2, 2):
		x1, y1 = xyFromUv(roadsideUvs[i], roadsideUvs[i + 1], quarterTurns)
		x2, y2 = xyFromUv(roadsideUvs[i + 2], roadsideUvs[i + 3], quarterTurns)
		polygon = EggPolygon()

		polygon.addVertex(addEggVertex(eggVertices, x1, y1, -0.01, 0.02, i / (n - 2.0)))
		polygon.addVertex(addEggVertex(eggVertices, x2, y2, -0.01, 0.02, (i + 2) / (n - 2.0)))
		polygon.addVertex(addEggVertex(eggVertices, x2, y2, 0.0, 0.01, (i + 2) / (n - 2.0)))
		polygon.addVertex(addEggVertex(eggVertices, x1, y1, 0.0, 0.01, i / (n - 2.0)))

		result.append(polygon)

	return result

def generateSidewalks(sidewalkType, size, walkUvs, curbUvs):
	textureScale = size
	textureName = "pavers"

	for quarterTurns, namePrefix in enumerate(["sw", "se", "ne", "nw"]):
		name = namePrefix + sidewalkType + "sidewalk"
		egg, group = newEggAndGroup()
		vertices = EggVertexPool(name + "Vertices")
		egg.addChild(vertices)

		polygon = newFlatPolygon(vertices, walkUvs, quarterTurns)
		polygon.addTexture(retrieveTexture(name, textureName, EggTexture.ETUnspecified, textureScale))
		polygon.addTexture(retrieveTexture(name, textureName, EggTexture.ETNormal, textureScale))
		group.addChild(polygon)

		for polygon in newCurbTop(vertices, curbUvs, quarterTurns):
			polygon.addTexture(retrieveTexture(name, "cement", EggTexture.ETUnspecified, textureScale, textureFormat = "jpg"))
			group.addChild(polygon)

		for polygon in newCurbSide(vertices, curbUvs, quarterTurns):
			polygon.addTexture(retrieveTexture(name, "cement", EggTexture.ETUnspecified, textureScale, textureFormat = "jpg"))
			group.addChild(polygon)

		group.addRotx(-90.0)
		group.addUniformScale(size)
		group.addTranslate3d(Vec3D(0.0, 0.1, 0.0))

		finishEgg(egg)
		egg.writeEgg("models/" + name + ".egg")

def generateExteriorSidewalks(size, smoothness = 16):
	connectUvs = [
		0.09, 0.5,
		0.00, 0.5,
		0.00, 0.0,
		0.50, 0.0,
	] + arc(0.5, 0.5, 0.41, -pi / 2.0, -pi, smoothness)
	curbUvs = [
		arc(0.5, 0.5, 0.41, -pi / 2.0, -pi, smoothness, includeEnd = True),
		arc(0.5, 0.5, 0.40, -pi / 2.0, -pi, smoothness, includeEnd = True),
	]

	generateSidewalks("exterior", size, connectUvs, curbUvs)

def generateInteriorSidewalks(size, smoothness = 16):
	connectUvs = [
		0.0, 0.09,
		0.0, 0.00,
	] + arc(0.0, 0.0, 0.09, 0.0, pi / 2.0, smoothness)
	curbUvs = [
		arc(0.0, 0.0, 0.09, 0.0, pi / 2.0, smoothness, includeEnd = True),
		arc(0.0, 0.0, 0.10, 0.0, pi / 2.0, smoothness, includeEnd = True)
	]

	generateSidewalks("interior", size, connectUvs, curbUvs)

def generateHalf1Sidewalks(size):
	connectUvs = [
		0.0, 0.09,
		0.0, 0.00,
		0.5, 0.00,
		0.5, 0.09
	]
	curbUvs = [[
		0.5, 0.09,
		0.0, 0.09
	],[
		0.5, 0.10,
		0.0, 0.10
	]]

	generateSidewalks("half1", size, connectUvs, curbUvs)

def generateHalf2Sidewalks(size):
	connectUvs = [
		0.09, 0.5,
		0.00, 0.5,
		0.00, 0.0,
		0.09, 0.0
	]
	curbUvs = [[
		0.09, 0.0,
		0.09, 0.5,
	],[
		0.10, 0.0,
		0.10, 0.5,
	]]

	generateSidewalks("half2", size, connectUvs, curbUvs)

def newMarking(eggVertices):
	return newFlatPolygon(eggVertices, [
		0.0, 0.0,
		1.0, 0.0,
		1.0, 1.0,
		0.0, 1.0
	])

def frange(begin, end, n, includeBegin = True, includeEnd = False):
	result = []
	extent = end - begin

	for i in range(0 if includeBegin else 1, n + (1 if includeEnd else 0)):
		result.append(begin + i * extent / n)
		pass

	return result

def generateCurvedRoadMarkings(size, smoothness = 5):
	overflowAngle = 10.0

	for quarterTurns, namePrefix in enumerate(["sw", "se", "ne", "nw"]):
		name = namePrefix + "marking"
		egg, group = newEggAndGroup()
		vertices = EggVertexPool(name + "Vertices")
		egg.addChild(vertices)
		centerX, centerY = xyFromUv(1.0, 1.0, quarterTurns)

		for angle in frange(quarterTurns * 90.0 - 180.0 - overflowAngle, quarterTurns * 90.0 - 90.0 + overflowAngle, smoothness, False, False):
			markingGroup = newGroup(group)
			markingPolygon = newMarking(vertices)
			markingPolygon.addTexture(retrieveTexture(name, "curvemarking"))
			markingGroup.addChild(markingPolygon)
			markingGroup.addTranslate3d(Vec3D(-0.5, -0.5, 0.0))
			markingGroup.addScale3d(Vec3D(1.0 / 5.0, 1.0 / 8.0 / 5.0, 1.0))
			markingGroup.addRotz(angle + 90.0)
			markingGroup.addTranslate3d(Vec3D(centerX + 0.5 * cos(deg2Rad(angle)), centerY + 0.5 * sin(deg2Rad(angle)), 0.0))

		group.addRotx(-90.0)
		group.addUniformScale(size)
		group.addTranslate3d(Vec3D(0.0, 0.001, 0.0))

		finishEgg(egg)
		egg.writeEgg("models/" + name + ".egg")


blockSize = 10.0
generateTexturedQuad("ground", blockSize, "grass", True, blockSize)
generateTexturedQuad("road", blockSize, "asphalt", True, blockSize)
generateTexturedQuad("building", blockSize - 2.0, "blue",
	translation = Vec3D(blockSize / 10.0, 0.0, -blockSize / 10.0))
generateBuildingPad(blockSize)
generateExteriorSidewalks(blockSize)
generateInteriorSidewalks(blockSize)
generateHalf1Sidewalks(blockSize)
generateHalf2Sidewalks(blockSize)
generateTexturedQuad("wemarking", blockSize, "marking",
	scale = Vec3D(1.0, 1.0, 1.0 / 40.0), textureScale = 5.0, translation = Vec3D(0.0, 0.001, -(0.5 - 1.0 / 40.0 / 2.0) * blockSize))
generateTexturedQuad("nsmarking", blockSize, "marking",
	quarterTurns = 1, scale = Vec3D(1.0 / 40.0, 1.0, 1.0), textureScale = 5.0, translation = Vec3D((0.5 - 1.0 / 40.0 / 2.0) * blockSize, 0.001, 0.0))
generateCurvedRoadMarkings(blockSize)
