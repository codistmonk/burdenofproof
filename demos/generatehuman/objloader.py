from panda3d.core import *
from utils import *
from objparser import *

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

		self.finishGroup()

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

	def finishGroup(self):
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
