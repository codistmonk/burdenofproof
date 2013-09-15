from bisect import *

oneSecond = 1000L
oneHour = 3600L * oneSecond
oneDay = 24L * oneHour
oneWeek = 7L * oneDay
oneYear = 365L * oneDay
oneMillenium = 1000L * oneYear

def isUndefined(x):
    return x is None

def lerp(t1, v1, t2, v2, t):
    if isUndefined(v1) or isUndefined(v2):
        return None

    return v1 + (v2 - v1) * (t - t1) / (t2 - t1)

class Chronology:

    def __init__(self, period):
        self.period = period
        self.times = []
        self.values = []

    def getPeriod(self):
        return self.period

    def setValue(self, time, value):
        i = bisect(self.times, time)

        if i < len(self.times) and self.times[i] == time:
            self.values[i] = value
        else:
            self.times.insert(i, time)
            self.values.insert(i, value)

    def getValue(self, time):
        return None

class PiecewiseConstantChronology(Chronology):

    def __init__(self, period):
        Chronology.__init__(self, period)

    def getValue(self, time):
        i = bisect(self.times, time % self.getPeriod())

        return self.values[i - 1]

class PiecewiseLinearChronology(Chronology):

    def __init__(self, period):
        Chronology.__init__(self, period)

    def getValue(self, time):
        if 0 == len(self.times):
            return None

        t = time % self.getPeriod()
        i = bisect(self.times, t)

        if i == len(self.times):
            return lerp(self.times[i - 1], self.values[i - 1], self.times[0] + self.getPeriod(), self.values[0], t)

        return lerp(self.times[i - 1], self.values[i - 1], self.times[i], self.values[i], t)

class Persona:

    def __init__(self, period):
        self.position = PiecewiseLinearChronology(period)

    def getPosition(self, time):
        return self.position.getValue(time)

    def setPosition(self, time, value):
        return self.position.setValue(time, value)

class Character:

    def __init__(self):
        self.actualPersona = Persona(oneMillenium)
        self.routinePersona = Persona(oneDay)

    def getActualPersona(self):
        return self.actualPersona

    def getRoutinePersona(self):
        return self.routinePersona

    def getPosition(self, time):
        value = self.getActualPersona().getPosition(time)
        
        return value if not value is None else self.getRoutinePersona().getPosition(time)

class City:

    def __init__(self, blueprintFilePath):
        pass

class Game:

    def __init__(self):
        pass
