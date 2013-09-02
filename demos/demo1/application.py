import sys, os
from panda3d.core import *
from panda3d.egg import *
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from bop import *
from orbitalcameracontroller import *
from utils import *

class Application(ShowBase):

	def __init__(self):
		ShowBase.__init__(self)

		self.scriptPath = os.path.dirname(sys.argv[0]).replace("\\", "/")

		self.game = Game(self.scriptPath)

		self.setupModels()
		self.setupLighting()
		self.setupKeyboard()
		self.cameraController = OrbitalCameraController(self)
		self.camera.setHpr(10, -40, 0)
		self.cameraController.scaleDistanceFromTarget(3)

	def setupModels(self):
		self.city = self.loader.loadModel("models/city")
		self.city.reparentTo(self.render)

	def setupLighting(self):
		self.ambientLight = self.render.attachNewNode(AmbientLight("ambientLight"))
		self.ambientLight.node().setColor(Vec4(1, 1, 1, 1))
		self.render.setLight(self.ambientLight)

	def setupKeyboard(self):
		self.accept("escape", sys.exit)

loadPrcFile("myconfig.prc")

Application().run()
