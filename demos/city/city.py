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
		self.setupeFilters()
		self.setupModels()
		self.setupKeyboardControl()
		self.camera.setPos(0, 0, 2)
		self.setupMouseControl()
		self.phoneState.request("Hidden")

	def setupeFilters(self):
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
		self.accept("mouse2", self.togglePhoneCenter)
		self.accept("tab", self.togglePhoneCenter)
		self.accept("mouse3", self.togglePhoneVisible)
		self.accept("wheel_up", self.incrementMinimapZoom, [1])
		self.accept("wheel_down", self.incrementMinimapZoom, [-1])

		self.taskMgr.add(self.controlCamera, "cameraTask")

	def setupModels(self):
		self.setupLights()
		self.loadSky()
		self.loadTerrain()
		self.setupBuildings()
		self.setupPhone()

	def setupPhone(self):
		self.phone = self.loader.loadModel("models/phone")
		self.phone.reparentTo(self.render2d)
		self.phone.setLightOff()
		self.phone.setDepthWrite(False)
		self.phone.setDepthTest(False)

		self.phoneDisplayRegion = self.win.makeDisplayRegion(0.0, 1.0, 0.0, 1.0)
		self.phoneDisplayRegion.setClearColor(Vec4(1, 1, 1, 1))
		self.phoneDisplayRegion.setClearColorActive(True)
		self.phoneDisplayRegion.setClearDepthActive(True)
		self.phoneDisplayRegion.setSort(self.cam2d.node().getDisplayRegion(0).getSort() + 1)
		self.phoneDisplayRegion.setActive(False)

		self.minimapCamera = NodePath(Camera("minimapCamera"))
		self.minimapCamera.node().setLens(OrthographicLens())
		self.minimapCamera.node().getLens().setNearFar(1, 100)
		self.minimapCamera.reparentTo(self.minimap)
		self.minimapCamera.setPos(self.camera.getPos())
		self.minimapCamera.setZ(50)
		self.minimapCamera.lookAt(self.camera.getPos())
		self.phoneDisplayRegion.setCamera(self.minimapCamera)

		self.orientationTriangle = self.loader.loadModel("models/orientation_triangle")
		self.orientationTriangle.reparentTo(self.minimap)
		self.orientationTriangle.setPos(0, 0, 45)
		self.orientationTriangle.setHpr(0, -90, 0)
		self.orientationTriangle.setLightOff()

		self.updatePhoneGeometry(None)

		self.accept("window-event", self.updatePhoneGeometry)

		self.minimapZoom = 3
		self.incrementMinimapZoom(0)

	def updatePhoneGeometry(self, event):
		windowWidth = 1.0 * self.win.getXSize()
		windowHeight = 1.0 * self.win.getYSize()
		phoneWidth = 256.0
		phoneHeight = 512.0
		phoneTopBorder = 48.0
		phoneDisplayRegionLeftOffset = 15.0
		phoneDisplayRegionRightOffset = 241.0
		phoneDisplayRegionBottomOffset = 73.0
		phoneDisplayRegionTopOffset = 459.0
		phoneLeft = windowWidth - phoneWidth
		phoneHiddenBottom = 0.0 - phoneHeight + phoneTopBorder
		phoneVisibleBottom = 0.0
		phoneCenterLeft = phoneLeft / 2.0
		phoneCenterBottom = (windowHeight - phoneHeight) / 2.0
		self.phoneHiddenPosition = Vec3(2.0 * phoneLeft / windowWidth - 1.0, 0, 2.0 * phoneHiddenBottom / windowHeight - 1.0)
		self.phoneVisiblePosition = Vec3(2.0 * phoneLeft / windowWidth - 1.0, 0, 2.0 * phoneVisibleBottom / windowHeight - 1.0)
		self.phoneCenterPosition = Vec3(2.0 * phoneCenterLeft / windowWidth - 1.0, 0, 2.0 * phoneCenterBottom / windowHeight - 1.0)
		self.phoneDisplayRegionHiddenDimensions = Vec4((phoneLeft + phoneDisplayRegionLeftOffset) / windowWidth, (phoneLeft + phoneDisplayRegionRightOffset) / windowWidth,
			(phoneHiddenBottom + phoneDisplayRegionBottomOffset) / windowHeight, (phoneHiddenBottom + phoneDisplayRegionTopOffset) / windowHeight)
		self.phoneDisplayRegionVisibleDimensions = Vec4((phoneLeft + phoneDisplayRegionLeftOffset) / windowWidth, (phoneLeft + phoneDisplayRegionRightOffset) / windowWidth,
			(phoneVisibleBottom + phoneDisplayRegionBottomOffset) / windowHeight, (phoneVisibleBottom + phoneDisplayRegionTopOffset) / windowHeight)
		self.phoneDisplayRegionCenterDimensions = Vec4((phoneCenterLeft + phoneDisplayRegionLeftOffset) / windowWidth, (phoneCenterLeft + phoneDisplayRegionRightOffset) / windowWidth,
			(phoneCenterBottom + phoneDisplayRegionBottomOffset) / windowHeight, (phoneCenterBottom + phoneDisplayRegionTopOffset) / windowHeight)

		self.phone.setScale(2.0 * phoneWidth / windowWidth, 1.0, 2.0 * phoneHeight / windowHeight)

		if (self.phoneState.state == "Visible"):
			self.phone.setPos(self.phoneVisiblePosition)
			self.phoneDisplayRegion.setDimensions(self.phoneDisplayRegionVisibleDimensions)
		elif (self.phoneState.state == "Center"):
			self.phone.setPos(self.phoneCenterPosition)
			self.phoneDisplayRegion.setDimensions(self.phoneDisplayRegionCenterDimensions)
		else:
			self.phone.setPos(self.phoneHiddenPosition)
			self.phoneDisplayRegion.setDimensions(self.phoneDisplayRegionHiddenDimensions)

	def incrementMinimapZoom(self, zoomVariation):
		if (zoomVariation == 0 or self.phoneState.state == "Visible" or self.phoneState.state == "Center"):
			self.minimapZoom = clamp(self.minimapZoom + zoomVariation, -2, 4)
			s = 2 ** self.minimapZoom
			self.orientationTriangle.setScale(5.0 / s)
			self.minimapCamera.node().getLens().setFilmSize(self.phoneDisplayRegion.getPixelWidth() / s, self.phoneDisplayRegion.getPixelHeight() / s)

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
		self.minimap = NodePath("minimap")
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
					buildingOutlineInstance = self.minimap.attachNewNode("buildingOutline")
					buildingOutlineInstance.setPos(buildingX, buildingY, buildingZ)
					buildingOutlinePrototype.instanceTo(buildingOutlineInstance)

	def setMouseBtn(self, btn, value):
		self.mousebtn[btn] = value

		if (btn == 0 and value == 1 and self.phoneState.state == "Center"):
			phoneDisplayRegionCenterX = self.win.getXSize() * (self.phoneDisplayRegion.getLeft() + self.phoneDisplayRegion.getRight()) / 2.0
			phoneDisplayRegionCenterY = self.win.getYSize() * (1.0 - (self.phoneDisplayRegion.getBottom() + self.phoneDisplayRegion.getTop()) / 2.0)
			mouse = self.win.getPointer(0)
			s = 2 ** self.minimapZoom
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
			self.orientationTriangle.setH(previousHeading)

			Parallel(
				self.camera.posInterval(0.5, Vec3(x, y, self.camera.getZ())),
				self.minimapCamera.posInterval(0.5, Vec3(x, y, self.minimapCamera.getZ())),
				self.orientationTriangle.posInterval(0.5, Vec3(x, y, self.orientationTriangle.getZ())),
				self.camera.hprInterval(0.5, Vec3(heading, self.camera.getP(), self.camera.getR())),
				self.orientationTriangle.hprInterval(0.5, Vec3(heading, self.orientationTriangle.getP(), self.orientationTriangle.getR()))
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

	def togglePhoneCenter(self):
		if (self.phoneState.state != "Center"):
			self.phoneState.demand("Center")
		else:
			self.phoneState.demand(self.phoneState.getPreviousState())

	def togglePhoneVisible(self):
		if (self.phoneState.state == "Visible"):
			self.phoneState.demand("Hidden")
		elif (self.phoneState.state == "Hidden"):
			self.phoneState.demand("Visible")
		else:
			self.phoneState.demand(self.phoneState.getPreviousState())

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

		self.minimapCamera.setX(self.camera.getX())
		self.minimapCamera.setY(self.camera.getY())

		self.orientationTriangle.setX(self.camera.getX())
		self.orientationTriangle.setY(self.camera.getY())
		self.orientationTriangle.setHpr(heading, -90, 0)

		self.last = task.time

		return Task.cont

loadPrcFile("myconfig.prc")

MyApp().run()
