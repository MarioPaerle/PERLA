import numpy as np
from midigen import chord_to_notes, generate_midi_numeric, generate_midi
from models import SCM
import random

# Carichiamo il dataset di progressioni di accordi.
# Ogni progressione è codificata come vettore (ad es., one-hot concatenato per ogni accordo)
with open('datas/trap_hh1.txt', 'r') as f:
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
generated_sample = bm.sequential_predict(v_init, 4, 16)
# print(data.tolist().index([generated_sample + [generated_sample[0]]]))
print(generated_sample)
print(generated_sample in data.tolist())
from ADAMusicGen2 import *
drum = DrumMIDI()
exec("\n".join(generated_sample))
drum.generate_midi('drum_pattern.mid')
