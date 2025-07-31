import numpy as np
from midigen import chord_to_notes, generate_midi_numeric
from models import SCM, DeepSCM
from random import choice


# Carichiamo il dataset di progressioni di accordi.
# Ogni progressione è codificata come vettore (ad es., one-hot concatenato per ogni accordo)
with open('datas/parole_sillabate_2.txt', 'r') as f:
    datas = ' '.join(f.readlines())

# datas2 = np.array([[str(chord_to_notes(c))[1:-1] for c in line.split()] for line in datas])
datalist = [[c for c in datas.split()]]
print(datalist)
datas2 = np.array(datalist)
print(datas2)
mlt = 1
data = np.array(datas2) # normalizzazione simile all'RBM originale

# Creiamo la BM completa
bm = DeepSCM(10)

bm.fit(data, hashable=True)

v_init = choice(data[0])
print(v_init)
generated_sample = bm.sequential_predict(v_init, 3, 3)
print(''.join(generated_sample).replace('-', ' '))