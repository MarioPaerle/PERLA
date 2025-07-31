import numpy as np
from COMPOSER.midigen_ import chord_to_notes, generate_midi_numeric, generate_midi
from COMPOSER.models import SCM
import random

"""Questo fa una specie di Program Synthesis"""

with open('../datas/trap_kick1.txt', 'r') as f:
    datas = f.read().splitlines()

datalist = [[c.strip()+f".{i}" for i, c in enumerate((line.split(', ') + [line.split(', ')[0]]))] for line in datas]
datas2 = np.array(datalist)
mlt = 1
data = np.array(datas2)
bm = SCM()

bm.fit(data, hashable=True)

v_init = '127.0'
generated_sample = bm.sequential_predict(v_init, 15, 15)
generated_sample2 = bm.sequential_predict(v_init, 15, 15)
print(generated_sample in data.tolist())
from COMPOSER.ADAMusicGen2 import *
drum = DrumMIDI()
generated_sample = [g.split('.')[0] for i, g in enumerate(generated_sample)] + [g.split('.')[0] for i, g in enumerate(generated_sample2)]
pattern = "[" + ", ".join(generated_sample) + "]"
string = f"drum.add_fixednote_pattern({pattern},  subdivision=1 / 8)"
drum.generate_midi('drum_pattern.mid')
