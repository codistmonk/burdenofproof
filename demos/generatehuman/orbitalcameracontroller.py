from panda3d.core import *
from direct.task import Task

from utils import *

class OrbitalCameraController:

	def __init__(self, scene):
		self.scene = scene
		self.mouseButton = [0, 0, 0]
		self.target = Vec3(0.0, 0.0, 0.0)
		self.distanceFromTarget = 64.0
		self.last = 0
		self.mouseVisible = True
		self.mouseLastVisibleLocation = None

		scene.disableMouse()

		scene.accept("mouse1", self.setMouseButton, [0, 1])
		scene.accept("mouse1-up", self.setMouseButton, [0, 0])
		scene.accept("wheel_up", self.scaleDistanceFromTarget, [0.75])
		scene.accept("wheel_down", self.scaleDistanceFromTarget, [1.25])

		scene.taskMgr.add(self.controlCamera, "cameraTask")

	def setMouseButton(self, button, value):
		self.mouseButton[button] = value

		if button == 0:
			self.setMouseVisible(value == 0)

	def scaleDistanceFromTarget(self, scale):
		self.distanceFromTarget *= scale

	def controlCamera(self, task):
		if self.mouseButton[0]:
			mouse = self.scene.win.getPointer(0)
			x = mouse.getX()
			y = mouse.getY()
			mousePreviousX = self.mouseLastVisibleLocation.getX()
			mousePreviousY = self.mouseLastVisibleLocation.getY()
			heading = self.scene.camera.getH()
			pitch = self.scene.camera.getP()

			if self.scene.win.movePointer(0, mousePreviousX, mousePreviousY):
				heading -= (x - mousePreviousX) * 0.2
				pitch = clamp(pitch - (y - mousePreviousY) * 0.2, -89, 89)
				self.scene.camera.setHpr(heading, pitch, 0)

		direction = self.scene.camera.getMat().getRow3(1)
		self.scene.camera.setPos(self.target - direction * self.distanceFromTarget)

		return Task.cont

	def setMouseVisible(self, mouseVisible):
		if (self.mouseVisible != mouseVisible):
			self.mouseVisible = mouseVisible

			props = WindowProperties()
			props.setCursorHidden(not mouseVisible)
			self.scene.win.requestProperties(props)

			if (not mouseVisible):
				self.mouseLastVisibleLocation = self.scene.win.getPointer(0)

	def tictoc(self, task):
		elapsed = task.time - self.last

		if (self.last == 0):
			elapsed = 0

		self.last = task.time

		return elapsed
