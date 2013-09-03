import sys
from math import *
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.directnotify.DirectNotify import DirectNotify
from direct.filter.CommonFilters import CommonFilters
from direct.fsm.FSM import FSM
from direct.interval.IntervalGlobal import *
from direct.task import Task

from phonestate import *
from utils import *

class MyApp(ShowBase):

	def __init__(self):
		ShowBase.__init__(self)

		self.useAdvancedVisualEffects = ConfigVariableBool("use-advanced-visual-effects", True)

		self.debug = DirectNotify().newCategory("Debug")

		self.phoneState = PhoneState(self)
		self.setupFilters()
		self.setupModels()
		self.setupKeyboardControl()
		self.camera.setPos(0, 0, 2)
		self.setupMouseControl()
		self.phoneState.request("Hidden")

	def setupFilters(self):
		if (self.useAdvancedVisualEffects):
			self.filters = CommonFilters(self.win, self.cam)
			self.filters.setBloom()

	def setupKeyboardControl(self):
		self.accept("escape", sys.exit)

	def setupMouseControl(self):
		self.disableMouse()

		self.mousex = 0
		self.mousey = 0
		self.last = 0
		self.mousebtn = [0,0,0]

		self.accept("mouse1", self.setMouseBtn, [0, 1])
		self.accept("mouse1-up", self.setMouseBtn, [0, 0])

		self.taskMgr.add(self.controlCamera, "cameraTask")

	def setupModels(self):
		self.setupLights()
		self.loadSky()
		self.loadTerrain()
		self.setupBuildings()
		self.phoneState.setupPhone()

	def setupLights(self):
		self.sunLight = self.render.attachNewNode(DirectionalLight("sunLight"))
		self.sunLight.setColor(Vec4(0.8, 0.8, 0.8, 1))
		self.sunLight.node().getLens().setFilmSize(128, 64)
		self.sunLight.node().getLens().setNearFar(20,2000)
		self.sunLight.setPos(60, 30, 50)
		self.sunLight.lookAt(0, 0, 0)
		self.render.setLight(self.sunLight)
#		self.sunLight.node().showFrustum()
		if (self.useAdvancedVisualEffects and base.win.getGsg().getSupportsBasicShaders() != 0 and base.win.getGsg().getSupportsDepthTexture() != 0):
			self.sunLight.node().setShadowCaster(True, 256, 256)
			self.render.setShaderAuto()

		self.ambientLight = self.render.attachNewNode(AmbientLight("ambientLight"))
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
		self.teapot = self.loader.loadModel("teapot")

	def setupBuildings(self):
		# Load building prototypes
		self.buildingPadPrototype = self.loader.loadModel("models/building_pad")
		self.policeBuildingPrototype = self.loader.loadModel("models/police_building")
		self.tribunalPrototype = self.loader.loadModel("models/tribunal")
		self.officeBuildingPrototype = self.loader.loadModel("models/office_building")
		self.housePrototype = self.loader.loadModel("models/House/CasaSimples")
		self.housePrototype.setPos(5, 5, 2.1)

		self.buildCity()

	def buildCity(self):
		# Define city blueprint
		city = [
			"PSOSHS_",
			"SSSSSSS",
			"OSHHHHH",
			"_SSSSSS",
			"_SHHHHH",
			"_SSSSSS",
			"_SHHHHH",
			"_SSSSSS",
			"_SHHHHH"
		]
		blockSize = 10
		cityWESize = len(city[0]) * blockSize
		cityNSSize = len(city) * blockSize
		self.maxX = cityWESize / 2.0
		self.maxY = cityNSSize / 2.0
		buildingOutline = LineSegs("building")

		buildingSize = 8
		buildingPadding = 1
		buildingOutline.setColor(0, 0, 0, 1)
		buildingOutline.moveTo(buildingPadding, buildingPadding, 0)
		buildingOutline.drawTo(buildingPadding + buildingSize, buildingPadding, 0)
		buildingOutline.drawTo(buildingPadding + buildingSize, buildingPadding + buildingSize, 0)
		buildingOutline.drawTo(buildingPadding, buildingPadding + buildingSize, 0)
		buildingOutline.drawTo(buildingPadding, buildingPadding, 0)
		buildingOutlinePrototype = NodePath(buildingOutline.create())

		# Create buildings from city blueprint
		for rowIndex, row in enumerate(city):
			for columnIndex, buildingType in enumerate(row):
				# Get building data from city blueprint
				buildingInstanceName, buildingPrototype = self.buildingInstanceNameAndPrototypeFromType(buildingType)

				if (not (buildingInstanceName is None or buildingPrototype is None)):
					# Compute building position
					buildingX, buildingY, buildingZ = columnIndex * blockSize - cityWESize / 2, cityNSSize / 2 - (rowIndex + 1) * blockSize, 0

					# Create building pad
					buildingPadInstance = self.render.attachNewNode("buildingPadInstance")
					buildingPadInstance.setPos(buildingX, buildingY, buildingZ)
					self.buildingPadPrototype.instanceTo(buildingPadInstance)

					# Create building
					buildingInstance = self.render.attachNewNode(buildingInstanceName)
					buildingInstance.setPos(buildingX, buildingY, buildingZ)
					buildingPrototype.instanceTo(buildingInstance)

					# Create building outline in minimap
					buildingOutlineInstance = self.phoneState.minimap.attachNewNode("buildingOutline")
					buildingOutlineInstance.setPos(buildingX, buildingY, buildingZ)
					buildingOutlinePrototype.instanceTo(buildingOutlineInstance)

	def setMouseBtn(self, btn, value):
		self.mousebtn[btn] = value

		if (btn == 0 and value == 1 and self.phoneState.state == "Center"):
			phoneDisplayRegionCenterX = self.win.getXSize() * (self.phoneState.phoneDisplayRegion.getLeft() + self.phoneState.phoneDisplayRegion.getRight()) / 2.0
			phoneDisplayRegionCenterY = self.win.getYSize() * (1.0 - (self.phoneState.phoneDisplayRegion.getBottom() + self.phoneState.phoneDisplayRegion.getTop()) / 2.0)
			mouse = self.win.getPointer(0)
			s = 2 ** self.phoneState.minimapZoom
			x = clamp(self.camera.getX() + (mouse.getX() - phoneDisplayRegionCenterX) / s, -self.maxX, self.maxX)
			y = clamp(self.camera.getY() + (phoneDisplayRegionCenterY - mouse.getY()) / s, -self.maxY, self.maxY)
			previousHeading = self.camera.getH() % 360.0
			heading = (rad2Deg(atan2(y - self.camera.getY(), x - camera.getX())) - 90.0) % 360.0

			if (180.0 < abs(heading - previousHeading)):
				if (previousHeading < heading):
					heading -= 360.0
				else:
					heading += 360.0

			self.camera.setH(previousHeading)
			self.phoneState.orientationTriangle.setH(previousHeading)

			Parallel(
				self.camera.posInterval(0.5, Vec3(x, y, self.camera.getZ())),
				self.phoneState.minimapCamera.posInterval(0.5, Vec3(x, y, self.phoneState.minimapCamera.getZ())),
				self.phoneState.orientationTriangle.posInterval(0.5, Vec3(x, y, self.phoneState.orientationTriangle.getZ())),
				self.camera.hprInterval(0.5, Vec3(heading, self.camera.getP(), self.camera.getR())),
				self.phoneState.orientationTriangle.hprInterval(0.5, Vec3(heading, self.phoneState.orientationTriangle.getP(), self.phoneState.orientationTriangle.getR()))
			).start()

	def buildingInstanceNameAndPrototypeFromType(self, buildingType):
		return {
			'S' : ( None, None ),
			'P' : ( "policeBuildingInstance", self.policeBuildingPrototype ),
			'T' : ( "tribunalInstance", self.tribunalPrototype ),
			'O' : ( "officeBuildingInstance", self.officeBuildingPrototype ),
			'H' : ( "houseInstance", self.housePrototype ),
		}.get(buildingType, ( None, None ))
	
	def setBlurSharpen(self, amount):
		if (not self.useAdvancedVisualEffects):
			return

		if (amount == 1.0):
			self.filters.delBlurSharpen()
		else:
			self.filters.setBlurSharpen(amount=amount)

	def controlCamera(self, task):
		if (self.phoneState.state == "Center"):
			return Task.cont

		# figure out how much the mouse has moved (in pixels)
		mouse = self.win.getPointer(0)
		x = mouse.getX()
		y = mouse.getY()
		windowCenterX = self.win.getXSize() / 2
		windowCenterY = self.win.getYSize() / 2
		heading = self.camera.getH()
		pitch = self.camera.getP()

		if self.win.movePointer(0, windowCenterX, windowCenterY):
			heading -= (x - windowCenterX) * 0.2
			pitch = clamp(pitch - (y - windowCenterY) * 0.2, -45, 45)

		self.camera.setHpr(heading, pitch, 0)

		elapsed = task.time - self.last

		if (self.last == 0):
			elapsed = 0

		if (self.mousebtn[0]):
			direction = self.camera.getMat().getRow3(1)
			self.camera.setPos(self.camera.getPos() + direction * elapsed*30)

		clampX(self.camera, -self.maxX, self.maxX)
		clampY(self.camera, -self.maxY, self.maxY)
		self.camera.setZ(2)

		self.phoneState.minimapCamera.setX(self.camera.getX())
		self.phoneState.minimapCamera.setY(self.camera.getY())

		self.phoneState.orientationTriangle.setX(self.camera.getX())
		self.phoneState.orientationTriangle.setY(self.camera.getY())
		self.phoneState.orientationTriangle.setHpr(heading, -90, 0)

		self.last = task.time

		return Task.cont

loadPrcFile("myconfig.prc")

MyApp().run()
