import sys, os, struct
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *

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
		self.cameraController = OrbitalCameraController(self)

	def setupModels(self):
#		self.human = self.loader.loadModel("data/3dobjs/base")
#		self.human.reparentTo(self.render)
		self.humanObjLoader = ObjLoader("human")
		self.human = self.render.attachNewNode(ObjParser("data/3dobjs/base.obj", self.humanObjLoader).listener.node)
		target = readMakehumanTarget("data/targets/measure/measure-bust-increase.targetb")

		# TODO(codistmonk) consider that there may be multiple vdatas
		# for general objs, although Makehuman only has one
		vertices = GeomVertexRewriter(self.humanObjLoader.vdata, 'vertex')
		amount = 4.0

		for vertexObjIndex, delta in target:
			for vertexIndex in self.humanObjLoader.vertexCopies[vertexObjIndex]:
				vertices.setRow(vertexIndex)
				vertices.setData3f(vertices.getData3f() + delta * amount)

	def setupKeyboardControl(self):
		self.accept("escape", sys.exit)

	def setupLights(self):
		self.sunLight = self.render.attachNewNode(DirectionalLight("sunLight"))
		self.sunLight.setColor(Vec4(0.8, 0.8, 0.8, 1))
		self.sunLight.node().getLens().setFilmSize(32, 32)
		self.sunLight.node().getLens().setNearFar(75,95)
		self.sunLight.setPos(60, 30, 50)
		self.sunLight.lookAt(0, 0, 0)
		self.render.setLight(self.sunLight)
		self.sunLight.node().showFrustum()
		if (self.useAdvancedVisualEffects and base.win.getGsg().getSupportsBasicShaders() != 0 and base.win.getGsg().getSupportsDepthTexture() != 0):
			self.sunLight.node().setShadowCaster(True, 256, 256)
			self.render.setShaderAuto()

		self.ambientLight = self.render.attachNewNode(AmbientLight("ambientLight"))
		self.ambientLight.node().setColor(Vec4(0.2, 0.2, 0.2, 1))
		self.render.setLight(self.ambientLight)

ShowHuman().run()
