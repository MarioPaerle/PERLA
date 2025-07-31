import numpy as np
from midigen import chord_to_notes, generate_midi_numeric, generate_midi
from models import SCM
import random

# Carichiamo il dataset di progressioni di accordi.
# Ogni progressione è codificata come vettore (ad es., one-hot concatenato per ogni accordo)
with open('datas/trap_kick1.txt', 'r') as f:
    datas = f.read().splitlines()

datalist = [[c.strip()+f".{i}" for i, c in enumerate((line.split(', ') + [line.split(', ')[0]]))] for line in datas]
datas2 = np.array(datalist)
mlt = 1
data = np.array(datas2)  # normalizzazione simile all'RBM originale
# print(data)
# Creiamo la BM completa
bm = SCM()

bm.fit(data, hashable=True)

v_init = '127.0'
generated_sample = bm.sequential_predict(v_init, 15, 15)
generated_sample2 = bm.sequential_predict(v_init, 15, 15)
# print(data.tolist().index([generated_sample + [generated_sample[0]]]))
print(generated_sample)
print(generated_sample2)
print(generated_sample in data.tolist())
from ADAMusicGen2 import *
drum = DrumMIDI()
generated_sample = [g.split('.')[0] for i, g in enumerate(generated_sample)] + [g.split('.')[0] for i, g in enumerate(generated_sample2)]
print(generated_sample)
pattern = "[" + ", ".join(generated_sample) + "]"
string = f"drum.add_fixednote_pattern({pattern},  subdivision=1 / 8)"
exec(string)
drum.generate_midi('drum_pattern.mid')
