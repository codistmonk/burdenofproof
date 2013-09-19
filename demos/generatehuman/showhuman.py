import sys, os, struct, re
from traceback import *
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from panda3d.egg import *
from direct.task import Task
from direct.gui.DirectGui import *

from orbitalcameracontroller import *
from humanbuilder import *

class ShowHuman(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        self.useAdvancedVisualEffects =\
            ConfigVariableBool("use-advanced-visual-effects", True) and\
            base.win.getGsg().getSupportsBasicShaders() and\
            base.win.getGsg().getSupportsGlsl() and\
            base.win.getGsg().getSupportsDepthTexture()

        self.cameraController = OrbitalCameraController(self)
        self.setupKeyboardControl()
        self.setupGUI()
        self.setupModels()
        self.setupLights()

    def setupModels(self):
        self.humanBuilder = HumanBuilder(self)
        self.humanBuilder.human.reparentTo(self.render)

        self.center("*head")

    def setupKeyboardControl(self):
        self.accept("escape", sys.exit)

    def setupLights(self):
        self.sunlight = self.render.attachNewNode(DirectionalLight("sunlight"))
        self.sunlight.setColor(Vec4(0.8, 0.8, 0.8, 1))
        self.sunlight.node().getLens().setFilmSize(32, 32)
        self.sunlight.node().getLens().setNearFar(75,95)
        self.sunlight.setPos(60, 30, 50)
        self.sunlight.lookAt(0, 0, 0)
        self.render.setLight(self.sunlight)

        if ConfigVariableBool("show-sunlight-frustum", True):
            self.sunlight.node().showFrustum()

        if self.useAdvancedVisualEffects:
            self.sunlight.node().setShadowCaster(True, 512, 512)
            self.render.setShaderAuto()

        self.ambientLight = self.render.attachNewNode(AmbientLight("ambientLight"))
        self.ambientLight.node().setColor(Vec4(0.2, 0.2, 0.2, 1))
        self.render.setLight(self.ambientLight)

        self.taskMgr.add(self.sunlightConrol, "sunlightControl")

    def sunlightConrol(self, task):
        setOrbiterHeading(self.sunlight, self.camera.getH() + 60.0, self.cameraController.target)

        return Task.cont

    def setupGUI(self):
        self.userEntry = DirectEntry(text = "" , scale = .05, command = lambda command : self.userEntryChanged(command),
            initialText = "self.help()",
            width = 40, numLines = 2, focus = 1)
        self.userEntry.setPos(-1.3, 0.0, -0.9)

    def userEntryChanged(self, command):
        try:
            print command
            exec command
        except:
            print sys.exc_info()
            print_tb(sys.exc_info()[2])
        finally:
            self.userEntry["focus"] = True

    def center(self, nodePattern):
        self.cameraController.target = self.humanBuilder.computeCenter(self.humanBuilder.human.find(nodePattern).node())

    def __getattr__(self, name):
        return getattr(self.humanBuilder, name)

    def help(self):
        print
        print "self.help()"
        print "     Print this message"
        print
        print "self.setTarget(path)"
        print "     Load the target specified by path"
        print "     Example: self.setTarget(\"data/targets/measure/measure-bust-increase\")"
        print
        print "self.applyTarget(amount)"
        print "     Deform the dynamic model using the current target modulated by the specified amount"
        print "     dynamicModel = staticModel + target * amount"
        print "     The static model is not affected"
        print
        print "self.setStaticVertices()"
        print "     Save the current deformation into the static model"
        print "     staticModel = dynamicModel"
        print
        print "self.find(nodePattern)"
        print "     Return a list of NodePath objects matching nodePattern"
        print "     Example: print self.find(\"helper*\")"
        print
        print "self.show(nodePattern)"
        print "self.hide(nodePattern)"
        print "     Show / hide the NodePath objects matching nodePattern"
        print "     Example: self.hide(\"joint*\")"
        print
        print "self.setColor(nodePattern, r, g, b)"
        print "     Set the color of the NodePath objects matching nodePattern"
        print "     Example: self.setColor(0, 0, 1, \"*cornea*\")"
        print
        print "self.center(nodePattern)"
        print "     Center the view on the NodePath object matching nodePattern"
        print "     Example: self.center(\"*head\")"
        print
        print "self.setExportEgg(path)"
        print "     Export the visible geometry to the specified path"
        print "     Example: self.export(\"model\")"
        print
        print "self.setGender(amount)"
        print "     Morph the dynamic model toward female (amount == 0.0) or male (amount == 1.0)"
        print
        print "self.setAge(amount)"
        print "     Morph the dynamic model toward young (amount == 0.0) or old (amount == 1.0)"
        print
        print "self.setWeight(amount)"
        print "     Morph the dynamic model toward thin (amount == 0.0) or fat (amount == 1.0)"
        print
        print "self.setMuscle(amount)"
        print "     Morph the dynamic model toward light (amount == 0.0) or heavy (amount == 1.0)"
        print
        print "self.setHeight(amount)"
        print "     Morph the dynamic model toward dwarf (amount == 0.0) or giant (amount == 1.0)"
        print
        print "self.setAfrican(amount)"
        print "self.setAsian(amount)"
        print "self.setCaucasian(amount)"
        print "     Morph the dynamic model away (amount == 0.0) or toward (amount == 1.0) a particular ethnicity"
        print

loadPrcFile("myconfig.prc")

ShowHuman().run()
