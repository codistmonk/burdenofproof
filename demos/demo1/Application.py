from panda3d.core import *
from direct.showbase.ShowBase import ShowBase

class MyApp(ShowBase):

	def __init__(self):
		ShowBase.__init__(self)

loadPrcFile("myconfig.prc")

MyApp().run()
