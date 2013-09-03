from panda3d.core import *
from direct.fsm.FSM import FSM
from direct.interval.IntervalGlobal import *

class PhoneState(FSM):

	def __init__(self, app):
		FSM.__init__(self, "PhoneState")
		self.app = app
		self.mouseVisible = True
		self.previousState = self.state
		self.minimap = NodePath("minimap")

		app.accept("mouse2", self.togglePhoneCenter)
		app.accept("tab", self.togglePhoneCenter)
		app.accept("mouse3", self.togglePhoneVisible)
		self.accept("wheel_up", self.incrementMinimapZoom, [1])
		self.accept("wheel_down", self.incrementMinimapZoom, [-1])

	def enterHidden(self):
		Sequence(
			Func(self.setMouseVisible, False),
			Func(self.phoneDisplayRegion.setActive, False),
			Parallel(
				self.phone.posInterval(0.25, self.phoneHiddenPosition),
				LerpFunc(self.phoneDisplayRegion.setDimensions, duration=0.25,
					fromData=self.phoneDisplayRegion.getDimensions(), toData=self.phoneDisplayRegionHiddenDimensions)
			),
			Func(self.app.setBlurSharpen, 1.0)
		).start()

	def exitHidden(self):
		self.previousState = self.oldState

	def enterVisible(self):
		Sequence(
			Func(self.setMouseVisible, False),
			Parallel(
				self.phone.posInterval(0.25, self.phoneVisiblePosition),
				LerpFunc(self.phoneDisplayRegion.setDimensions, duration=0.25,
					fromData=self.phoneDisplayRegion.getDimensions(), toData=self.phoneDisplayRegionVisibleDimensions)
			),
			Func(self.app.setBlurSharpen, 1.0),
			Func(self.phoneDisplayRegion.setActive, True)
		).start()

	def exitVisible(self):
		self.previousState = self.oldState

	def enterCenter(self):
		Sequence(
			Func(self.app.setBlurSharpen, 0.0),
			Parallel(
				self.phone.posInterval(0.25, self.phoneCenterPosition),
				LerpFunc(self.phoneDisplayRegion.setDimensions, duration=0.25,
					fromData=self.phoneDisplayRegion.getDimensions(), toData=self.phoneDisplayRegionCenterDimensions)
			),
			Func(self.phoneDisplayRegion.setActive, True),
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

	def togglePhoneCenter(self):
		if (self.state != "Center"):
			self.demand("Center")
		else:
			self.demand(self.getPreviousState())

	def togglePhoneVisible(self):
		if (self.state == "Visible"):
			self.demand("Hidden")
		elif (self.state == "Hidden"):
			self.demand("Visible")
		else:
			self.demand(self.getPreviousState())

	def setupPhone(self):
		self.phone = self.app.loader.loadModel("models/phone")
		self.phone.reparentTo(self.app.render2d)
		self.phone.setLightOff()
		self.phone.setDepthWrite(False)
		self.phone.setDepthTest(False)

		self.phoneDisplayRegion = self.app.win.makeDisplayRegion(0.0, 1.0, 0.0, 1.0)
		self.phoneDisplayRegion.setClearColor(Vec4(1, 1, 1, 1))
		self.phoneDisplayRegion.setClearColorActive(True)
		self.phoneDisplayRegion.setClearDepthActive(True)
		self.phoneDisplayRegion.setSort(self.app.cam2d.node().getDisplayRegion(0).getSort() + 1)
		self.phoneDisplayRegion.setActive(False)

		self.minimapCamera = NodePath(Camera("minimapCamera"))
		self.minimapCamera.node().setLens(OrthographicLens())
		self.minimapCamera.node().getLens().setNearFar(1, 100)
		self.minimapCamera.reparentTo(self.minimap)
		self.minimapCamera.setPos(self.app.camera.getPos())
		self.minimapCamera.setZ(50)
		self.minimapCamera.lookAt(self.app.camera.getPos())
		self.phoneDisplayRegion.setCamera(self.minimapCamera)

		self.orientationTriangle = self.app.loader.loadModel("models/orientation_triangle")
		self.orientationTriangle.reparentTo(self.minimap)
		self.orientationTriangle.setPos(0, 0, 45)
		self.orientationTriangle.setHpr(0, -90, 0)
		self.orientationTriangle.setLightOff()

		self.updatePhoneGeometry(None)

		self.app.accept("window-event", self.updatePhoneGeometry)

		self.minimapZoom = 3
		self.incrementMinimapZoom(0)

	def updatePhoneGeometry(self, event):
		windowWidth = 1.0 * self.app.win.getXSize()
		windowHeight = 1.0 * self.app.win.getYSize()
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

		if (self.state == "Visible"):
			self.phone.setPos(self.phoneVisiblePosition)
			self.phoneDisplayRegion.setDimensions(self.phoneDisplayRegionVisibleDimensions)
		elif (self.state == "Center"):
			self.phone.setPos(self.phoneCenterPosition)
			self.phoneDisplayRegion.setDimensions(self.phoneDisplayRegionCenterDimensions)
		else:
			self.phone.setPos(self.phoneHiddenPosition)
			self.phoneDisplayRegion.setDimensions(self.phoneDisplayRegionHiddenDimensions)

	def incrementMinimapZoom(self, zoomVariation):
		if (zoomVariation == 0 or self.state == "Visible" or self.state == "Center"):
			self.minimapZoom = clamp(self.minimapZoom + zoomVariation, -2, 4)
			s = 2 ** self.minimapZoom
			self.orientationTriangle.setScale(5.0 / s)
			self.minimapCamera.node().getLens().setFilmSize(self.phoneDisplayRegion.getPixelWidth() / s, self.phoneDisplayRegion.getPixelHeight() / s)
