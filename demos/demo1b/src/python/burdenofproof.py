from direct.actor.Actor import Actor
from direct.filter.CommonFilters import CommonFilters
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from bop import *
from bopmodel import *
from utils import *


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
        self.setupMouseControl()
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

    def setupMouseControl(self):
        self.disableMouse()

        self.mousex = 0
        self.mousey = 0
        self.last = 0
        self.mousebtn = [0, 0, 0]

        self.accept("mouse1", self.setMouseBtn, [0, 1])
        self.accept("mouse1-up", self.setMouseBtn, [0, 0])

        self.taskMgr.add(self.controlCamera, "cameraTask")

    def setMouseBtn(self, btn, value):
        self.mousebtn[btn] = value

        # if (btn == 0 and value == 1 and self.phoneState.state == "Center"):
        #     phoneDisplayRegionCenterX = self.win.getXSize() *\
        #         (self.phoneState.phoneDisplayRegion.getLeft() +
        #          self.phoneState.phoneDisplayRegion.getRight()) / 2.0
        #     phoneDisplayRegionCenterY = self.win.getYSize() *\
        #         (1.0 - (self.phoneState.phoneDisplayRegion.getBottom() +
        #          self.phoneState.phoneDisplayRegion.getTop()) / 2.0)
        #     mouse = self.win.getPointer(0)
        #     s = 2 ** self.phoneState.minimapZoom
        #     x = clamp(self.camera.getX() + (mouse.getX() -
        #               phoneDisplayRegionCenterX) / s,
        #               -self.maxX, self.maxX)
        #     y = clamp(self.camera.getY() + (phoneDisplayRegionCenterY -
        #               mouse.getY()) / s, -self.maxY, self.maxY)
        #     previousHeading = self.camera.getH() % 360.0
        #     heading = (rad2Deg(atan2(
        #         y - self.camera.getY(), x - camera.getX())) - 90.0) % 360.0

        #     if (180.0 < abs(heading - previousHeading)):
        #         if (previousHeading < heading):
        #             heading -= 360.0
        #         else:
        #             heading += 360.0

        #     self.camera.setH(previousHeading)
        #     self.phoneState.orientationTriangle.setH(previousHeading)

        #     Parallel(
        #         self.camera.posInterval(0.5, Vec3(x, y, self.camera.getZ())),
        #         self.phoneState.minimapCamera.posInterval(0.5, Vec3(
        #             x, y, self.phoneState.minimapCamera.getZ())),
        #         self.phoneState.orientationTriangle.posInterval(0.5, Vec3(
        #             x, y, self.phoneState.orientationTriangle.getZ())),
        #         self.camera.hprInterval(0.5, Vec3(
        #             heading, self.camera.getP(), self.camera.getR())),
        #         self.phoneState.orientationTriangle.hprInterval(0.5, Vec3(
        #             heading,
        #             self.phoneState.orientationTriangle.getP(),
        #             self.phoneState.orientationTriangle.getR()))
        #     ).start()

    def controlCamera(self, task):
        # if (self.phoneState.state == "Center"):
        #     return Task.cont

        # figure out how much the mouse has moved (in pixels)
        mouse = self.win.getPointer(0)
        x = mouse.getX()
        y = mouse.getY()
        windowCenterX = self.win.getXSize() / 2
        windowCenterY = self.win.getYSize() / 2
        heading = self.camera.getH()
        pitch = self.camera.getP()

        if self.win.movePointer(0, windowCenterX, windowCenterY):
            heading -= (x - windowCenterX) * 0.2
            pitch = clamp(pitch - (y - windowCenterY) * 0.2, -45, 45)

        self.camera.setHpr(heading, pitch, 0)

        elapsed = task.time - self.last

        if (self.last == 0):
            elapsed = 0

        if (self.mousebtn[0]):
            direction = self.camera.getMat().getRow3(1)
            self.camera.setPos(self.camera.getPos() + direction * elapsed*30)

        clampX(self.camera, -self.maxX, self.maxX)
        clampY(self.camera, -self.maxY, self.maxY)
        self.camera.setZ(2)

        # self.phoneState.minimapCamera.setX(self.camera.getX())
        # self.phoneState.minimapCamera.setY(self.camera.getY())

        # self.phoneState.orientationTriangle.setX(self.camera.getX())
        # self.phoneState.orientationTriangle.setY(self.camera.getY())
        # self.phoneState.orientationTriangle.setHpr(heading, -90, 0)

        self.last = task.time

        return Task.cont

loadPrcFile("myconfig.prc")

BurdenOfProof().run()
