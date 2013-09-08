import sys, os, struct, re
from traceback import *
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from panda3d.egg import *
from direct.task import Task
from direct.gui.DirectGui import *

from orbitalcameracontroller import *
from objparser import *
from objloader import *

def readBinaryTarget(path):
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

def forEachPrimitiveIn(node, process = lambda stack : None, stack = []):
	stack.append(None)
	stack.append(None)

	for geomIndex in range(node.getNumGeoms()):
		geom = node.getGeom(geomIndex)
		stack[-2] = geom

		for primitiveIndex in range(geom.getNumPrimitives()):
			stack[-1] = geom.getPrimitive(primitiveIndex)
			process(stack)

	stack.pop()
	stack.pop()

def forEachVisiblePrimitiveIn(nodePath, process = lambda stack : None, stack = []):
	stack.append(None)

	for geomNodePath in nodePath.findAllMatches('**/+GeomNode'):
		if not geomNodePath.isHidden():
			stack[-1] = geomNodePath
			forEachPrimitiveIn(geomNodePath.node(), process, stack)

	stack.pop()

def extractTargetDimensionsFromPath(path):
	dimensions = list(set(re.split("[/\-\.]", path.replace("\\", "/"))) - set(["data", "targets", "targetb"]))
	dimensions.sort()

	return dimensions

def loadAllTargets():
	print "loadAllTargets..."

	result = {}

	for root, dirs, files in os.walk("data"):
		for f in files:
			if f.endswith(".targetb"):
				path = os.path.join(root, f)
				dimensions = frozenset(extractTargetDimensionsFromPath(path))
				result[dimensions] = readBinaryTarget(path)

	print "loadAllTargets: OK"

	return result

class ShowHuman(ShowBase):

	def __init__(self):
		ShowBase.__init__(self)

		self.useAdvancedVisualEffects = ConfigVariableBool("use-advanced-visual-effects", True)

		self.targets = loadAllTargets()

		self.setupKeyboardControl()
		self.setupModels()
		self.setupLights()
		self.setupGUI()
		self.cameraController = OrbitalCameraController(self)

	def setupModels(self):
		self.dynamicHumanObjLoader = ObjLoader("human")
		self.human = self.render.attachNewNode(ObjParser("data/3dobjs/base.obj", [self.dynamicHumanObjLoader]).listeners[0].node)
		self.setTarget("data/targets/bust-increase-measure")

		# TODO(codistmonk) consider that there may be multiple vdatas
		# for general objs, although Makehuman only has one
		self.dynamicVertices = GeomVertexRewriter(self.dynamicHumanObjLoader.vdata, 'vertex')
		self.dynamicUvs = GeomVertexRewriter(self.dynamicHumanObjLoader.vdata, 'texcoord')
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
			self.sunlight.node().setShadowCaster(True, 512, 512)
			self.render.setShaderAuto()

		self.ambientLight = self.render.attachNewNode(AmbientLight("ambientLight"))
		self.ambientLight.node().setColor(Vec4(0.2, 0.2, 0.2, 1))
		self.render.setLight(self.ambientLight)

		self.taskMgr.add(self.sunlightConrol, "sunlightControl")

	def sunlightConrol(self, task):
		setOrbiterHeading(self.sunlight, self.camera.getH() + 60.0, self.cameraController.target)

		return Task.cont

	def setupGUI(self):
		self.setColor("*", 246.0 / 255.0, 202 / 255.0, 185 / 255.0)
		self.setColor("helper-tights", 181.0 / 255.0, 178.0 / 255.0, 171.0 / 255.0)
		self.setColor("helper-skirt", 181.0 / 255.0, 178.0 / 255.0, 171.0 / 255.0)
		self.setColor("*hair", 52.0 / 255.0, 44.0 / 255.0, 40.0 / 255.0)
		self.hide("*genital")
		self.userEntry = DirectEntry(text = "" , scale = .05, command = lambda command : self.userEntryChanged(command), initialText = "self.applyTargets({'head':1.0, 'round':0.1, 'square':0.9})",
			width = 40, numLines = 2, focus = 1)
		self.userEntry.setPos(-1.3, 0.0, -0.9)

	def userEntryChanged(self, command):
		try:
			print command
			exec command
		except:
			print sys.exc_info()
			print_tb(sys.exc_info()[2])
		finally:
			self.userEntry["focus"] = True

	def setTarget(self, path):
		self.targetPath = path
		self.target = readBinaryTarget(path + ".targetb")

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

	def applyTargets(self, factors, amount = 1.0):
		dimensions = set([])

		for key, value in factors.items():
			if 0.0 != value:
				dimensions.add(key)

		print dimensions

		mul = lambda x, y : x * y

		for key, value in self.targets.items():
			if key.issubset(dimensions):
				factor = amount * reduce(mul, [factors[k] for k in key])
				print key, factor
				# TODO(codistmonk) dynamic = static + factor * value

	def show(self, nodePattern):
		for nodePath in self.find(nodePattern):
			nodePath.show()

	def hide(self, nodePattern):
		for nodePath in self.find(nodePattern):
			nodePath.hide()

	def setColor(self, nodePattern, r, g, b):
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

		forEachPrimitiveIn(pandaNode, lambda stack : self.sumVertices(stack[-1], center, vertexCount))

		vertexCount = vertexCount[0]

		if 0 < vertexCount:
			center /= vertexCount

		print "center:", center, "computed using", vertexCount, "vertices"

		return center

	def exportPrimitiveToEgg(self, primitive, eggVertices, texture):
		egg = eggVertices.getParent()

		if isinstance(primitive, GeomTriangles):
			for faceIndex in range(primitive.getNumFaces()):
				eggPolygon = EggPolygon()

				eggPolygon.addTexture(texture)
				egg.addChild(eggPolygon)

				for vertexIndex in range(primitive.getPrimitiveStart(faceIndex), primitive.getPrimitiveEnd(faceIndex)):
					vdataVertexIndex = primitive.getVertex(vertexIndex)
					self.dynamicVertices.setRow(vdataVertexIndex)
					self.dynamicUvs.setRow(vdataVertexIndex)
					vertex = self.dynamicVertices.getData3f()
					uv = self.dynamicUvs.getData2f()
					eggPolygon.addVertex(newEggVertex(eggVertices, vertex, uv))
		else:
			print "Warning: ignoring", type(primitive)

	def exportEgg(self, path):
		print "Creating EGG..."

		egg = EggData()
		name = os.path.basename(path)
		textureRelativePath = os.path.join("textures", name)
		eggVertices = EggVertexPool("humanVertices")
		texture = EggTexture("humanTexture",  textureRelativePath + "_diffuse.png")

		egg.addChild(eggVertices)

		forEachVisiblePrimitiveIn(self.human, lambda stack : self.exportPrimitiveToEgg(stack[-1], eggVertices, texture))

		print "Finishing EGG..."

		finishEgg(egg, 180.0)

		print "Writing", path + "..."

		ensureDirectory(path)

		egg.writeEgg(path + ".egg")

		print "Export EGG", path + ": OK"

		self.exportTexture(os.path.join(os.path.dirname(path), textureRelativePath))

	def makeUvTriangle(self, stack, triangles, vdataVertex, vdataColor):
		primitive = stack[-1]
		color = stack[-3].getColor()

		if isinstance(primitive, GeomTriangles):
			for faceIndex in range(primitive.getNumFaces()):
				for vertexIndex in range(primitive.getPrimitiveStart(faceIndex), primitive.getPrimitiveEnd(faceIndex)):
					self.dynamicUvs.setRow(primitive.getVertex(vertexIndex))
					uv = self.dynamicUvs.getData2f()
					triangles.addVertex(vdataVertex.getWriteRow())
					addData(vdataVertex, Vec3(uv[0] - 0.5, 0.0, uv[1] - 0.5))
					addData(vdataColor, color)
		else:
			print "Warning: ignoring", type(primitive)

	def makeUvModel(self):
		vdata = GeomVertexData("uvModelVertices", GeomVertexFormat.getV3cp(), Geom.UHDynamic)
		vdataVertex = GeomVertexWriter(vdata, 'vertex')
		vdataColor = GeomVertexWriter(vdata, 'color')
		triangles = GeomTriangles(Geom.UHDynamic)

		forEachVisiblePrimitiveIn(self.human, lambda stack : self.makeUvTriangle(stack, triangles, vdataVertex, vdataColor))

		triangles.closePrimitive()
		geometry = Geom(vdata)
		geometry.addPrimitive(triangles)
		geomNode = GeomNode("uvModel")
		geomNode.addGeom(geometry)
		node = PandaNode("uvModel")
		node.addChild(geomNode)

		return node

	def exportTexture(self, path):
		print "Creating texture..."

		textureMap = NodePath("textureMap")
		model = NodePath(self.makeUvModel())
		model.reparentTo(textureMap)
		model.setTwoSided(True)
		offscreen = self.win.makeTextureBuffer("offscreen", 2048, 2048, Texture(), True)
		offscreenCamera = self.makeCamera(offscreen)
		offscreenCamera.node().setLens(OrthographicLens())
		offscreenCamera.node().getLens().setNearFar(1, 3)
		offscreenCamera.reparentTo(textureMap)
		offscreenCamera.setPos(0, -2, 0)
		light = AmbientLight('light')
		light.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
		textureMap.setLight(textureMap.attachNewNode(light))
		self.win.getEngine().renderFrame()

		print "Writing", path + "..."

		ensureDirectory(path)

		if offscreen.getTexture().write(path + "_diffuse.png"):
			print "Export texture", path + ": OK"
		else:
			print "Export texture", path + ": KO"

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
		print "self.setColor(nodePattern, r, g, b)"
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
