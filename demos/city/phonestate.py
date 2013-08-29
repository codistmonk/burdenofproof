from panda3d.core import *
from direct.fsm.FSM import FSM
from direct.interval.IntervalGlobal import *

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
