from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from bop import *

class Application(ShowBase):

	def __init__(self):
		ShowBase.__init__(self)

		self.game = Game()
		print self.game.getCityBlueprint()
loadPrcFile("myconfig.prc")

Application().run()
