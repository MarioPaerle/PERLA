import numpy as np
from COMPOSER.midigen_ import chord_to_notes, generate_midi_numeric, generate_midi, NOTE_TO_MIDI
from COMPOSER.models import DeepSCM, SCM
import random

"""
Quessto Esempio Genera una melodia Phonk (un genere più che banale) per il quale generare melodie
è piuttosto facile
"""

# Carichiamo il dataset di progressioni di accordi.
# Ogni progressione è codificata come vettore
with open('../datas/phonk_melodies1.txt', 'r') as f:
    datas = f.read().splitlines()
datalist = [[c.strip()+f".{i}" for i, c in enumerate((line.split('|') + [line.split('|')[0]]))] for line in datas]

datas2 = np.array(datalist)
mlt = 1
data = np.array(datas2)

bm = DeepSCM(1)

bm.fit(data, hashable=True)

v_init = random.choice(data)[0]
generated_sample = bm.sequential_predict(v_init, 1, 8)
generated_sample += bm.sequential_predict(v_init, 1, 8)
generated_sample += bm.sequential_predict(v_init, 1, 8)
generated_sample += bm.sequential_predict(v_init, 1, 8)

generated_sample = [(100, NOTE_TO_MIDI[k]) for k in " ".join([g.split('.')[0] for g in generated_sample]).split()]
print(len(generated_sample))

from COMPOSER.ADAMusicGen2 import *
drum = DrumMIDI()

drum.add_numeric_pattern(generated_sample, subdivision=1/4)
drum.generate_midi()
