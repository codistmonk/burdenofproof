import sys, os
from math import *
from panda3d.core import *
from panda3d.egg import *
from utils import *

def retrieveTexture(textureName, textureFolderName, textureEnvType, textureScale, textureFormat = "png"):
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
		texture.addUniformScale(textureScale)

	return texture

def finishEgg(eggData):
	eggData.recomputeVertexNormals(0.0)
	eggData.recomputeTangentBinormalAuto()
	eggData.removeUnusedVertices(True)

def generateTexturedQuad(name, size, textureName, useTextureNormal = False, textureScale = 1.0, translation = None):
	vertices = EggVertexPool(name + "Vertices")
	polygon = EggPolygon()

	polygon.addVertex(addEggVertex(vertices, 0, 0, 0, 0, 0))
	polygon.addVertex(addEggVertex(vertices, size, 0, 0, 1, 0))
	polygon.addVertex(addEggVertex(vertices, size, 0, -size, 1, 1))
	polygon.addVertex(addEggVertex(vertices, 0, 0, -size, 0, 1))

	polygon.addTexture(retrieveTexture(name, textureName, EggTexture.ETUnspecified, textureScale))

	if useTextureNormal:
		polygon.addTexture(retrieveTexture(name, textureName, EggTexture.ETNormal, textureScale))

	egg = EggData()

	egg.addChild(vertices)

	if translation is None:
		egg.addChild(polygon)
	else:
		group = EggGroup()
		egg.addChild(group)
		group.setGroupType(EggGroup.GTInstance)
		group.addChild(polygon)
		group.addTranslate3d(translation)

	finishEgg(egg)
	egg.writeEgg("models/" + name + ".egg")

def xyFromUv(u, v, quarterTurns):
	if quarterTurns == 1:
		return 1.0 - v, u
	elif quarterTurns == 2:
		return 1.0 - u, 1.0 - v
	elif quarterTurns == 3:
		return v, 1.0 - u
	else:
		return u, v

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

	for i in range(len(uvs) - 2, -2, -2):
		result.append(uvs[i])
		result.append(uvs[i + 1])

	return result

def newCurbTop(eggVertices, curbUvs, quarterTurns = 0):
	polygon = EggPolygon()
	walksideUvs = curbUvs[0]
	roadsideUvs = curbUvs[1]
	n = len(walksideUvs)

	for i in range(0, n, 2):
		u, v = roadsideUvs[i], roadsideUvs[i + 1]
		x, y = xyFromUv(u, v, quarterTurns)
		polygon.addVertex(addEggVertex(eggVertices, x, y, 0.0, 0.01, i / (n - 1.0)))

	for i in range(n - 2, -2, -2):
		u, v = walksideUvs[i], walksideUvs[i + 1]
		x, y = xyFromUv(u, v, quarterTurns)
		polygon.addVertex(addEggVertex(eggVertices, x, y, 0.0, 0.0, i / (n - 1.0)))

	return polygon

def generateSidewalks(sidewalkType, size, walkUvs, curbUvs):
	textureScale = size
	textureName = "pavers"
	curbTopUvs = reverseUvs(curbUvs[0]) + curbUvs[1]

	print sidewalkType, curbTopUvs

	for quarterTurns, namePrefix in enumerate(["sw", "se", "ne", "nw"]):
		name = namePrefix + sidewalkType + "sidewalk"
		egg, group = newEggAndGroup()
		vertices = EggVertexPool(name + "Vertices")
		egg.addChild(vertices)
		polygon = newFlatPolygon(vertices, walkUvs, quarterTurns)
		polygon.addTexture(retrieveTexture(name, textureName, EggTexture.ETUnspecified, textureScale))
		polygon.addTexture(retrieveTexture(name, textureName, EggTexture.ETNormal, textureScale))
		group.addChild(polygon)
		polygon = newCurbTop(vertices, curbUvs, quarterTurns)
		polygon.addTexture(retrieveTexture(name, "cement", EggTexture.ETUnspecified, textureScale, textureFormat = "jpg"))
		group.addChild(polygon)

		group.addRotx(-90.0)
		group.addUniformScale(size)
		group.addTranslate3d(Vec3D(0.0, 0.1, 0.0))

		finishEgg(egg)
		egg.writeEgg("models/" + name + ".egg")

def generateExteriorSidewalks(size, smoothness = 16):
	connectUvs = [
		0.1, 0.5,
		0.0, 0.5,
		0.0, 0.0,
		0.5, 0.0,
	] + arc(0.5, 0.5, 0.41, -pi / 2.0, -pi, smoothness)
	curbUvs = [
		arc(0.5, 0.5, 0.41, -pi / 2.0, -pi, smoothness, includeEnd = True),
		arc(0.5, 0.5, 0.40, -pi / 2.0, -pi, smoothness, includeEnd = True),
	]

	generateSidewalks("exterior", size, connectUvs, curbUvs)

def generateInteriorSidewalks(size, smoothness = 16):
	connectUvs = [
		0.0, 0.1,
		0.0, 0.0,
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

blockSize = 10.0
generateTexturedQuad("ground", blockSize, "grass", True, blockSize)
generateTexturedQuad("road", blockSize, "asphalt", True, blockSize)
generateTexturedQuad("building", blockSize - 2.0, "blue", translation = Vec3D(blockSize / 10.0, 0.0, -blockSize / 10.0))
generateBuildingPad(blockSize)
generateExteriorSidewalks(blockSize)
generateInteriorSidewalks(blockSize)
generateHalf1Sidewalks(blockSize)
generateHalf2Sidewalks(blockSize)
