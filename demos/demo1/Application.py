import sys
from panda3d.core import *
from panda3d.egg import *
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from bop import *
from orbitalcameracontroller import *

def addEggVertex(eggVertexPool, x, y, z):
	vertex = EggVertex()

	vertex.setPos(Point3D(x, y, z))

	eggVertexPool.addVertex(vertex)

	return vertex

class Application(ShowBase):

	def __init__(self):
		ShowBase.__init__(self)

		self.game = Game()

		self.setupModels()
		self.setupLighting()
		self.setupKeyboard()
		self.cameraController = OrbitalCameraController(self)
		self.camera.setHpr(10, -40, 0)
		self.cameraController.scaleDistanceFromTarget(3)

	def setupModels(self):
		self.setupCity()

	def setupCity(self):
		blueprint = self.game.getCityBlueprint()
		blockSize = 10
		citySizeNS = blueprint.getSizeNS() * blockSize
		citySizeWE = blueprint.getSizeWE() * blockSize
		roadMaterial = EggMaterial("roadMaterial")
		roadMaterial.setDiff(Vec4(1, 0, 0, 1))
		groundMaterial = EggMaterial("groundMaterial")
		groundMaterial.setDiff(Vec4(0, 1, 0, 1))
		buildingMaterial = EggMaterial("buildingMaterial")
		buildingMaterial.setDiff(Vec4(0, 0, 1, 1))
		cityVertices = EggVertexPool("cityVertices")
		cityEgg = EggData()
		cityEgg.addChild(roadMaterial)
		cityEgg.addChild(groundMaterial)
		cityEgg.addChild(buildingMaterial)
		cityEgg.addChild(cityVertices)

		print "citySize:", citySizeNS, citySizeWE

		for nsIndex in range(blueprint.getSizeNS()):
			blockZ = -(citySizeNS / 2 - (nsIndex + 1) * blockSize)
			for weIndex in range(blueprint.getSizeWE()):
				blockX = weIndex * blockSize - citySizeWE / 2
				blockType = blueprint.getCell(nsIndex, weIndex)
				blockPolygon = EggPolygon()
				blockPolygon.addVertex(addEggVertex(cityVertices, blockX, 0, blockZ))
				blockPolygon.addVertex(addEggVertex(cityVertices, blockX + blockSize, 0, blockZ))
				blockPolygon.addVertex(addEggVertex(cityVertices, blockX + blockSize, 0, blockZ - blockSize))
				blockPolygon.addVertex(addEggVertex(cityVertices, blockX, 0, blockZ - blockSize))
				if CityCell.ROAD == blockType:
					blockPolygon.setMaterial(roadMaterial)
				elif CityCell.HOUSE == blockType or CityCell.POLICE_BUILDING == blockType or CityCell.OFFICE_BUILDING == blockType:
					blockPolygon.setMaterial(buildingMaterial)
				else:
					blockPolygon.setMaterial(groundMaterial)
				cityEgg.addChild(blockPolygon)

		cityEgg.writeEgg("test.egg")

		self.city = self.loader.loadModel("../test.egg")
		self.city.reparentTo(self.render)

	def setupLighting(self):
		self.ambientLight = self.render.attachNewNode(AmbientLight("ambientLight"))
		self.ambientLight.node().setColor(Vec4(1, 1, 1, 1))
		self.render.setLight(self.ambientLight)

	def setupKeyboard(self):
		self.accept("escape", sys.exit)

loadPrcFile("myconfig.prc")

Application().run()
