import sys
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.directnotify.DirectNotify import DirectNotify
from direct.task import Task

def clamp(value, minValue, maxValue):
	return min(max(minValue, value), maxValue)

def clampX(target, minX, maxX):
	target.setX(clamp(target.getX(), minX, maxX))

def clampY(target, minY, maxY):
	target.setY(clamp(target.getY(), minY, maxY))

def clampZ(target, minZ, maxZ):
	target.setZ(clamp(target.getZ(), minZ, maxZ))

class MyApp(ShowBase):

	def __init__(self):
		ShowBase.__init__(self)

		self.debug = DirectNotify().newCategory("Debug")

		self.setupModels()
		self.setupKeyboardControl()
		self.camera.setPos(0, 0, 2)
		self.setupMouseControl()

	def setupKeyboardControl(self):
		self.accept('escape', sys.exit)

	def setupMouseControl(self):
		base.disableMouse()

		# Set the current viewing target
		self.heading = 180
		self.pitch = 0
		self.mousex = 0
		self.mousey = 0
		self.last = 0
		self.mousebtn = [0,0,0]

		self.accept("mouse1", self.setMouseBtn, [0, 1])
		self.accept("mouse1-up", self.setMouseBtn, [0, 0])
		self.accept("mouse2", self.setMouseBtn, [1, 1])
		self.accept("mouse2-up", self.setMouseBtn, [1, 0])
		self.accept("mouse3", self.setMouseBtn, [2, 1])
		self.accept("mouse3-up", self.setMouseBtn, [2, 0])

		# Start the camera control task
		self.taskMgr.add(self.controlCamera, "camera-task")

	def setupModels(self):
		self.setupLights()
		self.loadSky()
		self.loadTerrain()
		self.loadBuildings()

	def setupLights(self):
		self.sunLight = self.render.attachNewNode(DirectionalLight('sunLight'))
		self.sunLight.setColor(Vec4(0.8, 0.8, 0.8, 1))
		self.sunLight.node().getLens().setFilmSize(128, 64)
		self.sunLight.node().getLens().setNearFar(20,2000)
		self.sunLight.setPos(60, 30, 50)
		self.sunLight.lookAt(0, 0, 0)
		self.render.setLight(self.sunLight)
#		self.sunLight.node().showFrustum()
		if (base.win.getGsg().getSupportsBasicShaders() != 0 and base.win.getGsg().getSupportsDepthTexture() != 0):
			self.sunLight.node().setShadowCaster(True, 256, 256)
			self.render.setShaderAuto()
		else:
			self.debug.warning("Shadows deactivated")

		self.ambientLight = self.render.attachNewNode(AmbientLight('ambientLight'))
		self.ambientLight.node().setColor(Vec4(0.2, 0.2, 0.2, 1))
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
			"PSOSH_",
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

	def setMouseBtn(self, btn, value):
		self.mousebtn[btn] = value

	def buildingInstanceNameAndPrototypeFromType(self, buildingType):
		return {
			'S' : ( None, None ),
			'P' : ( "Police-Building-Instance", self.policeBuildingPrototype ),
			'T' : ( "Tribunal-Instance", self.tribunalPrototype ),
			'O' : ( "Office-Building-Instance", self.officeBuildingPrototype ),
			'H' : ( "House-Instance", self.housePrototype ),
		}.get(buildingType, ( None, None ))
	
	def controlCamera(self, task):
		# figure out how much the mouse has moved (in pixels)
		md = self.win.getPointer(0)
		x = md.getX()
		y = md.getY()
		windowCenterX = self.win.getXSize() / 2
		windowCenterY = self.win.getYSize() / 2

		if self.win.movePointer(0, windowCenterX, windowCenterY):
			self.heading = self.heading - (x - windowCenterX) * 0.2
			self.pitch = clamp(self.pitch - (y - windowCenterY) * 0.2, -45, 45)

		self.camera.setHpr(self.heading, self.pitch, 0)

		elapsed = task.time - self.last

		if (self.last == 0):
			elapsed = 0

		if (self.mousebtn[0]):
			direction = self.camera.getMat().getRow3(1)
			self.camera.setPos(self.camera.getPos() + direction * elapsed*30)

		clampX(self.camera, -59, 59)
		clampY(self.camera, -59, 59)
		self.camera.setZ(2)

		self.last = task.time

		return Task.cont


app = MyApp()
app.run()
