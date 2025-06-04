from intomido.composers import *
import numpy as np

class PercussionPattern:
    def __init__(self, duration, subdivisions=16):
        self.subdivisions = subdivisions
        self.velocities = [0 for _ in range(subdivisions*duration)]
        self.duration = duration
        self.note = 60

    def add_to(self, roll: Pianoroll):
        roll.add_rythmic_pattern_list(self.velocities, note=self.note)

    def genmod(self, mods=(4,), div=1):
        velocities = []
        for i in range(self.duration*self.subdivisions // div):
            thisvel = 0
            for j, mod in enumerate(mods):
                j = j + 1
                if i % mod == 0:
                    thisvel = (127*j) // len(mods)
            velocities.append(thisvel)

        cop = velocities.copy()
        for i in range(div):
            velocities.extend(cop)
        velocities = velocities[:self.duration*self.subdivisions]
        print(velocities)
        self.velocities = velocities
        return velocities

    def add_roll(self, before, hits, mod=2, scaleup=False, multiplier=2):
        for i in range(before-hits*multiplier, before):
            if i % mod == 0:
                self.velocities[i] = 100 if not scaleup else 100*(i/before)

        return self.velocities

    def humanize(self, p=1):
        """p from 0 to 10 please"""
        for i, note in enumerate(self.velocities):
            if note > 0:
                self.velocities[i] = self.velocities[i] + rd.randint(0, 10*p) - 10

        for i in range(len(self.velocities)-1):
            if rd.random() < p/10:
                swap(self.velocities, i, i+1)

        self.velocities = [min(max(v, 0), 127) for v in self.velocities]
        return self.velocities
def swap(l, i, j):
    l[i], l[j] = l[j], l[i]








