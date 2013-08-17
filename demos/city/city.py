from direct.showbase.ShowBase import ShowBase
from direct.directnotify.DirectNotify import DirectNotify
from panda3d.core import Mat4

class MyApp(ShowBase):

	def __init__(self):
		ShowBase.__init__(self)

		self.debug = DirectNotify().newCategory("Debug")

		self.loadModels()
		self.setCameraPos(0, 0, 2)

	def loadModels(self):
		self.loadSky()
		self.loadTerrain()
		self.loadBuildings()

	def loadSky(self):
		self.sky = self.loader.loadModel("models/sky")
		self.sky.reparentTo(self.camera)
		self.sky.setScale(base.camLens.getNear() * 1.1)
		self.sky.setBin("background", 0)
		self.sky.setDepthWrite(False)
		self.sky.setCompass()

	def loadTerrain(self):
		self.terrain = self.loader.loadModel("models/terrain")
		self.terrain.reparentTo(self.render)

	def loadBuildings(self):
		buildingPadPrototype = self.loader.loadModel("models/building_pad")
		buildingPadInstance = render.attachNewNode("Building-Pad-Instance")
		buildingPadPrototype.instanceTo(buildingPadInstance)

	def setCameraPos(self, x, y, z):
		base.disableMouse()
		self.camera.setPos(x, y, z)
		mat = Mat4(self.camera.getMat())
		mat.invertInPlace()
		base.mouseInterfaceNode.setMat(mat)
		base.enableMouse()

app = MyApp()
app.run()
