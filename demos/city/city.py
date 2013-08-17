import threading

from direct.showbase.ShowBase import ShowBase
from direct.directnotify.DirectNotify import DirectNotify

class MyApp(ShowBase):

	def __init__(self):
		ShowBase.__init__(self)

		self.debug = DirectNotify().newCategory("Debug")

		self.loadModels()

	def loadModels(self):
		self.sky = self.loader.loadModel("models/sky")
		self.sky.reparentTo(self.cam)
		self.sky.setScale(2, 2, 2)
		self.sky.setBin("background", 0)
		self.sky.setDepthWrite(False)
		self.sky.setCompass()

app = MyApp()
app.run()
