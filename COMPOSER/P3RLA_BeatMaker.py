

import numpy as np
from midigen import chord_to_notes, generate_midi_numeric, generate_midi, CHORD_FORMULAS
from models import SCM
import random
import os
from ADAMusicGen2 import *

NAME = 'songs/song01'
os.makedirs(NAME, exist_ok=True)


class BeatMaker:
    def __init__(self, name, genre='trap'):
        self.genre = genre
        self.name = name
        os.makedirs(name, exist_ok=True)
        self.kicks_pattern = []
        self.progression = []
        self.roots = []
        self.rythm_mask = []

    def generate_kick(self, tmp=5):
        with open(f'datas/{self.genre}_kick1.txt', 'r') as f:
            datas = f.read().splitlines()

        datalist = [[c.strip() + f".{i}" for i, c in enumerate((line.split(', ') + [line.split(', ')[0]]))] for line in
                    datas]
        datas2 = np.array(datalist)
        data = np.array(datas2)  # normalizzazione simile all'RBM originale

        bm = SCM()

        bm.fit(data, hashable=True)

        v_init = '127.0'
        generated_sample = bm.sequential_predict(v_init, tmp, 15)
        generated_sample2 = bm.sequential_predict(v_init, tmp, 15)
        # print(data.tolist().index([generated_sample + [generated_sample[0]]]))
        # print(generated_sample)
        # print(generated_sample2)
        # print(generated_sample in data.tolist())

        drum = DrumMIDI()
        generated_sample = [g.split('.')[0] for i, g in enumerate(generated_sample)] + [g.split('.')[0] for i, g in
                                                                                        enumerate(generated_sample2)]
        # print(generated_sample)
        self.kicks_pattern = generated_sample
        pattern = "[" + ", ".join(generated_sample) + "]"
        string = f"drum.add_fixednote_pattern({pattern},  subdivision=1 / 8)"
        exec(string)
        drum.generate_midi(f'{NAME}/KICK.mid')

    def generate_hh(self, tmp=5):
        with open(f'datas/{self.genre}_hh1.txt', 'r') as f:
            datas = f.read().split('@\n')[1:-1]

        datalist = [[c.strip() for c in line.split('\n')] for line in datas]
        datalist2 = []
        max_len = len(max(datalist, key=lambda x: len(x)))
        for d in datalist:
            datalist2.append(d + ['pass'] * (max_len - len(d)))
        datas2 = np.array(datalist2)
        mlt = 1
        data = np.array(datas2)  # normalizzazione simile all'RBM originale

        # Creiamo la BM completa
        bm = SCM()

        bm.fit(data, hashable=True)

        v_init = random.choice(data)[0]
        generated_sample = bm.sequential_predict(v_init, tmp, 8)
        # print(data.tolist().index([generated_sample + [generated_sample[0]]]))
        print(generated_sample)
        print(generated_sample in data.tolist())
        drum = DrumMIDI()
        exec("\n".join(generated_sample))
        drum.generate_midi(f'{NAME}/hh.mid')

    def generate_snare(self, tmp=5):
        with open(f'datas/{self.genre}_snare1.txt', 'r') as f:
            datas = f.read().splitlines()

        datalist = [[c.strip() + f".{i}" for i, c in enumerate((line.split(', ') + [line.split(', ')[0]]))] for line in
                    datas]
        datas2 = np.array(datalist)
        mlt = 1
        data = np.array(datas2)  # normalizzazione simile all'RBM originale
        # print(data)
        # Creiamo la BM completa
        bm = SCM()

        bm.fit(data, hashable=True)

        v_init = '0.0'
        generated_sample = bm.sequential_predict(v_init, tmp, 15)
        generated_sample2 = bm.sequential_predict(v_init, tmp, 15)
        # print(data.tolist().index([generated_sample + [generated_sample[0]]]))
        print(generated_sample)
        print(generated_sample2)
        print(generated_sample in data.tolist())
        drum = DrumMIDI()
        generated_sample = [g.split('.')[0] for i, g in enumerate(generated_sample)] + [g.split('.')[0] for i, g in
                                                                                        enumerate(generated_sample2)]
        print(generated_sample)
        pattern = "[" + ", ".join(generated_sample) + "]"
        string = f"drum.add_fixednote_pattern({pattern},  subdivision=1 / 8)"
        exec(string)
        drum.generate_midi(f'{NAME}/snare.mid')

    def generate_drums(self, tmp=5):
        self.generate_hh(tmp)
        self.generate_snare(tmp)
        self.generate_kick(tmp)

    def generate_progression(self, genmidi=False):
        with open(f'datas/{self.genre}_progressions1.txt', 'r') as f:
            datas = f.read().splitlines()

        # datas2 = np.array([[str(chord_to_notes(c))[1:-1] for c in line.split()] for line in datas])
        datalist = [[c.strip() for c in (line.split('|') + [line.split('|')[0]])] for line in datas]
        datas2 = np.array(datalist)
        data = np.array(datas2)  # normalizzazione simile all'RBM originale

        # Creiamo la BM completa
        bm = SCM()

        bm.fit(data, hashable=True)

        v_init = random.choice(random.choice(data))
        generated_sample = bm.sequential_predict(v_init, 8, 3)
        self.progression = " ".join(generated_sample).split()
        lower_progression = " ".join(generated_sample).lower().split()
        self.roots = [p[0] for p in lower_progression]
        generated_sample = "|".join(generated_sample)
        if genmidi:
            generate_midi(generated_sample, output_file=f'{NAME}/progression.mid')

    def generate_simple_bass(self, octave=3):
        if len(self.kicks_pattern) == 0:
            raise "No kick pattern found!"
        double_roots = []
        for root in self.roots:
            double_roots.append(root)
            double_roots.append(root)
        pattern = list(zip(self.kicks_pattern, [k + str(octave) for k in double_roots]))
        drum = DrumMIDI()
        drum.add_pattern(pattern)
        drum.generate_midi(f'{NAME}/808.mid')

    def generate_rythm_mask(self, tmp):
        with open(f'datas/{self.genre}_mask1.txt', 'r') as f:
            datas = f.read().replace('|', '').replace('  ', ' ').splitlines()

        datalist = [[c.strip() + f".{i}" for i, c in enumerate((line.split(' ') + [line.split(' ')[0]]))] for line in
                    datas]
        datas2 = np.array(datalist)
        data = np.array(datas2)  # normalizzazione simile all'RBM originale

        bm = SCM()

        bm.fit(data, hashable=True)

        v_init = '1.0'
        generated_sample = bm.sequential_predict(v_init, tmp, 15)
        generated_sample2 = bm.sequential_predict(v_init, tmp, 15)

        generated_sample = [g.split('.')[0] for i, g in enumerate(generated_sample)] + [g.split('.')[0] for i, g in
                                                                                        enumerate(generated_sample2)]
        print(generated_sample)
        self.rythm_mask = [int(g) for g in generated_sample]

    def generate_melody(self):
        midi = DrumMIDI()
        double_prog = []
        for chord in self.progression:
            double_prog.append(chord)
            double_prog.append(chord)
        for i, (chord, k) in enumerate(zip(double_prog, self.rythm_mask)):
            if k == 0:
                continue
            print(chord)
            cf = CHORD_FORMULAS[chord[1:]]
            root = chord_to_notes(chord)[0]
            subdivision_ticks = int(1 / 8 * midi.beats_per_measure * midi.resolution)
            for c in cf:
                midi.add_event(subdivision_ticks * i, root + c, 100, 'note_on')
                midi.add_event(subdivision_ticks * i + subdivision_ticks, root + c, 100, 'note_off')

        midi.generate_midi(f'{NAME}/melody.mid')


if __name__ == '__main__':
    NAME = 'songs/song01'
    bm = BeatMaker(NAME)
    bm.generate_drums(5)
    bm.generate_rythm_mask(5)
    bm.generate_progression(genmidi=False)
    bm.generate_melody()
    bm.generate_simple_bass()
