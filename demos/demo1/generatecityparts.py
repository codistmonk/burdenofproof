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

def generateTexturedQuad(name, size, textureName, useTextureNormal = False, textureScale = 1.0):
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
	egg.addChild(polygon)
	egg.writeEgg("models/" + name + ".egg")

generateTexturedQuad("ground", 10.0, "grass", True, 10.0)
generateTexturedQuad("road", 10.0, "asphalt", True, 10.0)
generateTexturedQuad("building", 8.0, "blue")
