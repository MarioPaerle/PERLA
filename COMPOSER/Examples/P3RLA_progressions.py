import numpy as np
from COMPOSER.midigen_ import chord_to_notes, generate_midi_numeric, generate_midi
from COMPOSER.models import DeepSCM, SCM
import random

with open('../datas/trap_progressions1.txt', 'r') as f:
    datas = f.read().splitlines()

# Questa riga aggiunge i positional encodings
datalist = [[c.strip()+f".{i}" for i, c in enumerate((line.split('|') + [line.split('|')[0]]))] for line in datas]

print(datalist) # Per vedere come sono encodate le posizioni
datas2 = np.array(datalist)
mlt = 1
data = np.array(datas2)

bm = DeepSCM(2)

bm.fit(data, hashable=True)

v_init = random.choice(random.choice(data))
print(v_init)
generated_sample = bm.sequential_predict(v_init, 2, 6)
print(generated_sample)
generated_sample = "|".join([g.split('.')[0] for g in generated_sample])
generate_midi(generated_sample)

