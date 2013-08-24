import sys
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.directnotify.DirectNotify import DirectNotify
from direct.filter.CommonFilters import CommonFilters
from direct.fsm.FSM import FSM
from direct.interval.IntervalGlobal import *
from direct.task import Task

def clamp(value, minValue, maxValue):
	return min(max(minValue, value), maxValue)

def clampX(target, minX, maxX):
	target.setX(clamp(target.getX(), minX, maxX))

def clampY(target, minY, maxY):
	target.setY(clamp(target.getY(), minY, maxY))

def clampZ(target, minZ, maxZ):
	target.setZ(clamp(target.getZ(), minZ, maxZ))

class PhoneState(FSM):

	def __init__(self, app):
		FSM.__init__(self, "PhoneState")
		self.app = app
		self.mouseVisible = True
		self.previousState = self.state

	def enterHidden(self):
		Sequence(
			Func(self.setMouseVisible, False),
			Func(self.app.phoneDisplayRegion.setActive, False),
			Parallel(
				self.app.phone.posInterval(0.25, self.app.phoneHiddenPosition),
				LerpFunc(self.app.phoneDisplayRegion.setDimensions, duration=0.25,
					fromData=self.app.phoneDisplayRegion.getDimensions(), toData=self.app.phoneDisplayRegionHiddenDimensions)
			),
			Func(self.app.setBlurSharpen, 1.0)
		).start()

	def exitHidden(self):
		self.previousState = self.oldState

	def enterVisible(self):
		Sequence(
			Func(self.setMouseVisible, False),
			Parallel(
				self.app.phone.posInterval(0.25, self.app.phoneVisiblePosition),
				LerpFunc(self.app.phoneDisplayRegion.setDimensions, duration=0.25,
					fromData=self.app.phoneDisplayRegion.getDimensions(), toData=self.app.phoneDisplayRegionVisibleDimensions)
			),
			Func(self.app.setBlurSharpen, 1.0),
			Func(self.app.phoneDisplayRegion.setActive, True)
		).start()

	def exitVisible(self):
		self.previousState = self.oldState

	def enterCenter(self):
		Sequence(
			Func(self.app.setBlurSharpen, 0.0),
			Parallel(
				self.app.phone.posInterval(0.25, self.app.phoneCenterPosition),
				LerpFunc(self.app.phoneDisplayRegion.setDimensions, duration=0.25,
					fromData=self.app.phoneDisplayRegion.getDimensions(), toData=self.app.phoneDisplayRegionCenterDimensions)
			),
			Func(self.app.phoneDisplayRegion.setActive, True),
			Func(self.setMouseVisible, True)
		).start()

	def exitCenter(self):
		self.setMouseVisible(False)
		self.previousState = self.oldState

	def getPreviousState(self):
		return self.previousState

	def setMouseVisible(self, mouseVisible):
		if (self.mouseVisible != mouseVisible):
			self.mouseVisible = mouseVisible

			props = WindowProperties()
			props.setCursorHidden(not mouseVisible)
			self.app.win.requestProperties(props)

			if (not mouseVisible):
				windowCenterX = self.app.win.getXSize() / 2
				windowCenterY = self.app.win.getYSize() / 2
				self.app.win.movePointer(0, windowCenterX, windowCenterY)

class MyApp(ShowBase):

	def __init__(self):
		ShowBase.__init__(self)

		self.useAdvancedVisualEffects = True

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

		self.heading = 180
		self.pitch = 0
		self.mousex = 0
		self.mousey = 0
		self.last = 0
		self.mousebtn = [0,0,0]

		self.accept("mouse1", self.setMouseBtn, [0, 1])
		self.accept("mouse1-up", self.setMouseBtn, [0, 0])
		self.accept("mouse2", self.togglePhoneCenter)
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

		self.phoneCamera = NodePath(Camera("phoneCamera"))
		self.phoneCamera.node().setLens(OrthographicLens())
		self.phoneCamera.node().getLens().setNearFar(1, 100)
		self.phoneDisplayRegion.setCamera(self.phoneCamera)
		self.phoneCamera.reparentTo(self.minimap)
		self.phoneCamera.setPos(self.camera.getPos())
		self.phoneCamera.setZ(50)
		self.phoneCamera.lookAt(self.camera.getPos())

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
		if (zoomVariation == 0 or self.isPhoneVisible()):
			self.minimapZoom = clamp(self.minimapZoom + zoomVariation, -2, 4)
			s = 2 ** self.minimapZoom
			self.orientationTriangle.setScale(5.0 / s)
			self.phoneCamera.node().getLens().setFilmSize(self.phoneDisplayRegion.getPixelWidth() / s, self.phoneDisplayRegion.getPixelHeight() / s)

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
		self.housePrototype = self.loader.loadModel("models/house")

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

	def controlCamera(self, task):
		if (self.phoneState.state == "Center"):
			return Task.cont

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

		self.phoneCamera.setX(self.camera.getX())
		self.phoneCamera.setY(self.camera.getY())

		self.orientationTriangle.setX(self.camera.getX())
		self.orientationTriangle.setY(self.camera.getY())
		self.orientationTriangle.setHpr(self.heading, -90, 0)

		self.last = task.time

		return Task.cont

MyApp().run()
