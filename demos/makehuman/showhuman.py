import sys
from direct.showbase.ShowBase import ShowBase

from orbitalcameracontroller import *
from objparser import *

def addData(writer, values):
	n = len(values)

	if n == 2:
		writer.addData2f(values[0], values[1])
	elif n == 3:
		writer.addData3f(values[0], values[1], values[2])
	elif n == 4:
		writer.addData4f(values[0], values[1], values[2], values[3])
	else:
		raise Exception("Invalid vector size: %d" % n)

def vec3(floats):
	return Vec3(floats[0], floats[1], floats[2])

class ObjLoader(ObjListener):

	def __init__(self, nodeName):
		ObjListener.__init__(self)

		self.vdataFormat = GeomVertexFormat.getV3n3t2()
		self.node = PandaNode(nodeName)
		self.triangles = None
		self.object("object")

	def object(self, name):
		print "object:", name

		self.objectName = name
		self.vertices = []
		self.texcoords = []
		self.normals = []
		self.vertexCopies = []
		self.copyIndices = dict()
		self.reverseCopyIndices = dict()
		self.vdata = GeomVertexData(name, self.vdataFormat, Geom.UHDynamic)
		self.vdataVertex = None
		self.vdataTexcoord = None
		self.vdataNormal = None
		self.faceCount = 0
		self.group(name)

	def group(self, name):
		print "group:", name

		self.finish()

		self.groupName = name

		self.geometry = None
		self.triangles = None

	def vertex(self, values):
		self.vertices.append([values[0], -values[2], values[1]])
		self.vertexCopies.append([])

	def vertexTexture(self, values):
		self.texcoords.append(values)

	def vertexNormal(self, values):
		self.normals.append(values)

	def face(self, values):
		indices = []
		generateNormals = 0

		for v in values:
			key = str(v) + "/" + str(self.faceCount)

			if key in self.copyIndices:
				indices.append(self.copyIndices[key])
			else:
				copyIndex = self.copyIndices.setdefault(key, len(self.copyIndices))
				indices.append(copyIndex)

				index = v[0] - 1

				self.reverseCopyIndices[copyIndex] = index
				self.vertexCopies[index].append(copyIndex)

				n = len(v)
				generateNormals += 1

				if 1 <= n:
					self.ensureVdataVertex()
					addData(self.vdataVertex, self.vertices[index])
				if 2 <= n:
					self.ensureVdataTexcoord()
					addData(self.vdataTexcoord, self.texcoords[v[1] - 1])
				if 3 == n:
					--generateNormals
					self.ensureVdataNormal()
					addData(self.vdataNormal, self.normals[v[2] - 1])
				if n < 1 or 3 < n:
					raise Exception("Invalid vector size: %d" % n)

		n = len(indices)
		normal = Vec3(0.0, 1.0, 0.0)

		if 3 <= n:
			self.ensureTriangles()

			for i in range(2, n):
				self.triangles.addVertex(indices[0])
				self.triangles.addVertex(indices[i - 1])
				self.triangles.addVertex(indices[i])

			if 0 < generateNormals:
				a = vec3(self.vertices[self.reverseCopyIndices[indices[0]]])
				b = vec3(self.vertices[self.reverseCopyIndices[indices[1]]])
				c = vec3(self.vertices[self.reverseCopyIndices[indices[2]]])
				normal = Vec3(b - a).cross(Vec3(c - a))
				normal.normalize()

		for i in range(generateNormals):
			self.ensureVdataNormal()
			addData(self.vdataNormal, normal)

		self.faceCount += 1


	def finish(self):
		if not self.triangles is None:
			self.triangles.closePrimitive()
			self.ensureGeometry()
			self.geometry.addPrimitive(self.triangles)
			geomNode = GeomNode(self.groupName)
			geomNode.addGeom(self.geometry)
			self.node.addChild(geomNode)

	def ensureVdataVertex(self):
		if self.vdataVertex is None:
			self.vdataVertex = GeomVertexWriter(self.vdata, 'vertex')

	def ensureVdataTexcoord(self):
		if self.vdataTexcoord is None:
			self.vdataTexcoord = GeomVertexWriter(self.vdata, 'texcoord')

	def ensureVdataNormal(self):
		if self.vdataNormal is None:
			self.vdataNormal = GeomVertexWriter(self.vdata, 'normal')

	def ensureTriangles(self):
		if self.triangles is None:
			self.triangles = GeomTriangles(Geom.UHDynamic)

	def ensureGeometry(self):
		if self.geometry is None:
			self.geometry = Geom(self.vdata)

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
		self.human = self.render.attachNewNode(ObjParser("data/3dobjs/base.obj", ObjLoader("human")).listener.node)

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
