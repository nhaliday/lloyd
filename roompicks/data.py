from enum import IntEnum, unique
from functools import total_ordering


@unique
class Office(IntEnum):
    president = 0
    secretary = 1
    superintendant = 2
    sociald = 3
    treasurer = 4
    ath = 5
    boc = 6
    redress = 7 # for seniors screwed by roompicks in past two years
    none = 8


@unique
class Cohort(IntEnum):
    senior = 0
    junior = 1
    soph = 2
    ssenior = 3


@total_ordering
class Lloydie:

    def __init__(self, id, cohort, pick, office=Office.none, ucc=False, healthad=False):
        self.id = id # id in houselist
        self.cohort = cohort
        self.pick = pick # pick is based off reverse oc lottery order
        self.office = office
        self.ucc = ucc
        self.healthad = healthad

    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        if self.office == Office.president:
            return True
        elif other.office == Office.president:
            return False
        if self.cohort != other.cohort:
            return self.cohort < other.cohort
        if self.office != other.office:
            return self.office < other.office
        return self.pick < other.pick


@total_ordering
class LloydieGroup:

    def __init__(self, *lloydies, prefs=[]):
        self.l = lloydies
        self.l.sort()
        self.pick = self.l[0]
        self.prefs = prefs # list of (alley, room) pairs in descending order of preference
        self.result = None

    @property
    def ucc(self):
        return any(v.ucc for v in self.l)

    @property
    def healthad(self):
        return sum(v.healthad for v in self.l)

    @property
    def cohort(self):
        return self.pick.cohort

    def __eq__(self, other):
        return self.pick == other.pick

    def __lt__(self, other):
        return self.pick < other.pick
