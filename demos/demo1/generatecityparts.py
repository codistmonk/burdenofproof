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

def setNormalAndTangentAndBinormal(polygon, tangent):
	polygon.recomputePolygonNormal()
	normal = Vec3D()
	polygon.calculateNormal(normal)
	binormal = normal.cross(tangent)

	for vertex in polygon.getVertices():
		uv = EggVertexUV(vertex.getUvObj(""))
		uv.setTangent(tangent)
		uv.setBinormal(binormal)
		vertex.setUvObj(uv)

def generateTexturedQuad(name, size, textureName, useTextureNormal = False, textureScale = 1.0):
	vertices = EggVertexPool(name + "Vertices")
	polygon = EggPolygon()
	v00 = polygon.addVertex(addEggVertex(vertices, 0, 0, 0, 0, 0))
	v10 = polygon.addVertex(addEggVertex(vertices, size, 0, 0, 1, 0))
	v11 = polygon.addVertex(addEggVertex(vertices, size, 0, -size, 1, 1))
	v01 = polygon.addVertex(addEggVertex(vertices, 0, 0, -size, 0, 1))

	setNormalAndTangentAndBinormal(polygon, Vec3D(1, 0, 0))

	polygon.addTexture(retrieveTexture(name, textureName, EggTexture.ETUnspecified, textureScale))

	if useTextureNormal:
		polygon.addTexture(retrieveTexture(name, textureName, EggTexture.ETNormal, textureScale))

	egg = EggData()
	egg.addChild(vertices)
	egg.addChild(polygon)
	egg.writeEgg("models/" + name + ".egg")

def generateBuildingPad(size):
	pass	

blockSize = 10.0
generateTexturedQuad("ground", blockSize, "grass", True, blockSize)
generateTexturedQuad("road", blockSize, "asphalt", True, blockSize)
generateTexturedQuad("building", blockSize - 2.0, "blue")

