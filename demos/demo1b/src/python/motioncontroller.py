from direct.task import Task
from utils import *


class MotionController:

    def __init__(self, application):
        self.application = application
        self.active = True

        self.setupMouseControl()

    def setActive(self, active):
        self.active = active

    def isActive(self):
        return self.active

    def setupMouseControl(self):
        self.application.disableMouse()

        self.mousex = 0
        self.mousey = 0
        self.last = 0
        self.mouseButton = [0, 0, 0]

        self.application.accept("mouse1", self.setMouseButton, [0, 1])
        self.application.accept("mouse1-up", self.setMouseButton, [0, 0])

        self.application.taskMgr.add(self.controlCamera, "cameraTask")

    def setMouseButton(self, button, value):
        self.mouseButton[button] = value

    def controlCamera(self, task):
        # if (self.phoneState.state == "Center"):
        #     return Task.cont
        if not self.isActive():
            return Task.cont

        # figure out how much the mouse has moved (in pixels)
        mouse = self.application.win.getPointer(0)
        x = mouse.getX()
        y = mouse.getY()
        windowCenterX = self.application.win.getXSize() / 2
        windowCenterY = self.application.win.getYSize() / 2
        heading = self.application.camera.getH()
        pitch = self.application.camera.getP()

        if self.application.win.movePointer(0, windowCenterX, windowCenterY):
            heading -= (x - windowCenterX) * 0.2
            pitch = clamp(pitch - (y - windowCenterY) * 0.2, -45, 45)

        self.application.camera.setHpr(heading, pitch, 0)

        elapsed = task.time - self.last

        if (self.last == 0):
            elapsed = 0

        if (self.mouseButton[0]):
            direction = self.application.camera.getMat().getRow3(1)
            self.application.camera.setPos(
                self.application.camera.getPos() + direction * elapsed*30)

        clampX(self.application.camera,
               -self.application.maxX, self.application.maxX)
        clampY(self.application.camera,
               -self.application.maxY, self.application.maxY)
        self.application.camera.setZ(2)

        self.last = task.time

        return Task.cont
