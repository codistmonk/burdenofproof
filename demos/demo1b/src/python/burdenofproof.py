from direct.actor.Actor import Actor
from direct.filter.CommonFilters import CommonFilters
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from bop import *
from bopmodel import *
from motioncontroller import *
import generatecityparts
import generatecity


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
        self.cityModel = self.loader.loadModel("data/models/city")
        self.cityModel.reparentTo(self.render)
        self.cityModel.setP(-90.0)

        self.pandaActor = Actor("models/panda-model",
                                {"walk": "models/panda-walk4"})
        self.pandaActor.setScale(0.005, 0.005, 0.005)
        self.pandaActor.loop("walk")

        population = self.game.getPopulation()
        self.characterInstances = []

        for i in range(1, population.getCharacterCount()):
            instance = self.render.attachNewNode("characterInstance")
            instance.setPos(
                population.getCharacter(i).getPosition(self.game.getTime()))
            self.pandaActor.instanceTo(instance)
            self.characterInstances.append(instance)

        self.taskMgr.add(self.update, "updateTask")

    def update(self, task):
        self.game.update(oneMinute)  # TODO(?) compute actual milliseconds

        population = self.game.getPopulation()

        for i in range(1, population.getCharacterCount()):
            self.characterInstances[i - 1].setPos(
                population.getCharacter(i).getPosition(self.game.getTime()))

        return Task.cont

loadPrcFile("myconfig.prc")

BurdenOfProof().run()
