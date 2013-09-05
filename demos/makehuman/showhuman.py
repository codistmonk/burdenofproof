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
	inputFile = open(path, "rb")

	try:
		bytes = inputFile.read(16)

		while bytes:
			vertexIndex, deltaX, deltaY, deltaZ = struct.unpack("<ifff", bytes)
			result.append((vertexIndex, Vec3(deltaX, deltaY, deltaZ)))
			bytes = inputFile.read(16)
	finally:
		inputFile.close()

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
		self.dynamicHumanObjLoader = ObjLoader("human")
		self.human = self.render.attachNewNode(ObjParser("data/3dobjs/base.obj", [self.dynamicHumanObjLoader]).listeners[0].node)
		self.setTarget("data/targets/measure/measure-bust-increase")

		# TODO(codistmonk) consider that there may be multiple vdatas
		# for general objs, although Makehuman only has one
		self.dynamicVertices = GeomVertexRewriter(self.dynamicHumanObjLoader.vdata, 'vertex')
		self.setStaticVertices()

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

		if ConfigVariableBool("show-sunlight-frustum", True):
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
		self.userEntry = DirectEntry(text = "" , scale = .05, command = lambda command : self.userEntryChanged(command), initialText = "self.help()",
			width = 20, numLines = 2, focus = 1)
		self.userEntry.setPos(-1.3, 0.0, -0.9)

	def userEntryChanged(self, command):
		try:
			print command
			exec command
		except:
			print sys.exc_info()
		finally:
			self.userEntry["focus"] = True

	def setTarget(self, path):
		self.targetPath = path
		self.target = readMakehumanTarget(path + ".targetb")

	def setStaticVertices(self):
		self.staticVertices = []
		self.dynamicVertices.setRow(0)

		while not self.dynamicVertices.isAtEnd():
			self.staticVertices.append(Vec3(self.dynamicVertices.getData3f()))

	def applyTarget(self, amount):
		for vertexObjIndex, delta in self.target:
			for vertexIndex in self.dynamicHumanObjLoader.vertexCopies[vertexObjIndex]:
				self.dynamicVertices.setRow(vertexIndex)
				self.dynamicVertices.setData3f(self.staticVertices[vertexIndex] + delta * amount)

	def help(self):
		print
		print "self.help()"
		print "     Print this message"
		print
		print "self.setTarget(path)"
		print "     Load the target specified by path"
		print "     Example: self.setTarget(\"data/targets/measure/measure-bust-increase\")"
		print
		print "self.applyTarget(amount)"
		print "     Deform the dynamic model using the current target modulated by the specified amount"
		print "     dynamicModel = staticModel + target * amount"
		print "     The static model is not affected"
		print
		print "self.setStaticVertices()"
		print "     Save the current deformation into the static model"
		print "     staticModel = dynamicModel"
		print

loadPrcFile("myconfig.prc")

ShowHuman().run()
