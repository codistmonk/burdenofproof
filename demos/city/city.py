from panda3d.core import *

loadPrcFileData("", "prefer-parasite-buffer #f")

from direct.showbase.ShowBase import ShowBase
from direct.directnotify.DirectNotify import DirectNotify

class MyApp(ShowBase):

	def __init__(self):
		ShowBase.__init__(self)

		self.debug = DirectNotify().newCategory("Debug")

		self.loadModels()
		self.setCameraPos(0, 0, 2)

	def loadModels(self):
		self.setupLights()
		self.loadSky()
		self.loadTerrain()
		self.loadBuildings()

	def setupLights(self):
		sunLight = DirectionalLight('sunLight')
		sunLight.setColor(Vec4(1, 1, 1, 1))
#		sunLight.showFrustum()
		sunLight.getLens().setFilmSize(128, 64)
		sunLight.getLens().setNearFar(20,2000)
		sunLight.setShadowCaster(True, 256, 256)
		self.sunLight = self.render.attachNewNode(sunLight)
		self.sunLight.setPos(60, 30, 50)
		self.sunLight.lookAt(0, 0, 0)
		self.render.setLight(self.sunLight)
		self.render.setShaderAuto()

		ambientLight = AmbientLight('ambientLight')
		ambientLight.setColor(Vec4(0.1, 0.1, 0.1, 1))
		self.ambientLight = self.render.attachNewNode(ambientLight)
		self.render.setLight(self.ambientLight)

	def loadSky(self):
		self.sky = self.loader.loadModel("models/sky")
		self.sky.reparentTo(self.camera)
		self.sky.setScale(base.camLens.getNear() * 1.1)
		self.sky.setBin("background", 0)
		self.sky.setDepthWrite(False)
		self.sky.setCompass()
		self.sky.setLightOff()

	def loadTerrain(self):
		self.terrain = self.loader.loadModel("models/terrain")
		self.terrain.reparentTo(self.render)
		self.teapot = self.loader.loadModel('teapot')

	def loadBuildings(self):
		# Load building prototypes
		self.buildingPadPrototype = self.loader.loadModel("models/building_pad")
		self.policeBuildingPrototype = self.loader.loadModel("models/police_building")
		self.tribunalPrototype = self.loader.loadModel("models/tribunal")
		self.officeBuildingPrototype = self.loader.loadModel("models/office_building")
		self.housePrototype = self.loader.loadModel("models/house")

		self.buildCity()

	def buildCity(self):
		# Define city blueprint
		city = [
			"PSOSHS",
			"TSOSHH",
			"SSSSSS",
			"OOSOSH",
			"SSSSSH",
			"HHHSHH"
		]
		blockSize = 10
		cityWESize = len(city[0]) * blockSize
		cityNSSize = len(city) * blockSize

		# Create buildings from city blueprint
		for rowIndex, row in enumerate(city):
			for columnIndex, buildingType in enumerate(row):
				# Get building data from city blueprint
				buildingInstanceName, buildingPrototype = self.buildingInstanceNameAndPrototypeFromType(buildingType)

				if (not (buildingInstanceName is None or buildingPrototype is None)):
					# Compute building position
					buildingX, buildingY, buildingZ = columnIndex * blockSize - cityWESize / 2, cityNSSize / 2 - (rowIndex + 1) * blockSize, 0

					# Create building pad
					buildingPadInstance = render.attachNewNode("Building-Pad-Instance")
					buildingPadInstance.setPos(buildingX, buildingY, buildingZ)
					self.buildingPadPrototype.instanceTo(buildingPadInstance)

					# Create building
					buildingInstance = render.attachNewNode(buildingInstanceName)
					buildingInstance.setPos(buildingX, buildingY, buildingZ)
					buildingPrototype.instanceTo(buildingInstance)

	def setCameraPos(self, x, y, z):
		base.disableMouse()
		self.camera.setPos(x, y, z)
		mat = Mat4(self.camera.getMat())
		mat.invertInPlace()
		base.mouseInterfaceNode.setMat(mat)
		base.enableMouse()

	def buildingInstanceNameAndPrototypeFromType(self, buildingType):
		return {
			'S' : ( None, None ),
			'P' : ( "Police-Building-Instance", self.policeBuildingPrototype ),
			'T' : ( "Tribunal-Instance", self.tribunalPrototype ),
			'O' : ( "Office-Building-Instance", self.officeBuildingPrototype ),
			'H' : ( "House-Instance", self.housePrototype ),
		}.get(buildingType, ( None, None ))

app = MyApp()
app.run()
