import sys, os, struct, re
from traceback import *
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from panda3d.egg import *
from direct.task import Task
from direct.gui.DirectGui import *

from orbitalcameracontroller import *
from objparser import *
from objloader import *

def readBinaryTarget(path):
    result = []
    inputFile = open(path, "rb")

    try:
        bytes = inputFile.read(16)

        while bytes:
            vertexIndex, deltaX, deltaY, deltaZ = struct.unpack("<ifff", bytes)
            result.append((vertexIndex, Vec3(deltaX, deltaY, deltaZ)))
            bytes = inputFile.read(16)
    finally:
        inputFile.close()

    return result

def forEachPrimitiveInNode(node, process = lambda stack : None, stack = []):
    stack.append(None)
    stack.append(None)

    for geomIndex in range(node.getNumGeoms()):
        geom = node.getGeom(geomIndex)
        stack[-2] = geom

        for primitiveIndex in range(geom.getNumPrimitives()):
            stack[-1] = geom.getPrimitive(primitiveIndex)
            process(stack)

    stack.pop()
    stack.pop()

def forEachVisiblePrimitiveInNodePath(nodePath, process = lambda stack : None, stack = []):
    stack.append(None)

    for geomNodePath in nodePath.findAllMatches('**/+GeomNode'):
        if not geomNodePath.isHidden():
            stack[-1] = geomNodePath
            forEachPrimitiveInNode(geomNodePath.node(), process, stack)

    stack.pop()

def forEachPrimitiveInNodePath(nodePath, process = lambda stack : None, stack = []):
    stack.append(None)

    for geomNodePath in nodePath.findAllMatches('**/+GeomNode'):
        stack[-1] = geomNodePath
        forEachPrimitiveInNode(geomNodePath.node(), process, stack)

    stack.pop()

def extractTargetDimensionsFromPath(path):
    dimensions = list(set(re.split("[/.-]", re.sub("-([0-9])", "_\g<1>", path.replace("\\", "/")))) - set(["data", "targets", "targetb"]))
    dimensions.sort()

    return dimensions

def loadAllTargets():
    print "loadAllTargets..."

    result = {}

    for root, dirs, files in os.walk("data"):
        for f in files:
            if f.endswith(".targetb"):
                path = os.path.join(root, f)
                dimensions = frozenset(extractTargetDimensionsFromPath(path))
                result[dimensions] = readBinaryTarget(path)

    print "loadAllTargets: OK"

    return result

def addTarget(source, factor, destination):
    for objVertexIndex, delta in source:
        if not objVertexIndex in destination:
            destination[objVertexIndex] = delta * factor
        else:
            destination[objVertexIndex] += delta * factor

class ShowHuman(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        self.useAdvancedVisualEffects = ConfigVariableBool("use-advanced-visual-effects", True)

        self.targets = loadAllTargets()

        self.cameraController = OrbitalCameraController(self)
        self.setupKeyboardControl()
        self.setupGUI()
        self.setupModels()
        self.setupLights()

    def setupModels(self):
        self.dynamicHumanObjLoader = ObjLoader("human")
        self.human = self.render.attachNewNode(ObjParser("data/3dobjs/base.obj", [self.dynamicHumanObjLoader]).listeners[0].node)
        self.setTarget("data/targets/macrodetails/universal-stature-giant")

        # TODO(codistmonk) consider that there may be multiple vdatas
        # for general objs, although Makehuman only has one
        self.dynamicVertices = GeomVertexRewriter(self.dynamicHumanObjLoader.vdata, "vertex")
        self.dynamicNormals = GeomVertexRewriter(self.dynamicHumanObjLoader.vdata, "normal")
        self.dynamicUvs = GeomVertexRewriter(self.dynamicHumanObjLoader.vdata, 'texcoord')
        self.setStaticVertices()

        self.hide("joint*")
        self.setColor("*", 246.0 / 255.0, 202 / 255.0, 185 / 255.0)
        self.setColor("helper-tights", 181.0 / 255.0, 178.0 / 255.0, 171.0 / 255.0)
        self.setColor("helper-skirt", 181.0 / 255.0, 178.0 / 255.0, 171.0 / 255.0)
        self.setColor("*hair", 52.0 / 255.0, 44.0 / 255.0, 40.0 / 255.0)
        self.hide("*genital")
        self.hide("*hair")
        self.hide("helper*")

        self.center("*head")

        self.setDefaultValues()

        # self.applyTargets({"male": 1.0, "female": 0.0, "macrodetails": 1.0, "universal": 1.0, "young": 1.0})
        self.reapplyTargets()

    def reapplyTargets(self):
        self.applyTargets({
        	"macrodetails": 1.0, "universal": 1.0,
        	"male": self.maleVal, "female": self.femaleVal,
        	"baby": self.babyVal, "child": self.childVal, "young": self.youngVal, "old": self.oldVal,
        	"minweight": self.minweightVal, "maxweight": self.maxweightVal, "averageweight": self.averageweightVal,
        	"minmuscle": self.minmuscleVal, "maxmuscle": self.maxmuscleVal, "averagemuscle": self.averagemuscleVal,
        	"dwarf": self.dwarfVal, "giant": self.giantVal,
        	"african": self.africanVal, "asian": self.asianVal, "caucasian": self.caucasianVal})

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

        if (self.useAdvancedVisualEffects and base.win.getGsg().getSupportsBasicShaders() != 0 and base.win.getGsg().getSupportsDepthTexture() != 0):
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
            initialText = "self.setGender(1.0)",
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

    def setTarget(self, path):
        self.targetPath = path
        self.target = readBinaryTarget(path + ".targetb")

    def setStaticVertices(self):
        self.staticVertices = []
        self.dynamicVertices.setRow(0)

        while not self.dynamicVertices.isAtEnd():
            self.staticVertices.append(Vec3(self.dynamicVertices.getData3f()))

    def applyTarget(self, amount):
        for vertexObjIndex, delta in self.target:
            for vertexIndex in self.dynamicHumanObjLoader.vertexCopies[vertexObjIndex]:
                self.dynamicVertices.setRow(vertexIndex)
                self.dynamicVertices.setData3f(self.staticVertices[vertexIndex] + delta * amount)

    def applyTargets(self, factors, amount = 1.0):
        dimensions = set([])

        for key, value in factors.items():
            if 0.0 != value:
                dimensions.add(key)

        print dimensions

        mul = lambda x, y : x * y
        deltas = {}

        for key, value in self.targets.items():
            if key.issubset(dimensions):
                factor = amount * reduce(mul, [factors[k] for k in key])
                print key, factor
                addTarget(value, factor, deltas)

        self.target = deltas.items()
        self.applyTarget(1.0)
        self.updateNormals()

    def getVertex(self, primitive, vertexIndexInPrimitive):
        self.dynamicVertices.setRow(primitive.getVertex(vertexIndexInPrimitive))
        return self.dynamicVertices.getData3f()

    def setNormal(self, primitive, vertexIndexInPrimitive, normal):
        self.dynamicNormals.setRow(primitive.getVertex(vertexIndexInPrimitive))
        self.dynamicNormals.setData3f(normal)

    def updatePrimitiveNormal(self, primitive):
        if isinstance(primitive, GeomTriangles):
            for i in range(0, primitive.getNumVertices(), 3):
                a = self.getVertex(primitive, i + 0)
                b = self.getVertex(primitive, i + 1)
                c = self.getVertex(primitive, i + 2)
                normal = (b - a).cross(c - a)
                normal.normalize()
                self.setNormal(primitive, i + 0, normal)
                self.setNormal(primitive, i + 1, normal)
                self.setNormal(primitive, i + 2, normal)
        else:
            print "Warning: ignoring", type(primitive)

    def updateNormals(self):
        forEachPrimitiveInNodePath(self.human, lambda stack : self.updatePrimitiveNormal(stack[-1]))

    def show(self, nodePattern):
        for nodePath in self.find(nodePattern):
            nodePath.show()

    def hide(self, nodePattern):
        for nodePath in self.find(nodePattern):
            nodePath.hide()

    def setColor(self, nodePattern, r, g, b):
        for nodePath in self.find(nodePattern):
            nodePath.setColor(r, g, b)

    def find(self, nodePattern):
        return self.human.findAllMatches(nodePattern)

    def center(self, nodePattern):
        self.cameraController.target = self.computeCenter(self.human.find(nodePattern).node())

    def sumVertices(self, primitive, result = Vec3(), vertexCount = [0]):
        for k in range(primitive.getNumVertices()):
            self.dynamicVertices.setRow(primitive.getVertex(k))
            result += self.dynamicVertices.getData3f()
            vertexCount[0] += 1

    def computeCenter(self, pandaNode):
        center = Vec3()
        vertexCount = [0]

        forEachPrimitiveInNode(pandaNode, lambda stack : self.sumVertices(stack[-1], center, vertexCount))

        vertexCount = vertexCount[0]

        if 0 < vertexCount:
            center /= vertexCount

        print "center:", center, "computed using", vertexCount, "vertices"

        return center

    def exportPrimitiveToEgg(self, primitive, eggVertices, texture):
        egg = eggVertices.getParent()

        if isinstance(primitive, GeomTriangles):
            for faceIndex in range(primitive.getNumFaces()):
                eggPolygon = EggPolygon()

                eggPolygon.addTexture(texture)
                egg.addChild(eggPolygon)

                for vertexIndex in range(primitive.getPrimitiveStart(faceIndex), primitive.getPrimitiveEnd(faceIndex)):
                    vdataVertexIndex = primitive.getVertex(vertexIndex)
                    self.dynamicVertices.setRow(vdataVertexIndex)
                    self.dynamicUvs.setRow(vdataVertexIndex)
                    vertex = self.dynamicVertices.getData3f()
                    uv = self.dynamicUvs.getData2f()
                    eggPolygon.addVertex(newEggVertex(eggVertices, vertex, uv))
        else:
            print "Warning: ignoring", type(primitive)

    def exportEgg(self, path):
        print "Creating EGG..."

        egg = EggData()
        name = os.path.basename(path)
        textureRelativePath = os.path.join("textures", name)
        eggVertices = EggVertexPool("humanVertices")
        texture = EggTexture("humanTexture",  textureRelativePath + "_diffuse.png")

        egg.addChild(eggVertices)

        forEachVisiblePrimitiveInNodePath(self.human, lambda stack : self.exportPrimitiveToEgg(stack[-1], eggVertices, texture))

        print "Finishing EGG..."

        finishEgg(egg, 180.0)

        print "Writing", path + "..."

        ensureDirectory(path)

        egg.writeEgg(path + ".egg")

        print "Export EGG", path + ": OK"

        self.exportTexture(os.path.join(os.path.dirname(path), textureRelativePath))

    def makeUvTriangle(self, stack, triangles, vdataVertex, vdataColor):
        primitive = stack[-1]
        color = stack[-3].getColor()

        if isinstance(primitive, GeomTriangles):
            for faceIndex in range(primitive.getNumFaces()):
                for vertexIndex in range(primitive.getPrimitiveStart(faceIndex), primitive.getPrimitiveEnd(faceIndex)):
                    self.dynamicUvs.setRow(primitive.getVertex(vertexIndex))
                    uv = self.dynamicUvs.getData2f()
                    triangles.addVertex(vdataVertex.getWriteRow())
                    addData(vdataVertex, Vec3(uv[0] - 0.5, 0.0, uv[1] - 0.5))
                    addData(vdataColor, color)
        else:
            print "Warning: ignoring", type(primitive)

    def makeUvModel(self):
        vdata = GeomVertexData("uvModelVertices", GeomVertexFormat.getV3cp(), Geom.UHDynamic)
        vdataVertex = GeomVertexWriter(vdata, 'vertex')
        vdataColor = GeomVertexWriter(vdata, 'color')
        triangles = GeomTriangles(Geom.UHDynamic)

        forEachVisiblePrimitiveInNodePath(self.human, lambda stack : self.makeUvTriangle(stack, triangles, vdataVertex, vdataColor))

        triangles.closePrimitive()
        geometry = Geom(vdata)
        geometry.addPrimitive(triangles)
        geomNode = GeomNode("uvModel")
        geomNode.addGeom(geometry)
        node = PandaNode("uvModel")
        node.addChild(geomNode)

        return node

    def exportTexture(self, path):
        print "Creating texture..."

        textureMap = NodePath("textureMap")
        model = NodePath(self.makeUvModel())
        model.reparentTo(textureMap)
        model.setTwoSided(True)
        offscreen = self.win.makeTextureBuffer("offscreen", 2048, 2048, Texture(), True)
        offscreenCamera = self.makeCamera(offscreen)
        offscreenCamera.node().setLens(OrthographicLens())
        offscreenCamera.node().getLens().setNearFar(1, 3)
        offscreenCamera.reparentTo(textureMap)
        offscreenCamera.setPos(0, -2, 0)
        light = AmbientLight('light')
        light.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        textureMap.setLight(textureMap.attachNewNode(light))
        self.win.getEngine().renderFrame()

        print "Writing", path + "..."

        ensureDirectory(path)

        if offscreen.getTexture().write(path + "_diffuse.png"):
            print "Export texture", path + ": OK"
        else:
            print "Export texture", path + ": KO"

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
        print "self.setCenter(nodePattern)"
        print "     Center the view on the NodePath object matching nodePattern"
        print "     Example: self.center(\"*head\")"
        print
        print "self.setExportEgg(path)"
        print "     Export the visible geometry to the specified path"
        print "     Example: self.export(\"model\")"
        print

# The following methods have been copied from MakeHuman's human.py and edited

    def setGender(self, gender):
        """
        Sets the gender of the model. 0 is female, 1 is male.

        Parameters
        ----------

        amount:
            *float*. An amount, usually between 0 and 1, specifying how much
            of the attribute to apply.
        """

        gender = min(max(gender, 0.0), 1.0)
        if self.gender == gender:
            return
        self.gender = gender
        self._setGenderVals()
        self.reapplyTargets()

    def getGender(self):
        """
        The gender of this human as a float between 0 and 1.
        0 for completely female, 1 for fully male.
        """
        return self.gender

    def _setGenderVals(self):
        self.maleVal = self.gender
        self.femaleVal = 1 - self.gender

        print "maleVal:", self.maleVal, "femaleVal:", self.femaleVal

    def setAge(self, age):
        """
        Sets the age of the model. 0 for 0 years old, 1 is 70. To set a
        particular age in years, use the formula age_value = age_in_years / 70.

        Parameters
        ----------

        amount:
            *float*. An amount, usually between 0 and 1, specifying how much
            of the attribute to apply.
        """
        age = min(max(age, 0.0), 1.0)
        if self.age == age:
            return
        self.age = age
        self._setAgeVals()
        self.reapplyTargets()

    def getAge(self):
        """
        Age of this human as a float between 0 and 1.
        """
        return self.age

    def getAgeYears(self):
        """
        Return the approximate age of the human in years.
        """
        if self.getAge() < 0.5:
            return self.MIN_AGE + ((self.MID_AGE - self.MIN_AGE) * 2) * self.getAge()
        else:
            return self.MID_AGE + ((self.MAX_AGE - self.MID_AGE) * 2) * (self.getAge() - 0.5)

    def setAgeYears(self, ageYears):
        """
        Set age in amount of years.
        """
        ageYears = float(ageYears)
        if ageYears < self.MIN_AGE or ageYears > self.MAX_AGE:
            raise RuntimeError("Invalid age specified, should be minimum %s and maximum %s." % (self.MIN_AGE, self.MAX_AGE))
        if ageYears < self.MID_AGE:
            age = (ageYears - self.MIN_AGE) / ((self.MID_AGE - self.MIN_AGE) * 2)
        else:
            age = ( (ageYears - self.MID_AGE) / ((self.MAX_AGE - self.MID_AGE) * 2) ) + 0.5
        self.setAge(age)

    def _setAgeVals(self):
        """
        New system (A8):
        ----------------

        1y       10y       25y            90y
        baby    child     young           old
        |---------|---------|--------------|
        0      0.1875      0.5             1  = age [0, 1]

        val ^     child young     old
          1 |baby\ / \ /   \    /
            |     \   \      /
            |    / \ / \  /    \ young
          0 ______________________________> age
               0  0.1875 0.5      1
        """
        if self.age < 0.5:
            self.oldVal = 0.0
            self.babyVal = max(0.0, 1 - self.age * 5.333)  # 1/0.1875 = 5.333
            self.youngVal = max(0.0, (self.age-0.1875) * 3.2) # 1/(0.5-0.1875) = 3.2
            self.childVal = max(0.0, min(1.0, 5.333 * self.age) - self.youngVal)
        else:
            self.childVal = 0.0
            self.babyVal = 0.0
            self.oldVal = max(0.0, self.age * 2 - 1)
            self.youngVal = 1 - self.oldVal

        print "babyVal:", self.babyVal, "childVal:", self.childVal, "youngVal:", self.youngVal, "oldVal:", self.oldVal

    def setWeight(self, weight):
        """
        Sets the amount of weight of the model. 0 for underweight, 1 for heavy.

        Parameters
        ----------

        amount:
            *float*. An amount, usually between 0 and 1, specifying how much
            of the attribute to apply.
        """

        weight = min(max(weight, 0.0), 1.0)
        if self.weight == weight:
            return
        self.weight = weight
        self._setWeightVals()
        self.reapplyTargets()

    def getWeight(self):
        return self.weight

    def _setWeightVals(self):
        self.maxweightVal = max(0.0, self.weight * 2 - 1)
        self.minweightVal = max(0.0, 1 - self.weight * 2)
        self.averageweightVal = 1 - (self.maxweightVal + self.minweightVal)

        print "minweightVal:", self.minweightVal, "maxweightVal:", self.maxweightVal, "averageweightVal", self.averageweightVal

    def setMuscle(self, muscle):
        """
        Sets the amount of muscle of the model. 0 for flacid, 1 for muscular.

        Parameters
        ----------

        amount:
            *float*. An amount, usually between 0 and 1, specifying how much
            of the attribute to apply.
        """

        muscle = min(max(muscle, 0.0), 1.0)
        if self.muscle == muscle:
            return
        self.muscle = muscle
        self._setMuscleVals()
        self.reapplyTargets()

    def getMuscle(self):
        return self.muscle

    def _setMuscleVals(self):
        self.maxmuscleVal = max(0.0, self.muscle * 2 - 1)
        self.minmuscleVal = max(0.0, 1 - self.muscle * 2)
        self.averagemuscleVal = 1 - (self.maxmuscleVal + self.minmuscleVal)

        print "minmuscleVal:", self.minmuscleVal, "maxmuscleVal:", self.maxmuscleVal, "averagemuscleVal", self.averagemuscleVal

    def setHeight(self, height):
        height = min(max(height, 0.0), 1.0)
        if self.height == height:
            return
        self.height = height
        self._setHeightVals()
        self.reapplyTargets()

    def getHeight(self):
        return self.height

    def getHeightCm(self):
        """
        The height in cm.
        """
        bBox = self.mesh.calcBBox()
        return 10*(bBox[1][1]-bBox[0][1])

    def _setHeightVals(self):
        self.dwarfVal = max(0.0, 1 - self.height * 2)
        self.giantVal = max(0.0, self.height * 2 - 1)

        print "dwarfVal:", self.dwarfVal, "giantVal:", self.giantVal

    def setCaucasian(self, caucasian, sync=True):
        caucasian = min(max(caucasian, 0.0), 1.0)
        old = 1 - self.caucasianVal
        self.caucasianVal = caucasian
        if not sync:
            return
        new = 1 - self.caucasianVal
        if old < 1e-6:
            self.asianVal = new / 2
            self.africanVal = new / 2
        else:
            self.asianVal *= new / old
            self.africanVal *= new / old
        self._updateDiffuseColor()
        self.reapplyTargets()

    def getCaucasian(self):
        return self.caucasianVal

    def setAfrican(self, african, sync=True):
        african = min(max(african, 0.0), 1.0)
        old = 1 - self.africanVal
        self.africanVal = african
        if not sync:
            return
        new = 1 - self.africanVal
        if old < 1e-6:
            self.caucasianVal = new / 2
            self.asianVal = new / 2
        else:
            self.caucasianVal *= new / old
            self.asianVal *= new / old
        self._updateDiffuseColor()
        self.reapplyTargets()

    def getAfrican(self):
        return self.africanVal

    def setAsian(self, asian, sync=True):
        asian = min(max(asian, 0.0), 1.0)
        old = 1 - self.asianVal
        self.asianVal = asian
        if not sync:
            return
        new = 1 - self.asianVal
        if old < 1e-6:
            self.caucasianVal = new / 2
            self.africanVal = new / 2
        else:
            self.caucasianVal *= new / old
            self.africanVal *= new / old
        self._updateDiffuseColor()
        self.reapplyTargets()

    def getAsian(self):
        return self.asianVal

    def _updateDiffuseColor(self):
        self.syncRace()

    	print "africanVal:", self.africanVal, "asianVal:", self.asianVal, "caucasianVal:", self.caucasianVal

        asianColor     = Vec3(0.721, 0.568, 0.431)
        africanColor   = Vec3(0.207, 0.113, 0.066)
        caucasianColor = Vec3(0.843, 0.639, 0.517)

        diffuse = asianColor * self.getAsian() + \
                  africanColor * self.getAfrican() + \
                  caucasianColor * self.getCaucasian()

        print "diffuse:", diffuse

    def syncRace(self):
        total = self.caucasianVal + self.asianVal + self.africanVal
        if total < 1e-6:
            self.caucasianVal = self.asianVal = self.africanVal = 1.0/3
        else:
            scale = 1.0 / total
            self.caucasianVal *= scale
            self.asianVal *= scale
            self.africanVal *= scale

    def setDefaultValues(self):
        self.age = 0.5
        self.gender = 0.5
        self.weight = 0.5
        self.muscle = 0.5
        self.height = 0.5
        self.breastSize = 0.5
        self.breastFirmness = 0.5

        self._setGenderVals()
        self._setAgeVals()
        self._setWeightVals()
        self._setMuscleVals()
        self._setHeightVals()

        self.caucasianVal = 1.0 / 3.0
        self.asianVal = 1.0 / 3.0
        self.africanVal = 1.0 / 3.0

        self._updateDiffuseColor()

loadPrcFile("myconfig.prc")

ShowHuman().run()
