import sys, os
from panda3d.core import *
from panda3d.egg import *
from utils import *

def retrieveTexture(textureName, textureFolderName, textureEnvType, textureScale):
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
		"textures/" + textureFolderName + "/" + textureFolderName + "_" + textureFileNameEnding + ".png")

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

def newPolygon(eggVertices, uvs, quarterTurns = 0):
	polygon = EggPolygon()

	for i in range(0, len(uvs), 2):
		u, v = uvs[i], uvs[i + 1]
		if quarterTurns == 1:
			x, y = 1.0 - v, u
		elif quarterTurns == 2:
			x, y = 1.0 - u, 1.0 - v
		elif quarterTurns == 3:
			x, y = v, 1.0 - u
		else:
			x, y = u, v
		polygon.addVertex(addEggVertex(eggVertices, x, y, 0.0, x, y))

	return polygon

def generateBuildingPad(size):
	name = "buildingpad"
	textureName = "pavers"
	textureScale = 10.0
	vertices = EggVertexPool(name + "Vertices")
	egg = EggData()
	group = EggGroup()
	group.setGroupType(EggGroup.GTInstance)
	egg.addChild(vertices)
	egg.addChild(group)
	uvs = [
		0.0, 0.0,
		0.9, 0.0,
		0.9, 0.1,
		0.0, 0.1
	]

	for quarterTurns in range(4):
		polygon = newPolygon(vertices, uvs, quarterTurns)
		polygon.addTexture(retrieveTexture(name, textureName, EggTexture.ETUnspecified, textureScale))
		polygon.addTexture(retrieveTexture(name, textureName, EggTexture.ETNormal, textureScale))
		group.addChild(polygon)

	group.addRotx(-90.0)
	group.addUniformScale(size)
	group.addTranslate3d(Vec3D(0.0, size / 10.0, 0.0))

	finishEgg(egg)
	egg.writeEgg("models/" + name + ".egg")

blockSize = 10.0
generateTexturedQuad("ground", blockSize, "grass", True, blockSize)
generateTexturedQuad("road", blockSize, "asphalt", True, blockSize)
generateTexturedQuad("building", blockSize - 2.0, "blue", translation = Vec3D(blockSize / 10.0, 0.0, -blockSize / 10.0))
generateBuildingPad(blockSize)
