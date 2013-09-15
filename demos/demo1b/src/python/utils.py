import sys, os
from panda3d.core import *
from panda3d.egg import *

def clamp(value, minValue, maxValue):
    return min(max(minValue, value), maxValue)

def clampX(target, minX, maxX):
    target.setX(clamp(target.getX(), minX, maxX))

def clampY(target, minY, maxY):
    target.setY(clamp(target.getY(), minY, maxY))

def clampZ(target, minZ, maxZ):
    target.setZ(clamp(target.getZ(), minZ, maxZ))

def addEggVertex(eggVertexPool, x, y, z, u = 0, v = 0, useUv = True):
    vertex = EggVertex()

    vertex.setPos(Point3D(x, y, z))

    if useUv:
        vertex.setUv(Point2D(u, v))

    eggVertexPool.addVertex(vertex)

    return vertex

def newGroup(eggData):
    group = EggGroup()

    group.setGroupType(EggGroup.GTInstance)

    eggData.addChild(group)

    return group

def finishEgg(eggData):
    eggData.recomputeVertexNormals(0.0)
    eggData.recomputeTangentBinormalAuto()
    eggData.removeUnusedVertices(True)

applicationName = "burdenofproof"
scriptPath = os.path.dirname(sys.argv[0]).replace("\\", "/")

if sys.platform == 'darwin':
    from AppKit import NSSearchPathForDirectoriesInDomains
    # http://developer.apple.com/DOCUMENTATION/Cocoa/Reference/Foundation/Miscellaneous/Foundation_Functions/Reference/reference.html#//apple_ref/c/func/NSSearchPathForDirectoriesInDomains
    # NSApplicationSupportDirectory = 14
    # NSUserDomainMask = 1
    # True for expanding the tilde into a fully qualified path
    applicationDataPath = os.path.join(NSSearchPathForDirectoriesInDomains(14, 1, True)[0], APPNAME)
elif sys.platform == 'win32':
    applicationDataPath = os.path.join(os.environ['APPDATA'], applicationName)
else:
    applicationDataPath = os.path.expanduser(os.path.join("~", "." + applicationName))

print "applicationName:", applicationName
print "scriptPath:", scriptPath
print "applicationDataPath:", applicationDataPath
