import sys
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from bop import *

class Application(ShowBase):

	def __init__(self):
		ShowBase.__init__(self)

		self.game = Game()

		self.setupModels()
		self.setupKeyboard()

	def setupModels(self):
		self.setupCity()

	def setupCity(self):
		blueprint = self.game.getCityBlueprint()
		print "citySize:", blueprint.getSizeNS(), blueprint.getSizeWE()

	def setupKeyboard(self):
		self.accept("escape", sys.exit)

loadPrcFile("myconfig.prc")

Application().run()
