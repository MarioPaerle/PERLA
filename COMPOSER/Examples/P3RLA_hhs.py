import numpy as np
from COMPOSER.midigen_ import chord_to_notes, generate_midi_numeric, generate_midi
from COMPOSER.models import SCM
import random

"""
Questo esempio mostra come usare la SCM() per generare una seguenza, in questo caso di righe di codice
Che vengono brutalmente eseguite da exec in fondo
"""

with open('../datas/trap_hh1.txt', 'r') as f:
    datas = f.read().split('@\n')[1:-1]

datalist = [[c.strip() for c in line.split('\n')] for line in datas]
datalist2 = []
max_len = len(max(datalist, key=lambda x: len(x)))
for d in datalist:
    datalist2.append(d + ['pass'] * (max_len - len(d)))

datas2 = np.array(datalist2)
mlt = 1
data = np.array(datas2)
bm = SCM()
bm.fit(data, hashable=True)

v_init = random.choice(data)[0]
generated_sample = bm.sequential_predict(v_init, 4, 16)
print(generated_sample)
print(generated_sample in data.tolist()) # Questo controlla che il dato generato non sia già nei dati, in quel caso si può risamplare
from COMPOSER.ADAMusicGen2 import *
drum = DrumMIDI()
exec("\n".join(generated_sample))
drum.generate_midi('drum_pattern.mid')
