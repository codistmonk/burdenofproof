import sys, os, struct
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from panda3d.egg import *
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

def forEachPrimitiveIn(node, process = lambda primitive : None):
	for geomIndex in range(node.getNumGeoms()):
		geom = node.getGeom(geomIndex)

		for primitiveIndex in range(geom.getNumPrimitives()):
			process(geom.getPrimitive(primitiveIndex))

def forEachVisiblePrimitiveIn(nodePath, process = lambda primitive : None):
	for geomNodePath in nodePath.findAllMatches('**/+GeomNode'):
		if not geomNodePath.isHidden():
			forEachPrimitiveIn(geomNodePath.node(), process)

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
		self.hide("joint*")

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
			width = 40, numLines = 2, focus = 1)
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

	def show(self, nodePattern):
		for nodePath in self.find(nodePattern):
			nodePath.show()

	def hide(self, nodePattern):
		for nodePath in self.find(nodePattern):
			nodePath.hide()

	def setColor(self, r, g, b, nodePattern):
		for nodePath in self.find(nodePattern):
			nodePath.setColor(r, g, b)

	def find(self, nodePattern):
		return self.human.findAllMatches(nodePattern)

	def center(self, nodePattern):
		self.cameraController.target = self.computeCenter(self.human.find(nodePattern).node())

	def sumVertices(self, primitive, result = Vec3(), vertexCount = [0]):
		for k in range(primitive.getNumVertices()):
			self.dynamicVertices.setRow(primitive.getVertex(k))
			result += self.dynamicVertices.getData3f()
			vertexCount[0] += 1

	def computeCenter(self, pandaNode):
		center = Vec3()
		vertexCount = [0]

		forEachPrimitiveIn(pandaNode, lambda primitive : self.sumVertices(primitive, center, vertexCount))

		vertexCount = vertexCount[0]

		if 0 < vertexCount:
			center /= vertexCount

		print "center:", center, "computed using", vertexCount, "vertices"

		return center

	def exportPrimitiveToEgg(self, primitive, eggVertices):
		egg = eggVertices.getParent()

		if isinstance(primitive, GeomTriangles):
			for faceIndex in range(primitive.getNumFaces()):
				eggPolygon = EggPolygon()

				egg.addChild(eggPolygon)

				for vertexIndex in range(primitive.getPrimitiveStart(faceIndex), primitive.getPrimitiveEnd(faceIndex)):
					self.dynamicVertices.setRow(primitive.getVertex(vertexIndex))
					vertex = self.dynamicVertices.getData3f()
					eggPolygon.addVertex(newEggVertex(eggVertices, vertex.getX(), vertex.getY(), vertex.getZ()))
		else:
			print "Warning: ignoring", type(primitive)

	def exportEgg(self, path):
		egg = EggData()
		eggVertices = EggVertexPool("humanVertices")

		egg.addChild(eggVertices)

		forEachVisiblePrimitiveIn(self.human, lambda primitive : self.exportPrimitiveToEgg(primitive, eggVertices))

		print "Finishing", path + "..."

		finishEgg(egg, 180.0)

		print "Writing", path + "..."

		egg.writeEgg(path + ".egg")

		print "Export EGG", path + ": OK"

	def exportTexture(self):
		textureMap = NodePath("textureMap")
		# TODO(codistmonk) create a model with triangles using self.human uvs as 3D vertices
		model = self.loader.loadModel("models/teapot")
		model.reparentTo(textureMap)
		model.setPos(0, 0, -1)
		offscreen = self.win.makeTextureBuffer("offscreen", 1024, 1024, Texture(), True)
		offscreenCamera = self.makeCamera(offscreen)
		offscreenCamera.reparentTo(textureMap)
		offscreenCamera.setPos(0, -10, 0)
		light = AmbientLight('light')
		light.setColor(Vec4(0.9, 0.2, 0.9, 1))
		textureMap.setLight(textureMap.attachNewNode(light))
		self.win.getEngine().renderFrame()

		texture = offscreen.getTexture()
		print texture
		print texture.write("test.png")

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
		print "self.find(nodePattern)"
		print "     Return a list of NodePath objects matching nodePattern"
		print "     Example: print self.find(\"helper*\")"
		print
		print "self.show(nodePattern)"
		print "self.hide(nodePattern)"
		print "     Show / hide the NodePath objects matching nodePattern"
		print "     Example: self.hide(\"joint*\")"
		print
		print "self.setColor(r, g, b, nodePattern)"
		print "     Set the color of the NodePath objects matching nodePattern"
		print "     Example: self.setColor(0, 0, 1, \"*cornea*\")"
		print
		print "self.setCenter(nodePattern)"
		print "     Center the view on the NodePath object matching nodePattern"
		print "     Example: self.center(\"*head\")"
		print
		print "self.setExportEgg(path)"
		print "     Export the visible geometry to the specified path"
		print "     Example: self.export(\"model\")"
		print

loadPrcFile("myconfig.prc")

ShowHuman().run()
