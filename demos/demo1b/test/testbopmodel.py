import sys, os
from panda3d.core import *

#scriptPath = os.path.dirname(sys.argv[0])
#sys.path.append(os.path.join(scriptPath, "..", "src", "python"))

from bopmodel import *

midnight = 0L
sixAM = 6L * oneHour
threeAM = 3L * oneHour
sevenAM = 7L * oneHour
eightAM = 8L * oneHour
noon = 12L * oneHour
twoPM = 14L * oneHour
sixPM = 18L * oneHour
sevenPM = 19L * oneHour
eightPM = 20L * oneHour
tenPM = 22L * oneHour
january = -1L * oneDay
february = january + 31L * oneDay
january14th = january + 14L * oneDay
january15th = january + 15L * oneDay
january16th = january + 16L * oneDay
february15th = february + 15L * oneDay

def testRoutinePersona():
	print "testRoutinePersona..."

	character = Character()
	home = Vec3(0.0, 0.0, 0.0)
	office = Vec3(10.0, 10.0, 0.0)
	midway = (home + office) / 2.0

	assert None == character.getPosition(midnight)

	character.getRoutinePersona().setPosition(midnight, home)

	assert home == character.getPosition(midnight)
	assert home == character.getPosition(noon)

	character.getRoutinePersona().setPosition(noon, office)

	assert home   == character.getPosition(midnight)
	assert midway == character.getPosition(sixAM)
	assert office == character.getPosition(noon)
	assert midway == character.getPosition(sixPM)

	character.getRoutinePersona().setPosition(sixAM,   home)
	character.getRoutinePersona().setPosition(eightAM, office)
	character.getRoutinePersona().setPosition(sixPM,   office)
	character.getRoutinePersona().setPosition(eightPM, home)

	assert home   == character.getPosition(midnight)
	assert home   == character.getPosition(sixAM)
	assert midway == character.getPosition(sevenAM)
	assert office == character.getPosition(eightAM)
	assert office == character.getPosition(noon)
	assert office == character.getPosition(sixPM)
	assert midway == character.getPosition(sevenPM)
	assert home   == character.getPosition(eightPM)
	assert home   == character.getPosition(tenPM)
	assert home   == character.getPosition(oneWeek + midnight)
	assert office == character.getPosition(oneWeek + noon)

	print "testRoutinePersona: OK"

def testActualPersona():
	print "testActualPersona..."

	character = Character()
	home = Vec3(0.0, 0.0, 0.0)
	office = Vec3(10.0, 10.0, 0.0)
	dentist = Vec3(10.0, 20.0, 0.0)

	character.getRoutinePersona().setPosition(midnight, home)
	character.getRoutinePersona().setPosition(noon, office)

	character.getActualPersona().setPosition(january15th + midnight - 1L, None)
	character.getActualPersona().setPosition(january15th + midnight,      home)
	character.getActualPersona().setPosition(january15th + noon,          dentist)
	character.getActualPersona().setPosition(january16th + midnight,      home)
	character.getActualPersona().setPosition(january16th + midnight + 1L, None)

	assert home    == character.getPosition(january14th + midnight)
	assert office  == character.getPosition(january14th + noon)
	assert home    == character.getPosition(january15th + midnight)
	assert dentist == character.getPosition(january15th + noon)
	assert home    == character.getPosition(january16th + midnight)
	assert office  == character.getPosition(january16th + noon)
	assert home    == character.getPosition(february15th + midnight)
	assert office  == character.getPosition(february15th + noon)

	print "testActualPersona: OK"

def testPiecewiseConstantChronology():
	print "testPiecewiseConstantChronology..."

	day = PiecewiseConstantChronology(oneDay)

	day.setValue(sixAM, "morning")
	day.setValue(noon,  "afternoon")
	day.setValue(sixPM, "night")

	assert "morning"   == day.getValue(sixAM)
	assert "morning"   == day.getValue(eightAM)
	assert "afternoon" == day.getValue(noon)
	assert "afternoon" == day.getValue(twoPM)
	assert "night"     == day.getValue(sixPM)
	assert "night"     == day.getValue(tenPM)
	assert "night"     == day.getValue(midnight)
	assert "night"     == day.getValue(threeAM)

	print "testPiecewiseConstantChronology: OK"

testRoutinePersona()
testActualPersona()
testPiecewiseConstantChronology()
