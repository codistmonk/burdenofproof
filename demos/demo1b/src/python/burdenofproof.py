from direct.showbase.ShowBase import ShowBase
from bop import *
from bopmodel import *
from utils import *

Hello()

class BurdenOfProof(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        self.useAdvancedVisualEffects = ConfigVariableBool("use-advanced-visual-effects", True)

        self.game = Game()

        self.setupKeyboardControl()

    def setupKeyboardControl(self):
        self.accept("escape", sys.exit)

loadPrcFile("myconfig.prc")

BurdenOfProof().run()
