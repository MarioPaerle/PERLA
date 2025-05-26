from intomido.composers import *
import numpy as np

class PercussionPattern:
    def __init__(self, duration, subdivisions=16):
        self.subdivisions = subdivisions
        self.velocities = [0 for _ in range(subdivisions*duration)]
        self.duration = duration
        self.note = 72

    def add_to(self, roll: Pianoroll):
        roll.add_rythmic_pattern_list(self.velocities, note=self.note)

    def genmod(self, mods=(4,)):
        velocities = []
        for i in range(self.duration*self.subdivisions):
            thisvel = 0
            for j, mod in enumerate(mods):
                j = j + 1
                if i % mod == 0:
                    thisvel = (127*j) // len(mods)

            velocities.append(thisvel)
        self.velocities = velocities
        return velocities

    def add_roll(self, before, hits, mod=2, scaleup=False, multiplier=2):
        for i in range(before-hits*multiplier, before):
            if i % mod == 0:
                self.velocities[i] = 100 if not scaleup else 100*(i/before)

        return self.velocities






