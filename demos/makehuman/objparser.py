import sys, os

class ObjCurve:

	def __init__(self, cstype):
		self.cstype = cstype
		self.degree = 0
		self.start = 0.0
		self.end = 1.0
		self.controlPoints = []
		self.knots = []

class ObjListener:

	def object(self, name):
		print "object:", name
		pass

	def group(self, name):
		print "group:", name
		pass

	def vertex(self, values):
		pass

	def vertexTexture(self, values):
		pass

	def vertexNormal(self, values):
		pass

	def face(self, values):
		pass

	def curve(self, cs):
		pass

def parsePoints(tokens):
	result = []

	for vertexInfo in tokens:
		result.append([int(x) for x in vertexInfo.replace("//", "/0/").split("/")])

	return result

class ObjParser:

	def __init__(self, path, listener):
		self.cs = None
		self.listener = listener

		with open(path) as infile:
			for line in infile:
				self.parseLine(line)

	def parseLine(self, line):
		tokens = line.split()

		if not tokens:
			return

		if "o" == tokens[0]:
			self.listener.object(tokens[1])
		elif "g" == tokens[0]:
			self.listener.group(tokens[1])
		elif "v" == tokens[0]:
			self.listener.vertex(tokens[1:])
		elif "vt" == tokens[0]:
			self.listener.vertexTexture(tokens[1:])
		elif "vn" == tokens[0]:
			self.listener.vertexNormal(tokens[1:])
		elif "f" == tokens[0]:
			self.listener.face(parsePoints(tokens[1:]))
		elif "cstype" == tokens[0] and "bspline" == tokens[1]:
			self.cs = ObjCurve(tokens[1])
		elif "deg" == tokens[0]:
			self.cs.degree = int(tokens[1])
		elif "curv" == tokens[0]:
			self.cs.start = float(tokens[1])
			self.cs.end = float(tokens[2])
			self.cs.controlPoints = parsePoints(tokens[3:])
		elif "parm" == tokens[0] and "u" == tokens[1]:
			self.cs.knots = [float(x) for x in tokens[2:]]
		elif "end" == tokens[0]:
			self.listener.curve(self.cs)
			self.cs = None

ObjParser(sys.argv[1], ObjListener())
