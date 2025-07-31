import numpy as np
from midigen import chord_to_notes, generate_midi_numeric, generate_midi, NOTE_TO_MIDI
from models import DeepSCM, SCM
import random

# Carichiamo il dataset di progressioni di accordi.
# Ogni progressione è codificata come vettore (ad es., one-hot concatenato per ogni accordo)
with open('datas/phonk_kick1.txt', 'r') as f:
    datas = f.read().splitlines()
# datas2 = np.array([[str(chord_to_notes(c))[1:-1] for c in line.split()] for line in datas])
datalist = [[c.strip()+f".{i}" for i, c in enumerate((line.split('|') + [line.split('|')[0]]))] for line in datas]

print(datalist)
input()
datas2 = np.array(datalist)
mlt = 1
data = np.array(datas2)  # normalizzazione simile all'RBM originale

# Creiamo la BM completa
bm = DeepSCM(1)

bm.fit(data, hashable=True)

v_init = random.choice(data)[0]
print(v_init)
generated_sample = bm.sequential_predict(v_init, 1, 15)
generated_sample += bm.sequential_predict(v_init, 1, 15)
generated_sample += bm.sequential_predict(v_init, 1, 15)
generated_sample += bm.sequential_predict(v_init, 1, 15)
print(generated_sample)
# print(data.tolist().index([generated_sample + [generated_sample[0]]]))
"""generated_sample = "|".join([g.split('.')[0] for g in generated_sample])
generate_midi(generated_sample)"""
# generated_sample = [NOTE_TO_MIDI[g] for g in "".join([gg.split('.')[0].split() for gg in generated_sample])]
generated_sample = [(100, NOTE_TO_MIDI[k]) for k in " ".join([g.split('.')[0] for g in generated_sample]).split()]
print(len(generated_sample))

from ADAMusicGen2 import *
drum = DrumMIDI()

drum.add_numeric_pattern(generated_sample, subdivision=1/16)
drum.generate_midi()
