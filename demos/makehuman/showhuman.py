import sys, os, struct
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.task import Task
from direct.gui.DirectGui import *

from orbitalcameracontroller import *
from objparser import *
from objloader import *

def readMakehumanTarget(path):
	result = []

	with open(path, "rb") as inputFile:
		bytes = inputFile.read(16)

		while bytes:
			vertexIndex, deltaX, deltaY, deltaZ = struct.unpack("<ifff", bytes)
			result.append((vertexIndex, Vec3(deltaX, deltaY, deltaZ)))
			bytes = inputFile.read(16)

	return result

class ShowHuman(ShowBase):

	def __init__(self):
		ShowBase.__init__(self)

		self.useAdvancedVisualEffects = ConfigVariableBool("use-advanced-visual-effects", True)

		self.setupKeyboardControl()
		self.setupModels()
		self.setupLights()
		self.setupGUI()
		self.cameraController = OrbitalCameraController(self)

	def setupModels(self):
		self.staticHumanObjLoader = ObjLoader("human")
		self.dynamicHumanObjLoader = ObjLoader("human")
		self.human = self.render.attachNewNode(ObjParser("data/3dobjs/base.obj", [self.staticHumanObjLoader, self.dynamicHumanObjLoader]).listeners[1].node)
		self.target = readMakehumanTarget("data/targets/measure/measure-bust-increase.targetb")

		# TODO(codistmonk) consider that there may be multiple vdatas
		# for general objs, although Makehuman only has one
		self.staticVertices = GeomVertexRewriter(self.staticHumanObjLoader.vdata, 'vertex')
		self.dynamicVertices = GeomVertexRewriter(self.dynamicHumanObjLoader.vdata, 'vertex')

	def setupKeyboardControl(self):
		self.accept("escape", sys.exit)

	def setupLights(self):
		self.sunlight = self.render.attachNewNode(DirectionalLight("sunlight"))
		self.sunlight.setColor(Vec4(0.8, 0.8, 0.8, 1))
		self.sunlight.node().getLens().setFilmSize(32, 32)
		self.sunlight.node().getLens().setNearFar(75,95)
		self.sunlight.setPos(60, 30, 50)
		self.sunlight.lookAt(0, 0, 0)
		self.render.setLight(self.sunlight)
		self.sunlight.node().showFrustum()
		if (self.useAdvancedVisualEffects and base.win.getGsg().getSupportsBasicShaders() != 0 and base.win.getGsg().getSupportsDepthTexture() != 0):
			self.sunlight.node().setShadowCaster(True, 256, 256)
			self.render.setShaderAuto()

		self.ambientLight = self.render.attachNewNode(AmbientLight("ambientLight"))
		self.ambientLight.node().setColor(Vec4(0.2, 0.2, 0.2, 1))
		self.render.setLight(self.ambientLight)

		self.taskMgr.add(self.sunlightConrol, "sunlightControl")

	def sunlightConrol(self, task):
		setOrbiterHeading(self.sunlight, self.camera.getH() + 60.0, self.cameraController.target)

		return Task.cont

	def setupGUI(self):
		self.slider = DirectSlider(range = (-50, 50), value = 0, pageSize = 5, command = lambda : self.sliderChanged())
		self.slider.setPos(0.0, 0.0, -0.9)

	def sliderChanged(self):
		amount = self.slider["value"] / 10.0

		for vertexObjIndex, delta in self.target:
			for vertexIndex in self.staticHumanObjLoader.vertexCopies[vertexObjIndex]:
				self.staticVertices.setRow(vertexIndex)
				self.dynamicVertices.setRow(vertexIndex)
				self.dynamicVertices.setData3f(self.staticVertices.getData3f() + delta * amount)

ShowHuman().run()
