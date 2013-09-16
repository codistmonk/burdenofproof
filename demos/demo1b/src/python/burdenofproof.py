from direct.actor.Actor import Actor
from direct.filter.CommonFilters import CommonFilters
from direct.showbase.ShowBase import ShowBase
from bop import *
from bopmodel import *
from motioncontroller import *


Hello()


class BurdenOfProof(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        self.useAdvancedVisualEffects = ConfigVariableBool(
            "use-advanced-visual-effects", True)

        self.game = Game()

        self.setupFilters()
        self.setupModels()
        self.setupKeyboardControl()
        self.motionController = MotionController(self)
        self.camera.setPos(0.0, 0.0, 1.7)

    def setupKeyboardControl(self):
        self.accept("escape", sys.exit)

    def setupFilters(self):
        if (self.useAdvancedVisualEffects):
            self.filters = CommonFilters(self.win, self.cam)
            self.filters.setBloom()

    def setupModels(self):
        # Load and transform the panda actor.
        self.pandaActor = Actor("models/panda-model",
                                {"walk": "models/panda-walk4"})
        self.pandaActor.setScale(0.005, 0.005, 0.005)
        self.pandaActor.reparentTo(self.render)
        # Loop its animation.
        self.pandaActor.loop("walk")

        self.maxX = 10.0  # TODO(codistmonk) use city size
        self.maxY = 10.0  # TODO(codistmonk) use city size

loadPrcFile("myconfig.prc")

BurdenOfProof().run()
