import numpy as np
from midigen import chord_to_notes, generate_midi_numeric, generate_midi
from models import DeepSCM, SCM
import random

# Carichiamo il dataset di progressioni di accordi.
# Ogni progressione è codificata come vettore (ad es., one-hot concatenato per ogni accordo)
with open('datas/trap_progressions1.txt', 'r') as f:
    datas = f.read().splitlines()

# datas2 = np.array([[str(chord_to_notes(c))[1:-1] for c in line.split()] for line in datas])
datalist = [[c.strip()+f".{i}" for i, c in enumerate((line.split('|') + [line.split('|')[0]]))] for line in datas]

print(datalist)
datas2 = np.array(datalist)
mlt = 1
data = np.array(datas2)  # normalizzazione simile all'RBM originale

# Creiamo la BM completa
bm = DeepSCM(2)

bm.fit(data, hashable=True)

v_init = random.choice(random.choice(data))
print(v_init)
generated_sample = bm.sequential_predict(v_init, 2, 6)
# print(data.tolist().index([generated_sample + [generated_sample[0]]]))
print(generated_sample)
generated_sample = "|".join([g.split('.')[0] for g in generated_sample])
generate_midi(generated_sample)
"""generated_sample = [chord_to_notes(g) for g in generated_sample]
generate_midi_numeric(generated_sample)"""
